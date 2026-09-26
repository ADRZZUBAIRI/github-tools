"""
CLI Entry Point & Dynamic Squad Orchestrator for 62-Role SEO Swarm
===================================================================
Executes uninflated role evaluation with GSC dataset ingestion, evidence binding,
universal codebase adaptation, profile/domain-pack resolution, and Chief Referee reality caps.
"""

import os
import sys
import uuid
import re
import json
import argparse
from typing import Dict, Any, Optional

# Ensure package root is importable when executed directly
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation, finalize_run
from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, TASK_ACTIVATION_PRESETS
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps
from seo_swarm.config.profile import load_project_profile
from seo_swarm.adapters.codebase import extract_page_primitives
from seo_swarm.adapters.authority import validate_authority_data
from seo_swarm.adapters.serp import load_serp_snapshot

def run_swarm_audit(
    target_file_path: str,
    task_preset: str = "single_page_audit",
    profile_name_or_path: str = "generic",
    gsc_dir: Optional[str] = None,
    authority_file: Optional[str] = None,
    serp_file: Optional[str] = None,
    db_path: Optional[str] = None,
    json_output: bool = False
) -> Dict[str, Any]:
    if not os.path.exists(target_file_path):
        error_msg = f"Target file '{target_file_path}' does not exist."
        if not json_output:
            print(f"[!] Error: {error_msg}")
        return {"status": "error", "message": error_msg}

    profile = load_project_profile(profile_name_or_path)
    site_url = profile.get("site_url", "https://example.com")
    page_data = extract_page_primitives(target_file_path, site_url=site_url)

    # Ingest verified GSC data (if provided)
    gsc_ingestor = GSCDataIngestor(gsc_dir, expected_site_url=site_url) if gsc_dir else GSCDataIngestor(None)
    site_gsc = gsc_ingestor.get_site_metrics()
    page_gsc = gsc_ingestor.get_page_metrics(target_file_path, page_route=page_data.get("route")) if site_gsc["is_active"] else None

    # Authority Data Handling: Strict validation via Authority Adapter
    authority_data = validate_authority_data(authority_file, expected_site_url=site_url)
    
    # SERP Snapshot Handling
    serp_data = load_serp_snapshot(serp_file)

    active_roles = get_active_roles(task_preset, profile=profile)
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    conn = init_db(db_path)
    store_run(conn, run_id, target_file_path, profile.get("profile_id", "generic"))

    html_content = page_data.get("html", "")
    clean_text = page_data.get("text", "")
    title = page_data.get("title", "")

    evidence_map: Dict[str, Any] = {
        "EVD-TITLE": title,
        "EVD-SCHEMA": "application/ld+json" in html_content,
        "EVD-TEL": "tel:" in html_content,
        "EVD-SECTIONS": str(len(re.findall(r'<(?:section|article|div\s+class=[\'"][^\'"]*(?:container|section|wrapper)[^\'"]*)', html_content, re.IGNORECASE))),
        "EVD-AUTHORITY": authority_data,
        "EVD-PROFILE": profile,
        "EVD-FRAMEWORK": page_data.get("framework", "generic"),
        "EVD-PAGE-PRIMITIVES": page_data
    }
    if site_gsc["is_active"]:
        evidence_map["EVD-GSC-SITE"] = site_gsc
    if page_gsc:
        evidence_map["EVD-GSC-PAGE"] = page_gsc
    if serp_data:
        evidence_map["EVD-SERP-COMPETITORS"] = serp_data

    for k, v in evidence_map.items():
        store_evidence(conn, run_id, k, "source_inspection", target_file_path, "1-end", str(v), {"value": v})

    evaluations = []
    if not json_output:
        print("\n" + "#" * 88)
        print(" " * 20 + "62-ROLE ADVERSARIAL SEO SWARM ENGINE")
        print(" " * 18 + f"Preset: [{task_preset.upper()}] | Profile: [{profile['profile_id']}]")
        print("#" * 88)
        print(f" Target File  : {target_file_path} (Route: {page_data.get('route')} | Framework: {page_data.get('framework')})")
        if site_gsc['is_active']:
            print(f" GSC Ingestion: Active ({site_gsc['complete_days']} days: {site_gsc['total_impressions']} impr, {site_gsc['total_clicks']} clicks across {site_gsc['tracked_pages_count']} pages)")
        else:
            print(f" GSC Ingestion: Not Loaded (Organic search metrics UNKNOWN)")
        print(f" Authority    : {authority_data['status']} ({authority_data.get('referring_domains', 0)} ref domains via {authority_data.get('provider', 'none')})")
        print(f" SERP Data    : {'Verified (' + str(serp_data['target_query']) + ' | KD ' + str(serp_data['keyword_difficulty']) + ')' if serp_data else 'Provisional (No SERP snapshot)'}")
        print(f" Industry/Pack: {profile.get('industry', 'generic')} (Scope: {profile.get('target_scope', 'national')})")
        print(f" Run ID       : {run_id} | Mode: Uninflated Reality Execution")
        print("#" * 88 + "\n")

    for role in active_roles:
        res = role.evaluate(page_data, evidence_map)
        evaluations.append(res)
        store_evaluation(conn, run_id, res["agent_id"], res["role"], res["status"], res["score"], res["verdict"], res["observations"], res["recommendations"])
        
        if not json_output:
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

    scored_evals = [
        e for e in evaluations 
        if e["status"] == "complete" 
        and e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee", "hallucination_redteam"]
    ]
    raw_avg = round(sum(e["score"] for e in scored_evals) / len(scored_evals), 1) if scored_evals else 0.0

    target_locations = profile.get("target_locations", [])
    is_national = profile.get("target_scope") != "local" or (target_locations and not any(loc.lower() in title.lower() for loc in target_locations))
    
    req_signals = profile.get("required_signals", [])
    has_tap_to_call = "tel:" in html_content if "tap_to_call" in req_signals else True
    has_ownership = ("100%" in clean_text or "ownership" in clean_text.lower()) if "ownership_or_trust_guarantee" in req_signals else True
    
    commercial_data = {
        "has_tap_to_call": has_tap_to_call,
        "has_ownership_guarantee": has_ownership
    }
    
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

    # Finalize SQLite run record
    finalize_run(
        conn,
        run_id=run_id,
        raw_score=gate_decision["raw_score"],
        final_score=gate_decision["final_capped_score"],
        verdict=gate_decision["verdict"],
        summary={
            "caps": gate_decision["cap_reasons"],
            "fatal_flaws": fatal_flaws,
            "recs": recs
        }
    )

    report_payload = {
        "run_id": run_id,
        "target": target_file_path,
        "route": page_data.get("route"),
        "public_url": page_data.get("public_url"),
        "profile": profile["profile_id"],
        "industry": profile.get("industry", "generic"),
        "raw_score": gate_decision["raw_score"],
        "final_score": gate_decision["final_capped_score"],
        "verdict": gate_decision["verdict"],
        "hard_caps_applied": gate_decision["hard_caps_applied"],
        "cap_reasons": gate_decision["cap_reasons"],
        "fatal_flaws": fatal_flaws,
        "recommendations": recs,
        "evaluations_count": len(evaluations),
        "scored_specialists_count": len(scored_evals)
    }

    if json_output:
        print(json.dumps(report_payload, indent=2))
    else:
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

    return report_payload

def main():
    parser = argparse.ArgumentParser(description="Run 62-Role Generic SEO Swarm Simulator")
    parser.add_argument("target", nargs="?", default="index.html", help="Path to target page, template or markup file")
    parser.add_argument("--preset", default="single_page_audit", choices=list(TASK_ACTIVATION_PRESETS.keys()))
    parser.add_argument("--profile", default="generic", help="Industry profile pack ('generic', 'saas', 'local_services' or path to profile.yaml/json)")
    parser.add_argument("--gsc-dir", default=None, help="Directory containing GSC CSV exports (Pages.csv, Chart.csv, etc.)")
    parser.add_argument("--authority-file", default=None, help="Validated JSON/CSV file containing referring_domains, domain_authority, and domain name")
    parser.add_argument("--serp-file", default=None, help="JSON file containing competitive SERP snapshot (target_query, keyword_difficulty, top_competitors)")
    parser.add_argument("--db-path", default=None, help="Custom SQLite database path")
    parser.add_argument("--json", action="store_true", help="Output audit report as structured JSON")
    args = parser.parse_args()
    
    run_swarm_audit(args.target, args.preset, args.profile, args.gsc_dir, args.authority_file, args.serp_file, args.db_path, args.json)

if __name__ == "__main__":
    main()
