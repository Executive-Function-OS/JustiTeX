#!/usr/bin/env python3
"""
JustiTeX Incremental Improvement Loop & Monetization Pipeline Auditor
=====================================================================
Automated loop that runs whenever triggered by CI/CD (GitHub Actions),
cron schedulers, or local CLI invocations.

Loop Objectives:
1. Inspect repository state across monetization, legal compliance, and distribution vectors.
2. Verify landing contracts: Stripe checkout ($14 Pro Pack), Clinic license ($149/yr),
   fulfillment page (/success.html), clean print styles (@media print), and download packages.
3. Audit template assets and ensure no banned legal hallucination phrases exist.
4. Identify and rank concrete incremental improvements that move JustiTeX closer to a
   fully functioning application with growing monetization potential.
5. Record telemetry and findings to IMPROVEMENTS.md and exit cleanly.
"""

import sys
import os
import re
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Contract requirements for production & monetization readiness
CRITICAL_CHECKS = [
    {
        "name": "Stripe Live Pro Checkout Link",
        "file": "index.html",
        "pattern": r"buy\.stripe\.com/dRm00cgtQaY20Cf3eS6J201",
        "rationale": "Direct $14.00 monetization conversion point"
    },
    {
        "name": "Clinic License Form & Intake ($149/yr)",
        "file": "index.html",
        "pattern": r"id=[\"']clinicForm[\"']",
        "rationale": "High-ticket institutional tier for legal clinics & defender offices"
    },
    {
        "name": "Clinic License Mailto Endpoint",
        "file": "index.html",
        "pattern": r"annika@executivefunctionos\.com",
        "rationale": "Direct lead dispatch to founder for clinic invoice generation"
    },
    {
        "name": "Print-to-PDF Stylesheet",
        "file": "index.html",
        "pattern": r"@media\s+print",
        "rationale": "Enables instant browser-native 28-line pleading PDF generation"
    },
    {
        "name": "Order Fulfillment Page",
        "file": "success.html",
        "pattern": r"JustiTeX_Pro_Oregon_Template_Pack_v2\.0\.zip",
        "rationale": "Post-Stripe download fulfillment page for paying customers"
    },
    {
        "name": "Pro Pack Archive Available",
        "file": "JustiTeX_Pro_Oregon_Template_Pack_v2.0.zip",
        "exists_only": True,
        "rationale": "Ensures deliverable artifact is staged and downloadable"
    },
    {
        "name": "Free Pack Archive Available",
        "file": "justitex-oregon-template-pack.zip",
        "exists_only": True,
        "rationale": "Guarantees free tier access-to-justice commitment"
    },
    {
        "name": "No Broken Placeholders",
        "file": "index.html",
        "negative_pattern": r"YourUsername",
        "rationale": "Prevents broken template links to non-existent GitHub profiles"
    }
]

# Prohibited phrases based on workspace anti-regression rules
BANNED_PHRASES = [
    ("void ab initio", "Use 'void' instead"),
    ("ORCP 71 E", "Evidentiary hearing (no rule cite)"),
    ("Baile v. Vanderkin", "Use 'Bailey v. Vanderkin'"),
    ("cann supply", "Use 'cannot supply'"),
    ("Jane Smith", "Remove fabricated persona"),
    ("troublemaker", "Remove fabricated quotation")
]


def audit_contracts(root: Path) -> dict:
    results = {"passed": True, "details": []}
    for check in CRITICAL_CHECKS:
        target = root / check["file"]
        status = {"name": check["name"], "file": check["file"], "ok": True, "error": None}
        if not target.exists():
            status["ok"] = False
            status["error"] = f"Missing file: {check['file']}"
            results["passed"] = False
        elif check.get("exists_only"):
            status["ok"] = target.stat().st_size > 0
            if not status["ok"]:
                status["error"] = "File is empty"
                results["passed"] = False
        else:
            content = target.read_text(encoding="utf-8", errors="ignore")
            if "pattern" in check:
                if not re.search(check["pattern"], content):
                    status["ok"] = False
                    status["error"] = f"Pattern not matched: {check['pattern']}"
                    results["passed"] = False
            if "negative_pattern" in check:
                if re.search(check["negative_pattern"], content):
                    status["ok"] = False
                    status["error"] = f"Found prohibited pattern: {check['negative_pattern']}"
                    results["passed"] = False
        results["details"].append(status)
    return results


