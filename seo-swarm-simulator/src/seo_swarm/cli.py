"""
CLI Entry Point & Brutal Orchestrator for SEO Swarm Simulator (12-Persona Suite)
=================================================================================
Runs the ruthless 12-persona adversarial reality pipeline.
"""

import os
import sys
import uuid
import re
from typing import Dict, Any

from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation
from seo_swarm.roles.roster import (
    SERPExecutionerRole,
    NavBoostClickstreamCriticRole,
    AIOverviewInterceptorRole,
    BacklinkDebtCollectorRole,
    InformationGainTribunalRole,
    InternalLinkMeshAuditorRole,
    SchemaKnowledgeGraphProsecutorRole,
    CoreWebVitalsTerminatorRole,
    SkepticalBlueCollarCFORole,
    B2BOperationsBuyerRole,
    VCCompetitorPredatorRole,
    AdversarialRefereeRole
)

def run_swarm_audit(target_file_path: str):
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

    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    conn = init_db()
    store_run(conn, run_id, target_file_path, "brutal_12_persona_mode")

    evidence_map = {
        "EVD-TITLE": title,
        "EVD-SCHEMA": "application/ld+json" in html_content,
        "EVD-TEL": "tel:" in html_content,
        "EVD-SECTIONS": str(len(re.findall(r'<section\b', html_content, re.IGNORECASE)))
    }
    for k, v in evidence_map.items():
        store_evidence(conn, run_id, k, "source_inspection", target_file_path, "1-end", str(v), {"value": v})

    analyst_roles = [
        SERPExecutionerRole(),
        NavBoostClickstreamCriticRole(),
        AIOverviewInterceptorRole(),
        BacklinkDebtCollectorRole(),
        InformationGainTribunalRole(),
        InternalLinkMeshAuditorRole(),
        SchemaKnowledgeGraphProsecutorRole(),
        CoreWebVitalsTerminatorRole(),
        SkepticalBlueCollarCFORole(),
        B2BOperationsBuyerRole(),
        VCCompetitorPredatorRole()
    ]

    evaluations = []
    print("\n" + "#" * 84)
    print(" " * 18 + "BRUTAL ADVERSARIAL SEO SWARM: 12-PERSONA AUDIT")
    print(" " * 22 + "(The Depressing Truth About Your SERP Rankings)")
    print("#" * 84)
    print(f" Target File  : {target_file_path}")
    print(f" Run ID       : {run_id} | Mode: 12-Persona Reality Execution")
    print("#" * 84 + "\n")

    for role in analyst_roles:
        res = role.evaluate(page_data, evidence_map)
        evaluations.append(res)
        store_evaluation(conn, run_id, res["agent_id"], res["role"], res["status"], res["score"], res["verdict"], res["observations"], res["recommendations"])
        
        status_symbol = "[FAIL]" if res["score"] < 50 else ("[WARN]" if res["score"] < 75 else "[PASS]")
        print(f"{status_symbol} [{res['role']}] Score: {res['score']}/100 -> Verdict: {res['verdict']}")
        for obs in res["observations"]:
            prefix = "FATAL" if obs["type"] == "fatal_flaw" else ("TRUTH" if obs["type"] == "harsh_truth" else "OBS")
            print(f"   |-- [{prefix}] {obs['statement']}")
        print()

    referee = AdversarialRefereeRole()
    final_verdict = referee.evaluate_swarm(evaluations)
    
    print("=" * 84)
    print("                        ADVERSARIAL REALITY CONSENSUS")
    print("=" * 84)
    print(f" Composite Reality Score : {final_verdict['composite_reality_score']} / 100")
    print(f" Depression Index        : {final_verdict['depression_index']}")
    print(f" Algorithmic Verdict     : {final_verdict['consensus']}")
    print(f" Fatal Flaws Exposed     : {final_verdict['fatal_flaws_count']} critical structural blockers")
    
    if final_verdict["fatal_flaws"]:
        print("\n[!] FATAL ARCHITECTURAL & STRATEGIC FLAWS:")
        for idx, flaw in enumerate(final_verdict["fatal_flaws"], 1):
            print(f"   {idx}. {flaw}")
            
    if final_verdict.get("priority_recommendations"):
        print("\n[+] MANDATORY RESCUE ACTIONS (HOW TO STOP GETTING 0 CLICKS):")
        for r in final_verdict["priority_recommendations"]:
            print(f"   * [{r.get('benefit', 'high').upper()}] {r.get('title')}: {r.get('action')}")
    print("=" * 84 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = r"c:\WebSmitherz\websmitherz\pages\services\roofing-seo.php"
    run_swarm_audit(target)
