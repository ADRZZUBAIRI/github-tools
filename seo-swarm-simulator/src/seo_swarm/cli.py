"""
CLI Entry Point & Dynamic Squad Orchestrator for 62-Role SEO Swarm
===================================================================
Executes uninflated role evaluation with GSC dataset ingestion, evidence binding,
and hard reality caps enforced by Chief Referee.
"""

import os
import sys
import uuid
import re
import argparse
from typing import Dict, Any, Optional

from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation
from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, TASK_ACTIVATION_PRESETS
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps

def run_swarm_audit(target_file_path: str, task_preset: str = "single_page_audit", gsc_dir: Optional[str] = None, authority_file: Optional[str] = None):
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

    # Ingest verified GSC data (if provided)
    gsc_ingestor = GSCDataIngestor(gsc_dir) if gsc_dir else GSCDataIngestor(None)
    site_gsc = gsc_ingestor.get_site_metrics()
    page_gsc = gsc_ingestor.get_page_metrics(target_file_path) if site_gsc["is_active"] else None

    # Authority Data Handling: Default to UNKNOWN unless verified provider is supplied
    authority_data = {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0}
    if authority_file and os.path.exists(authority_file):
        # Support basic JSON authority input
        try:
            import json
            with open(authority_file, "r", encoding="utf-8") as af:
                authority_data = json.load(af)
                authority_data["status"] = "VERIFIED"
        except Exception:
            authority_data = {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0}

    active_roles = get_active_roles(task_preset)
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    conn = init_db()
    store_run(conn, run_id, target_file_path, task_preset)

    evidence_map: Dict[str, Any] = {
        "EVD-TITLE": title,
        "EVD-SCHEMA": "application/ld+json" in html_content,
        "EVD-TEL": "tel:" in html_content,
        "EVD-SECTIONS": str(len(re.findall(r'<section\b', html_content, re.IGNORECASE))),
        "EVD-AUTHORITY": authority_data
    }
    if site_gsc["is_active"]:
        evidence_map["EVD-GSC-SITE"] = site_gsc
    if page_gsc:
        evidence_map["EVD-GSC-PAGE"] = page_gsc

    for k, v in evidence_map.items():
        store_evidence(conn, run_id, k, "source_inspection", target_file_path, "1-end", str(v), {"value": v})

    evaluations = []
    print("\n" + "#" * 88)
    print(" " * 20 + "62-ROLE ADVERSARIAL SEO SWARM ENGINE")
    print(" " * 18 + f"Task Preset: [{task_preset.upper()}] ({len(active_roles)} Active Specialists)")
    print("#" * 88)
    print(f" Target File  : {target_file_path}")
    if site_gsc['is_active']:
        print(f" GSC Ingestion: Active ({site_gsc['complete_days']} days: {site_gsc['total_impressions']} impr, {site_gsc['total_clicks']} clicks across {site_gsc['tracked_pages_count']} pages)")
    else:
        print(f" GSC Ingestion: Not Loaded (Organic search metrics UNKNOWN)")
    print(f" Authority    : {authority_data['status']} ({authority_data.get('referring_domains', 0)} ref domains)")
    print(f" Run ID       : {run_id} | Mode: Uninflated Reality Execution")
    print("#" * 88 + "\n")

    for role in active_roles:
        res = role.evaluate(page_data, evidence_map)
        evaluations.append(res)
        store_evaluation(conn, run_id, res["agent_id"], res["role"], res["status"], res["score"], res["verdict"], res["observations"], res["recommendations"])
        
        if res["status"] == "not_implemented":
            print(f"[SKIP] [{role.squad}] {res['role']} -> NOT_IMPLEMENTED (Excluded from calculation)")
        elif res["status"] == "insufficient_evidence":
            print(f"[WARN] [{role.squad}] {res['role']} -> INSUFFICIENT_EVIDENCE ({res['verdict']})")
            for obs in res["observations"]:
                print(f"   |-- [MISSING DATA] {obs['statement']}")
            print()
        else:
            status_symbol = "[FAIL]" if res["score"] < 50 else ("[WARN]" if res["score"] < 75 else "[PASS]")
            print(f"{status_symbol} [{role.squad}] {res['role']} (Score: {res['score']}/100) -> {res['verdict']}")
            for obs in res["observations"]:
                prefix = "FATAL" if obs["type"] == "fatal_flaw" else ("TRUTH" if obs["type"] == "harsh_truth" else "OBS")
                print(f"   |-- [{prefix}] {obs['statement']}")
            print()

    # Filter out unimplemented, insufficient_evidence, and command roles from mathematical raw average
    scored_evals = [
        e for e in evaluations 
        if e["status"] == "complete" 
        and e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee", "hallucination_redteam"]
    ]
    raw_avg = round(sum(e["score"] for e in scored_evals) / len(scored_evals), 1) if scored_evals else 0.0

    # Apply Chief Referee Hard Reality Caps
    is_national = ("roofing seo" in title.lower() or "seo services" in title.lower()) and not any(c in title.lower() for c in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
    commercial_data = {"has_tap_to_call": "tel:" in html_content, "has_ownership_guarantee": ("100%" in clean_text or "ownership" in clean_text.lower())}
    
    gate_decision = apply_hard_reality_caps(
        raw_score=raw_avg,
        gsc_metrics=site_gsc,
        page_metrics=page_gsc,
        authority_data=authority_data,
        commercial_data=commercial_data,
        is_national_target=is_national
    )

    fatal_flaws = []
    recs = []
    for e in evaluations:
        for obs in e.get("observations", []):
            if obs.get("type") == "fatal_flaw":
                fatal_flaws.append(obs["statement"])
        for r in e.get("recommendations", []):
            recs.append(r)

    print("=" * 88)
    print("                      CHIEF REFEREE SYNTHESIZED DECISION")
    print("=" * 88)
    print(f" Raw Heuristic Score     : {gate_decision['raw_score']} / 100")
    print(f" Final Capped Score      : {gate_decision['final_capped_score']} / 100")
    print(f" Decision Verdict        : {gate_decision['verdict']}")
    print(f" Scored Specialists      : {len(scored_evals)} evaluated (of {len(active_roles)} active in preset)")
    
    if gate_decision["hard_caps_applied"]:
        print("\n[!] HARD REALITY CAPS APPLIED BY CHIEF REFEREE:")
        for r in gate_decision["cap_reasons"]:
            print(f"   * [CAP {gate_decision['final_capped_score']}/100] {r}")

    if fatal_flaws:
        print("\n[!] FATAL STRUCTURAL FLAWS EXPOSED:")
        for idx, flaw in enumerate(fatal_flaws, 1):
            print(f"   {idx}. {flaw}")
            
    if recs:
        print("\n[+] MANDATORY RESCUE ACTIONS:")
        for r in recs:
            print(f"   * [{r.get('benefit', 'high').upper()}] {r.get('title')}: {r.get('action')}")
    print("=" * 88 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Run 62-Role SEO Swarm Simulator")
    parser.add_argument("target", nargs="?", default=r"c:\WebSmitherz\websmitherz\pages\services\roofing-seo.php")
    parser.add_argument("--preset", default="single_page_audit", choices=list(TASK_ACTIVATION_PRESETS.keys()))
    parser.add_argument("--gsc-dir", default=None, help="Directory containing GSC CSV exports (Pages.csv, Chart.csv, etc.)")
    parser.add_argument("--authority-file", default=None, help="JSON file containing verified referring_domains and domain_authority")
    args = parser.parse_args()
    
    run_swarm_audit(args.target, args.preset, args.gsc_dir, args.authority_file)

if __name__ == "__main__":
    main()