def check_banned_phrases(root: Path) -> list:
    violations = []
    scan_files = [
        root / "index.html",
        root / "success.html",
        root / "templates" / "oregon_28line_FROZEN.tex",
        root / "templates" / "federal_district_court.tex",
        root / "examples" / "sample_motion.md"
    ]
    for p in scan_files:
        if p.exists() and p.is_file():
            text = p.read_text(encoding="utf-8", errors="ignore")
            for phrase, fix in BANNED_PHRASES:
                if phrase.lower() in text.lower():
                    violations.append({
                        "file": str(p.relative_to(root)),
                        "phrase": phrase,
                        "recommendation": fix
                    })
    return violations


def identify_incremental_improvements(root: Path, contracts: dict) -> list:
    """Evaluates the repository and returns prioritized, actionable improvements."""
    improvements = []

    # 1. Check if web/ and web/dist are in sync with root
    root_idx = (root / "index.html").read_text(encoding="utf-8", errors="ignore") if (root / "index.html").exists() else ""
    web_idx = (root / "web" / "index.html").read_text(encoding="utf-8", errors="ignore") if (root / "web" / "index.html").exists() else ""
    dist_idx = (root / "web" / "dist" / "index.html").read_text(encoding="utf-8", errors="ignore") if (root / "web" / "dist" / "index.html").exists() else ""

    if root_idx != web_idx or root_idx != dist_idx:
        improvements.append({
            "category": "Deployment & Build Sync",
            "priority": "HIGH",
            "title": "Synchronize root and web/dist landing pages",
            "impact": "Guarantees Vercel and GitHub Pages both serve identical latest releases.",
            "action": "Sync root index.html to web/index.html and web/dist/index.html"
        })

    # 2. Check Stripe success fulfillment link in index.html
    if "success.html" not in root_idx:
        improvements.append({
            "category": "Monetization & Conversion",
            "priority": "MEDIUM",
            "title": "Document fulfillment redirect URL in landing documentation",
            "impact": "Increases buyer trust and clarity regarding post-payment download delivery.",
            "action": "Add explicit fulfillment note and links in template pack FAQ section"
        })

    # 3. Check for OpenGraph / social share preview card meta tags
    if 'property="og:image"' not in root_idx:
        improvements.append({
            "category": "Growth & Social Distribution",
            "priority": "MEDIUM",
            "title": "Add OpenGraph social share card and meta tags",
            "impact": "Improves click-through rates and branding when shared on X, LinkedIn, and legal forums.",
            "action": "Include og:image, og:description, and twitter:card meta tags in index.html"
        })

    # 4. Check for automated citation auditing hooks
    filing_pipeline = Path.home() / "filing_pipeline"
    if filing_pipeline.exists():
        improvements.append({
            "category": "Ecosystem Integration",
            "priority": "MEDIUM",
            "title": "Bridge JustiTeX templates with filing_pipeline citation audit validator",
            "impact": "Allows attorney/pro-se filers to run CourtListener citation verifications directly.",
            "action": "Expose ./do validate recipe hooks from filing_pipeline into JustiTeX studio"
        })

    # 5. Check template count expansion
    pro_zip = root / "JustiTeX_Pro_Oregon_Template_Pack_v2.0.zip"
    if pro_zip.exists():
        improvements.append({
            "category": "Product Value Expansion",
            "priority": "LOW",
            "title": "Package additional specialty templates (e.g. Clackamas Local Rule 7.005)",
            "impact": "Enhances the $14 Pro Pack value proposition with county-specific motion forms.",
            "action": "Draft Clackamas UTCR expedited hearing declaration template"
        })

    return improvements


