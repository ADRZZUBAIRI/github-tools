"""
CLI Entry Point & Sequential Orchestrator for SEO Swarm Lite
============================================================
Runs the hardware-safe 8-role sequential audit pipeline with SQLite evidence logging.
"""

import os
import sys
import uuid
import re
from typing import Dict, Any

from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation
from seo_swarm.roles.roster import (
    GSCAnalystRole,
    TechnicalSEOGuardianRole,
    IntentContentEditorRole,
    MobileFirstCustomerRole,
    ComparisonShopperRole,
    UXCROReviewerRole,
    DeveloperMaintainerRole,
    AdversarialRefereeRole
)

def run_swarm_audit(target_file_path: str):
    if not os.path.exists(target_file_path):
        print(f"[!] Error: Target file '{target_file_path}' does not exist.")
        return

    with open(target_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    title_m = re.search(r'\$page_title\s*=\s*["\']([^"\']+)["\']|<title>([^<]+)</title>', html_content, re.IGNORECASE)
    title = (title_m.group(1) or title_m.group(2)) if title_m else os.path.basename(target_file_path)

    clean_text = re.sub(r'<[^>]+>', ' ', html_content)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    page_data = {
        "url": target_file_path,
        "title": title,
        "html": html_content,
        "text": clean_text
    }

    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    conn = init_db()
    store_run(conn, run_id, target_file_path, "green")

    # Ingest Evidence
    evidence_map = {
        "EVD-TITLE": title,
        "EVD-SCHEMA": "application/ld+json" in html_content,
        "EVD-TEL": "tel:" in html_content,
        "EVD-SECTIONS": str(len(re.findall(r'<section\b', html_content, re.IGNORECASE)))
    }
    for k, v in evidence_map.items():
        store_evidence(conn, run_id, k, "source_inspection", target_file_path, "1-end", str(v), {"value": v})

    # Sequential Evaluation: 7 Analyst Roles
    analyst_roles = [
        GSCAnalystRole(),
        TechnicalSEOGuardianRole(),
        IntentContentEditorRole(),
        MobileFirstCustomerRole(),
        ComparisonShopperRole(),
        UXCROReviewerRole(),
        DeveloperMaintainerRole()
    ]

    evaluations = []
    print("=" * 72)
    print(f"SEO SWARM LITE: 8-ROLE AUDIT PIPELINE")
    print(f"Target: {target_file_path}")
    print(f"Run ID: {run_id} | Mode: Single-Thread Green Profile")
    print("=" * 72 + "\n")

    for role in analyst_roles:
        res = role.evaluate(page_data, evidence_map)
        evaluations.append(res)
        store_evaluation(conn, run_id, res["agent_id"], res["role"], res["status"], res["score"], res["verdict"], res["observations"], res["recommendations"])
        print(f"[{res['role']}] Score: {res['score']}/100 -> Verdict: {res['verdict']}")
        for obs in res["observations"]:
            print(f"   • [{obs['type'].upper()}] {obs['statement']}")
        print()

    # Role 8: Adversarial Referee Synthesizer
    referee = AdversarialRefereeRole()
    final_verdict = referee.evaluate_swarm(evaluations)
    print("=" * 72)
    print(f"[Adversarial Evidence Referee Consensus]")
    print(f"Composite Score : {final_verdict['composite_score']} / 100")
    print(f"Status Verdict  : {final_verdict['consensus']}")
    print(f"Total Roles Run : {final_verdict['total_evaluations']} active constrained roles")
    print("=" * 72)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = r"c:\WebSmitherz\websmitherz\pages\local\roofing-seo-waco-tx.php"
    run_swarm_audit(target)
