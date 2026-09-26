"""
Universal Multi-Cluster Reality Audit Runner
============================================
Runs the adversarial SEO swarm engine across key discovered route clusters in ANY web codebase:
- Automatically groups routes by root taxonomy (e.g. /docs, /pricing, /blog, /features)
- Evaluates reality caps, authority debt, SERP competition, and conversion friction
- Accepts --root, --profile, --gsc-dir, --authority-file, and --preset arguments
"""

import os
import sys
import json
import argparse
from collections import defaultdict
from typing import List, Tuple, Dict, Any, Optional

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, TASK_ACTIVATION_PRESETS
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps
from seo_swarm.config.profile import load_project_profile
from seo_swarm.adapters.codebase import extract_page_primitives, discover_public_codebase_routes
from seo_swarm.adapters.authority import validate_authority_data
from seo_swarm.adapters.serp import load_serp_snapshot

def execute_universal_cluster_audit(
    root_dir: str,
    profile_name_or_path: str = "generic",
    gsc_dir: Optional[str] = None,
    authority_file: Optional[str] = None,
    serp_file: Optional[str] = None,
    preset: str = "single_page_audit"
):
    if not os.path.exists(root_dir):
        print(f"[!] Error: Root directory '{root_dir}' does not exist.")
        return

    profile = load_project_profile(profile_name_or_path)
    site_url = profile.get("site_url", "https://example.com")
    extensions = profile.get("codebase", {}).get("extensions", [".html", ".htm", ".php", ".jsx", ".tsx", ".vue", ".astro"])
    
    public_files = discover_public_codebase_routes(root_dir, extensions=extensions)
    if not public_files:
        print(f"[!] Warning: No public files found under '{root_dir}'.")
        return

    # Select representative sample from each taxonomy cluster (up to 4 per cluster)
    cluster_buckets: Dict[str, List[str]] = defaultdict(list)
    for f in public_files:
        page_data = extract_page_primitives(f, root_dir=root_dir, site_url=site_url)
        route = page_data.get("route", "/")
        if "/" in route.strip("/"):
            cluster_name = route.strip("/").split("/")[0].title()
        else:
            cluster_name = "Core"
        cluster_buckets[cluster_name].append(f)

    sampled_files: List[Tuple[str, str]] = []
    for cluster_name, files in sorted(cluster_buckets.items()):
        for f in files[:4]:  # Take up to 4 key representative pages per cluster
            sampled_files.append((cluster_name, f))

    gsc_ingestor = GSCDataIngestor(gsc_dir, expected_site_url=site_url) if gsc_dir else GSCDataIngestor(None)
    site_gsc = gsc_ingestor.get_site_metrics()
    
    authority_data = validate_authority_data(authority_file, expected_site_url=site_url)
    serp_data = load_serp_snapshot(serp_file)

    active_roles = get_active_roles(preset, profile=profile)
    results_by_cluster = defaultdict(list)
    
    target_locations = profile.get("target_locations", [])
    req_signals = profile.get("required_signals", [])

    print("=" * 92)
    print("               UNIVERSAL MULTI-CLUSTER ADVERSARIAL REALITY AUDIT")
    print(f"  Root Dir      : {root_dir}")
    print(f"  Profile/Pack  : {profile['profile_id']} ({profile.get('industry', 'generic')})")
    print(f"  GSC Ingestion : {'Active (' + str(site_gsc['complete_days']) + ' days: ' + str(site_gsc['total_impressions']) + ' impr, ' + str(site_gsc['total_clicks']) + ' clicks)' if site_gsc['is_active'] else 'Not Loaded (Score Capped at 20/100)'}")
    print(f"  Authority     : {authority_data['status']} ({authority_data.get('referring_domains', 0)} ref domains via {authority_data.get('provider', 'none')})")
    print(f"  Preset        : [{preset.upper()}] ({len(active_roles)} active roles)")
    print(f"  Clusters Found: {len(cluster_buckets)} clusters ({len(sampled_files)} representative routes sampled)")
    print("=" * 92 + "\n")
    
    for cluster, file_path in sampled_files:
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
            
        evaluations = []
        for role in active_roles:
            res = role.evaluate(page_data, evidence_map)
            evaluations.append(res)
            
        scored_evals = [e for e in evaluations if e["status"] == "complete" and e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee", "hallucination_redteam"]]
        raw_avg = round(sum(e["score"] for e in scored_evals) / len(scored_evals), 1) if scored_evals else 0.0
        
        is_national = profile.get("target_scope") != "local" or (target_locations and not any(loc.lower() in title.lower() for loc in target_locations))
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
        
        results_by_cluster[cluster].append({
            "path": rel_path,
            "route": route,
            "title": title[:40] + "..." if len(title) > 40 else title,
            "raw_score": raw_avg,
            "final_score": gate_decision["final_capped_score"],
            "verdict": gate_decision["verdict"]
        })
        
    # Print Tabular Results by Cluster
    for cluster, rows in results_by_cluster.items():
        print(f"\n--- CLUSTER: {cluster.upper()} ---")
        print(f"{'Route':<42} | {'Raw':<5} | {'Final':<5} | {'Consensus Verdict':<32}")
        print("-" * 96)
        for r in rows:
            print(f"{r['route']:<42} | {r['raw_score']:<5.1f} | {r['final_score']:<5.1f} | {r['verdict']:<32}")
            
    print("\n" + "=" * 92 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Universal Multi-Cluster SEO Swarm Reality Audit")
    parser.add_argument("--root", default=".", help="Root directory of the web codebase")
    parser.add_argument("--profile", default="generic", help="Industry profile pack or path to profile.yaml/json")
    parser.add_argument("--gsc-dir", default=None, help="GSC export directory")
    parser.add_argument("--authority-file", default=None, help="Authority profile JSON file")
    parser.add_argument("--serp-file", default=None, help="Competitive SERP snapshot JSON file")
    parser.add_argument("--preset", default="single_page_audit", choices=list(TASK_ACTIVATION_PRESETS.keys()))
    args = parser.parse_args()
    
    execute_universal_cluster_audit(args.root, args.profile, args.gsc_dir, args.authority_file, args.serp_file, args.preset)

if __name__ == "__main__":
    main()