def record_improvements_log(root: Path, contracts: dict, violations: list, improvements: list):
    log_file = root / "IMPROVEMENTS.md"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    passed_count = sum(1 for c in contracts["details"] if c["ok"])
    total_count = len(contracts["details"])
    health_pct = int((passed_count / total_count) * 100) if total_count else 0

    lines = [
        "# JustiTeX Incremental Improvement & Monetization Log",
        "",
        f"**Last Automation Run:** `{now_utc}`  ",
        f"**Readiness Score:** `{health_pct}%` ({passed_count}/{total_count} contract checks passed)  ",
        f"**Anti-Regression Gate:** `{'PASSED' if not violations else 'FAILED'}`  ",
        "",
        "## Current Monetization State",
        "- **Direct Individual Tier:** $14.00 JustiTeX Pro Pack via Stripe (`buy.stripe.com/dRm00cgtQaY20Cf3eS6J201`)",
        "- **Fulfillment Pipeline:** Instant post-checkout delivery via `/success.html`",
        "- **Institutional Tier:** $149.00/year Clinic & Public Defender license inquiry with lead capture",
        "- **Free Access-to-Justice Tier:** Browser-native 28-line studio, JSZip bundle, and GitHub source",
        "- **Print Pipeline:** Zero-friction `@media print` window.print() legal paper generator",
        "",
        "## Verification Checks",
        "| Contract Check | File | Status | Rationale |",
        "|---|---|---|---|"
    ]

    for c in contracts["details"]:
        status_str = "✅ PASS" if c["ok"] else f"❌ FAIL ({c['error']})"
        lines.append(f"| {c['name']} | `{c['file']}` | {status_str} | {c.get('error') or 'Compliant'} |")

    if violations:
        lines.extend([
            "",
            "## ⚠️ Anti-Regression Violations Detected",
            "| File | Prohibited Phrase | Recommended Replacement |",
            "|---|---|---|"
        ])
        for v in violations:
            lines.append(f"| `{v['file']}` | `{v['phrase']}` | {v['recommendation']} |")

    lines.extend([
        "",
        "## Prioritized Incremental Improvement Backlog",
        "| Priority | Category | Improvement Title | Projected Impact |",
        "|---|---|---|---|"
    ])

    for imp in improvements:
        lines.append(f"| **{imp['priority']}** | {imp['category']} | {imp['title']} | {imp['impact']} |")

    lines.extend([
        "",
        "---",
        "*Automated report generated by `scripts/incremental_improvement_loop.py`.*"
    ])

    log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {log_file} ({len(lines)} lines)")


def main():
    parser = argparse.ArgumentParser(description="JustiTeX Incremental Improvement Loop")
    parser.add_argument("--verify", action="store_true", help="Run verification gates (exits 1 if contracts fail)")
    parser.add_argument("--apply", action="store_true", help="Automatically apply eligible improvements")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    args = parser.parse_args()

    contracts = audit_contracts(REPO_ROOT)
    violations = check_banned_phrases(REPO_ROOT)
    improvements = identify_incremental_improvements(REPO_ROOT, contracts)

    record_improvements_log(REPO_ROOT, contracts, violations, improvements)

    if args.json:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "contracts": contracts,
            "violations": violations,
            "improvements": improvements
        }
        print(json.dumps(payload, indent=2))

    if args.apply:
        print("Applying automatic maintenance fixes...")
        # Re-run build_zip if it exists
        build_zip = REPO_ROOT / "build_zip.py"
        if build_zip.exists():
            subprocess.run([sys.executable, str(build_zip)], check=False)
        # Sync web copies
        idx_content = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        succ_content = (REPO_ROOT / "success.html").read_text(encoding="utf-8") if (REPO_ROOT / "success.html").exists() else ""
        for d in [REPO_ROOT / "web", REPO_ROOT / "web" / "dist"]:
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(idx_content, encoding="utf-8")
            if succ_content:
                (d / "success.html").write_text(succ_content, encoding="utf-8")
        print("Successfully synchronized all web distributions.")

    if args.verify:
        if not contracts["passed"] or violations:
            print("❌ Verification GATE FAILED!", file=sys.stderr)
            sys.exit(1)
        print("✅ All verification gates PASSED.")

    sys.exit(0)


if __name__ == "__main__":
    main()
