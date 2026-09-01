#!/usr/bin/env python3
"""
publora_publisher.py - Automated Multi-Platform Social Media Publisher for JustiTeX via Publora API
Publishes launch announcements and educational legal tech content to X/Twitter and LinkedIn.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

PUBLORA_BASE_URL = "https://api.publora.com/api/v1"
API_KEY = os.getenv("PUBLORA_API_KEY", "sk_mtizc0ee_d7313bfb.ec8ba871eec7fdb54d0c935c8c23bcff44be9fe25a3f79dbc600")

HEADERS = {
    "x-publora-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_platform_connections():
    req = urllib.request.Request(f"{PUBLORA_BASE_URL}/platform-connections", headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data.get("connections", [])
    except Exception as e:
        print(f"❌ Failed to get platform connections: {e}")
        return []

def create_post(content, platform_ids, scheduled_time=None):
    payload = {
        "content": content,
        "platforms": platform_ids
    }
    if scheduled_time:
        payload["scheduledTime"] = scheduled_time

    req = urllib.request.Request(
        f"{PUBLORA_BASE_URL}/create-post",
        data=json.dumps(payload).encode('utf-8'),
        headers=HEADERS,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {err}")
        return None
    except Exception as e:
        print(f"❌ Error creating post: {e}")
        return None

def publish_launch_campaign():
    connections = get_platform_connections()
    if not connections:
        print("❌ No active platform connections found.")
        return

    print(f"✅ Found {len(connections)} active platform connections:")
    for conn in connections:
        print(f"  • {conn.get('platformId')}: {conn.get('username')} ({conn.get('tokenStatus')})")

    twitter_id = next((c['platformId'] for c in connections if 'twitter' in c['platformId']), None)
    linkedin_id = next((c['platformId'] for c in connections if 'linkedin' in c['platformId']), None)

    # Schedule times: Post 1 in 2 minutes, Post 2 in 4 hours
    now_utc = datetime.now(timezone.utc)
    t1 = (now_utc + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    t2 = (now_utc + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Post 1: Twitter Launch
    if twitter_id:
        tweet_content = (
            "If you've ever filed a pleading in Oregon Circuit Court, you know the frustration of "
            "MS Word line numbers drifting out of alignment with UTCR 2.010 28-line rules.\n\n"
            "We built JustiTeX — an automated 28-line pleading paper engine.\n\n"
            "Type in plain English/Markdown ➔ court-ready PDF in seconds:\n"
            "https://justitex.vercel.app\n\n"
            "#LegalTech #OregonLaw #Paralegal #AccessToJustice"
        )
        res_tw = create_post(tweet_content, [twitter_id], scheduled_time=t1)
        if res_tw:
            print(f"🚀 Scheduled Twitter/X launch post for {t1}: PostGroupId = {res_tw.get('postGroupId')}")

    # Post 2: LinkedIn Launch
    if linkedin_id:
        linkedin_content = (
            "Stop wrestling with Microsoft Word margins: Introducing JustiTeX ⚖️\n\n"
            "For solo practitioners, paralegals, and legal document preparers in Oregon, formatting 28-line "
            "legal pleadings to satisfy UTCR 2.010 is one of the most frustrating, unbillable time sinks in litigation practice.\n\n"
            "A single spacing mismatch can cause line numbers to drift, risking rejected e-filings and missed deadlines.\n\n"
            "JustiTeX eliminates this friction:\n"
            "✅ Exact 28-line frozen vertical pitch matching UTCR 2.010(1) & (2)\n"
            "✅ Standard two-column caption box geometry\n"
            "✅ Works directly in your browser with Markdown or plain text\n"
            "✅ Pre-configured for Oregon Circuit Courts, Court of Appeals, and District of Oregon\n\n"
            "Try the live browser studio: https://justitex.vercel.app\n\n"
            "#LegalTechnology #OregonStateBar #ParalegalServices #SoloLawyer #LawFirmOperations #AccessToJustice"
        )
        res_li = create_post(linkedin_content, [linkedin_id], scheduled_time=t1)
        if res_li:
            print(f"🚀 Scheduled LinkedIn launch post for {t1}: PostGroupId = {res_li.get('postGroupId')}")

if __name__ == "__main__":
    publish_launch_campaign()
