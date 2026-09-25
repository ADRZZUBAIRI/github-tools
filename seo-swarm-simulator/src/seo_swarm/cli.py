"""
CLI Entry Point & Dynamic Squad Orchestrator for 62-Role SEO Swarm
===================================================================
Executes dynamic role activation by task mode while preserving 5 always-on command roles.
"""

import os
import sys
import uuid
import re
import argparse
from typing import Dict, Any

from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation
from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, ChiefRefereeRole, TASK_ACTIVATION_PRESETS

def run_swarm_audit(target_file_path: str, task_preset: str = "single_page_audit"):
    if not os.path.exists(target_file_path):
        print(f"[!] Error: Target file '{target_file_path}' does not exist.")
        return

    with open(target_file_path, "r", encoding="utf-8", errors="ignore") as f:
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

    active_roles = get_active_roles(task_preset)
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    conn = init_db()
    store_run(conn, run_id, target_file_path, task_preset)

    evidence_map = {
        "EVD-TITLE": title,
        "EVD-SCHEMA": "application/ld+json" in html_content,
        "EVD-TEL": "tel:" in html_content,
        "EVD-SECTIONS": str(len(re.findall(r'<section\b', html_content, re.IGNORECASE)))
    }
    for k, v in evidence_map.items():
        store_evidence(conn, run_id, k, "source_inspection", target_file_path, "1-end", str(v), {"value": v})

    evaluations = []
    print("\n" + "#" * 88)
    print(" " * 20 + "62-ROLE ADVERSARIAL SEO SWARM ENGINE")
    print(" " * 18 + f"Task Preset: [{task_preset.upper()}] ({len(active_roles)} Active Specialists)")
    print("#" * 88)
    print(f" Target File  : {target_file_path}")
    print(f" Run ID       : {run_id} | Total Role Roster: 62 Named Roles")
    print("#" * 88 + "\n")

    for role in active_roles:
        res = role.evaluate(page_data, evidence_map)
        evaluations.append(res)
        store_evaluation(conn, run_id, res["agent_id"], res["role"], res["status"], res["score"], res["verdict"], res["observations"], res["recommendations"])
        
        status_symbol = "[FAIL]" if res["score"] < 50 else ("[WARN]" if res["score"] < 75 else "[PASS]")
        print(f"{status_symbol} [{role.squad}] {res['role']} (Score: {res['score']}/100) -> {res['verdict']}")
        for obs in res["observations"]:
            prefix = "FATAL" if obs["type"] == "fatal_flaw" else ("TRUTH" if obs["type"] == "harsh_truth" else "OBS")
            print(f"   |-- [{prefix}] {obs['statement']}")
        print()

    # Final Chief Referee Decision
    referee_evals = [e for e in evaluations if e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee"]]
    total_score = sum(e["score"] for e in referee_evals)
    avg_score = round(total_score / len(referee_evals), 1) if referee_evals else 50.0
    
    fatal_flaws = []
    recs = []
    for e in evaluations:
        for obs in e.get("observations", []):
            if obs.get("type") == "fatal_flaw":
                fatal_flaws.append(obs["statement"])
        for r in e.get("recommendations", []):
            recs.append(r)
            
    print("=" * 88)
    print("                      CHIEF REFEREE SYNTHESIZED VERDICT")
    print("=" * 88)
    print(f" Composite Reality Score : {avg_score} / 100")
    print(f" Active Roles Evaluated  : {len(active_roles)} specialists (out of 62)")
    print(f" Critical Fatal Flaws    : {len(fatal_flaws)} blockers")
    
    if fatal_flaws:
        print("\n[!] FATAL ARCHITECTURAL & COMMERCIAL FLAWS:")
        for idx, flaw in enumerate(fatal_flaws, 1):
            print(f"   {idx}. {flaw}")
            
    if recs:
        print("\n[+] MANDATORY RESCUE ACTIONS:")
        for r in recs:
            print(f"   * [{r.get('benefit', 'high').upper()}] {r.get('title')}: {r.get('action')}")
    print("=" * 88 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run 62-Role SEO Swarm Simulator")
    parser.add_argument("target", nargs="?", default=r"c:\WebSmitherz\websmitherz\pages\services\roofing-seo.php")
    parser.add_argument("--preset", default="local_roofing_audit", choices=list(TASK_ACTIVATION_PRESETS.keys()))
    args = parser.parse_args()
    
    run_swarm_audit(args.target, args.preset)
