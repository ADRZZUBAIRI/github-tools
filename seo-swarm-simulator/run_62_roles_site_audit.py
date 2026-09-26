"""
Site-Wide 62-Role Universal Multi-Agent Audit Runner
====================================================
Runs the 62-role adversarial swarm across every public route in ANY web codebase
(HTML, PHP, Next.js/React, Vue/Nuxt, Astro, Laravel, Django).
Uses the universal codebase adapter, profile system, GSC ingestor, and Chief Referee decision gates.
"""

import os
import sys
import re
import json
import uuid
import argparse
from collections import defaultdict
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps
from seo_swarm.config.profile import load_project_profile
from seo_swarm.adapters.codebase import extract_page_primitives, discover_public_codebase_routes
from seo_swarm.adapters.authority import validate_authority_data
from seo_swarm.adapters.serp import load_serp_snapshot
from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation, finalize_run

def run_universal_site_audit(
    root_dir: str,
    out_file: str,
    profile_name_or_path: str = "generic",
    gsc_dir: Optional[str] = None,
    authority_file: Optional[str] = None,
    serp_file: Optional[str] = None,
    db_path: Optional[str] = None
):
    if not os.path.exists(root_dir):
        print(f"[!] Error: Root directory '{root_dir}' does not exist.")
        return

    profile = load_project_profile(profile_name_or_path)
    site_url = profile.get("site_url", "https://example.com")
    extensions = profile.get("codebase", {}).get("extensions", [".html", ".htm", ".php", ".jsx", ".tsx", ".vue", ".astro"])
    
    public_files = discover_public_codebase_routes(root_dir, extensions=extensions)
    total_pages = len(public_files)
    
    if total_pages == 0:
        print(f"[!] Warning: No public routes found under '{root_dir}' with extensions {extensions}.")
        return

    total_evals = total_pages * len(ALL_62_ROLES)
    
    gsc_ingestor = GSCDataIngestor(gsc_dir, expected_site_url=site_url) if gsc_dir else GSCDataIngestor(None)
    site_gsc = gsc_ingestor.get_site_metrics()
    
    authority_data = validate_authority_data(authority_file, expected_site_url=site_url)
    serp_data = load_serp_snapshot(serp_file)

    print("\n" + "=" * 92)
    print("      UNIVERSAL 62-ROLE ADVERSARIAL MULTI-AGENT SITE AUDIT")
    print(f"      Auditing {total_pages} Public Routes x 62 Specialists = {total_evals:,} Total Evaluations")
    print(f"      Root Directory : {root_dir}")
    print(f"      Profile/Pack   : {profile['profile_id']} ({profile.get('industry', 'generic')})")
    print(f"      GSC Ingestion  : {'Active (' + str(site_gsc['complete_days']) + ' days: ' + str(site_gsc['total_impressions']) + ' impr, ' + str(site_gsc['total_clicks']) + ' clicks)' if site_gsc['is_active'] else 'Not Loaded (Scores Gated at <= 20/100)'}")
    print(f"      Authority Data : {authority_data['status']} ({authority_data.get('referring_domains', 0)} ref domains via {authority_data.get('provider', 'none')})")
    print(f"      SERP Snapshot  : {'Loaded (KD ' + str(serp_data['keyword_difficulty']) + ')' if serp_data else 'Provisional (None)'}")
    print("=" * 92 + "\n")
    
    conn = init_db(db_path)
    active_roles = get_active_roles("full_red_team_all_62", profile=profile)
    
    results = []
    category_scores = defaultdict(list)
    squad_scores = defaultdict(list)
    fatal_flaws_tally = defaultdict(int)
    
    target_locations = profile.get("target_locations", [])
    req_signals = profile.get("required_signals", [])

    for idx, file_path in enumerate(public_files, 1):
        page_data = extract_page_primitives(file_path, root_dir=root_dir, site_url=site_url)
        html_content = page_data.get("html", "")
        clean_text = page_data.get("text", "")
        title = page_data.get("title", "")
        route = page_data.get("route", "/")
        rel_path = page_data.get("rel_path", os.path.basename(file_path))
        
        page_gsc = gsc_ingestor.get_page_metrics(file_path, page_route=route) if site_gsc["is_active"] else None
        
        evidence_map = {
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
            
        run_id = f"RUN-SITE-{uuid.uuid4().hex[:8].upper()}"
        store_run(conn, run_id, file_path, profile.get("profile_id", "generic"))
        
        for k, v in evidence_map.items():
            store_evidence(conn, run_id, k, "source_inspection", file_path, "1-end", str(v), {"value": v})
        
        evaluations = []
        for role in active_roles:
            res = role.evaluate(page_data, evidence_map)
            evaluations.append(res)
            store_evaluation(conn, run_id, res["agent_id"], res["role"], res["status"], res["score"], res["verdict"], res["observations"], res["recommendations"])
            if res["status"] == "complete":
                squad_scores[role.squad].append(res["score"])
                
        scored_evals = [e for e in evaluations if e["status"] == "complete" and e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee", "hallucination_redteam"]]
        raw_page_score = round(sum(e["score"] for e in scored_evals) / len(scored_evals), 1) if scored_evals else 0.0
        
        is_national = profile.get("target_scope") != "local" or (target_locations and not any(loc.lower() in title.lower() for loc in target_locations))
        has_tap_to_call = "tel:" in html_content if "tap_to_call" in req_signals else True
        has_ownership = ("100%" in clean_text or "ownership" in clean_text.lower()) if "ownership_or_trust_guarantee" in req_signals else True
        
        commercial_data = {
            "has_tap_to_call": has_tap_to_call,
            "has_ownership_guarantee": has_ownership
        }
        
        gate_decision = apply_hard_reality_caps(
            raw_score=raw_page_score,
            gsc_metrics=site_gsc,
            page_metrics=page_gsc,
            authority_data=authority_data,
            commercial_data=commercial_data,
            is_national_target=is_national
        )
        
        flaws = []
        recs = []
        for e in evaluations:
            for obs in e.get("observations", []):
                if obs.get("type") == "fatal_flaw":
                    flaws.append(obs["statement"])
                    flaw_key = obs["statement"].split(":")[0] if ":" in obs["statement"] else obs["statement"][:45]
                    fatal_flaws_tally[flaw_key] += 1
            for r in e.get("recommendations", []):
                recs.append(r)
                
        finalize_run(
            conn,
            run_id=run_id,
            raw_score=gate_decision["raw_score"],
            final_score=gate_decision["final_capped_score"],
            verdict=gate_decision["verdict"],
            summary={
                "caps": gate_decision["cap_reasons"],
                "fatal_flaws": flaws,
                "recs": recs
            }
        )
                    
        # Dynamic Cluster/Category Isolation
        if "/" in route.strip("/"):
            cat = route.strip("/").split("/")[0].title() + " Routes"
        else:
            cat = "Root & Primary Routes"
            
        category_scores[cat].append(gate_decision["final_capped_score"])
        
        results.append({
            "path": rel_path,
            "route": route,
            "public_url": page_data.get("public_url"),
            "title": title,
            "raw_score": raw_page_score,
            "final_score": gate_decision["final_capped_score"],
            "verdict": gate_decision["verdict"],
            "category": cat,
            "flaws": flaws
        })
        
        if idx % 25 == 0 or idx == total_pages:
            print(f"[{idx:>3}/{total_pages}] Route: {route:<36} | Raw: {raw_page_score:>5.1f} | Final: {gate_decision['final_capped_score']:>5.1f}/100 ({gate_decision['verdict']})")
            
    out_dir = os.path.dirname(os.path.abspath(out_file))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "=" * 92)
    print("               UNIVERSAL 62-ROLE AUDIT COMPLETE REPORT")
    print("=" * 92)
    print(f"Total Routes Audited       : {total_pages}")
    print(f"Total Role Evaluations     : {total_evals:,}")
    print(f"Grand Average Final Score  : {round(sum(r['final_score'] for r in results)/len(results), 1)} / 100")
    print("=" * 92)
    
    print("\n--- 1. ROUTE CLUSTER BREAKDOWN ---")
    print(f"{'Route Cluster':<32} | {'Pages':<6} | {'Avg Score':<10}")
    print("-" * 92)
    for cat, scores in sorted(category_scores.items()):
        print(f"{cat:<32} | {len(scores):<6} | {round(sum(scores)/len(scores), 1):<10}/100")
        
    print("\n--- 2. TOP FATAL FLAWS DETECTED ACROSS SPECIALISTS ---")
    for idx, (flaw, count) in enumerate(sorted(fatal_flaws_tally.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        print(f"  {idx}. [{count} Routes] {flaw}")
        
    print("\n" + "=" * 92)
    print(f"Full JSON report saved to: {out_file}")
    print("=" * 92 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Universal 62-Role SEO Swarm Site Audit Runner")
    parser.add_argument("--root", default=".", help="Root directory of the web codebase")
    parser.add_argument("--output", default="./site_audit_62_roles.json", help="Output JSON path")
    parser.add_argument("--profile", default="generic", help="Industry profile pack or path to profile.yaml/json")
    parser.add_argument("--gsc-dir", default=None, help="Directory containing GSC export CSVs")
    parser.add_argument("--authority-file", default=None, help="Validated authority profile JSON file")
    parser.add_argument("--serp-file", default=None, help="Competitive SERP snapshot JSON file")
    parser.add_argument("--db-path", default=None, help="Custom SQLite database path")
    args = parser.parse_args()
    
    run_universal_site_audit(args.root, args.output, args.profile, args.gsc_dir, args.authority_file, args.serp_file, args.db_path)

if __name__ == "__main__":
    main()
