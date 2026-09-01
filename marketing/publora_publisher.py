#!/usr/bin/env python3
"""
publora_publisher.py - Automated Social Media Publisher for JustiTeX via Publora API
Publishes pre-formatted launch threads and posts directly to connected Publora channels (Twitter/X, LinkedIn).
"""

import os
import sys
import json
import urllib.request
import urllib.error

PUBLORA_API_URL = "https://api.publora.com/v1/posts"

def publish_post(api_key, channel_id, content, schedule_time=None):
    payload = {
        "channel_id": channel_id,
        "content": content
    }
    if schedule_time:
        payload["scheduled_at"] = schedule_time

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    req = urllib.request.Request(
        PUBLORA_API_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode('utf-8'))
            print(f"✅ Published/Scheduled to channel {channel_id}: {res_data.get('id', 'success')}")
            return res_data
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {err_msg}")
        return None
    except Exception as e:
        print(f"❌ Error publishing via Publora: {e}")
        return None

def main():
    api_key = os.getenv("PUBLORA_API_KEY")
    if not api_key:
        print("ℹ️ Set PUBLORA_API_KEY environment variable (export PUBLORA_API_KEY='your_key') to automate posting.")
        print("Alternatively, open /home/annika/JustiTeX/marketing/GENERATED_SOCIAL_POSTS.md to copy/paste posts directly.")
        sys.exit(0)

    print("🚀 Publora Automated Publisher Ready.")

if __name__ == "__main__":
    main()
