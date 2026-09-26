"""
Comprehensive Multi-Page Adversarial Swarm Audit Runner
========================================================
Runs the 62-role adversarial swarm engine across key strategic pages and clusters:
- Core Services (National / Umbrella)
- Local Geo Expansion Hubs
- Technical Authority Pillar Blogs
- Interactive Tools & Calculators

Outputs summary tables, structural fatal flaws, and actionable mathematical reality caps.
"""

import os
import sys
import glob
import json
import re
import argparse
from collections import defaultdict
from typing import List, Tuple

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, TASK_ACTIVATION_PRESETS
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps
from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation

DEFAULT_KEY_PAGES: List[Tuple[str, str]] = [
    # 1. Core National / Umbrella Services
    ("Core", "index.php"),
    ("Core", "pages/services/roofing-seo.php"),
    ("Core", "pages/services/gmb-local-seo.php"),
    ("Core", "pages/services/hvac-seo.php"),
    ("Core", "pages/services/custom-software.php"),
    
    # 2. Local Texas Expansion Hubs (Striking Distance Focus)
    ("Local Geo", "pages/local/roofing-seo-tyler-tx.php"),
    ("Local Geo", "pages/local/roofing-seo-waco-tx.php"),
    ("Local Geo", "pages/local/roofing-seo-sugar-land-tx.php"),
    ("Local Geo", "pages/local/roofing-seo-the-woodlands-tx.php"),
    ("Local Geo", "pages/local/roofing-seo-katy-tx.php"),
    
    # 3. Technical Authority Pillar Blogs
    ("Pillar Blog", "pages/resources/blog/contractor-crm-webhook-integration-guide.php"),
    ("Pillar Blog", "pages/resources/blog/replace-elementor-with-custom-gutenberg-blocks.php"),
    ("Pillar Blog", "pages/resources/blog/how-to-rank-google-maps.php"),
    ("Pillar Blog", "pages/resources/seo/roofing-seo-guide.php"),
    
    # 4. Interactive Tools & Calculators
    ("Tools", "pages/tools/contractor-schema-generator.php"),
    ("Tools", "pages/tools/local-seo-grader.php"),
    ("Tools", "pages/tools/mobile-speed-cro-analyzer.php"),
]

def execute_multi_cluster_audit(root_dir: str, gsc_dir: str = None, authority_file: str = None, preset: str = "single_page_audit"):
    gsc_ingestor = GSCDataIngestor(gsc_dir) if gsc_dir else GSCDataIngestor(None)
    site_gsc = gsc_ingestor.get_site_metrics()
    
    authority_data = {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0}
    if authority_file and os.path.exists(authority_file):
        try:
            with open(authority_file, "r", encoding="utf-8") as af:
                authority_data = json.load(af)
                authority_data["status"] = "VERIFIED"
        except Exception:
            pass

    active_roles = get_active_roles(preset)
    results_by_cluster = defaultdict(list)
    overall_flaws = []
    
    print("=" * 90)
    print("               SITE-WIDE ADVERSARIAL REALITY CLUSTER AUDIT")
    print(f"  Root Dir      : {root_dir}")
    print(f"  GSC Ingestion : {'Active (' + str(site_gsc['complete_days']) + ' days: ' + str(site_gsc['total_impressions']) + ' impr, ' + str(site_gsc['total_clicks']) + ' clicks)' if site_gsc['is_active'] else 'Not Loaded (Score Capped at 20/100)'}")
    print(f"  Authority     : {authority_data['status']}")
    print(f"  Task Preset   : [{preset.upper()}] ({len(active_roles)} active roles)")
    print("=" * 90 + "\n")
    
    for cluster, rel_path in DEFAULT_KEY_PAGES:
        file_path = os.path.join(root_dir, rel_path)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
            
        title_m = re.search(r'\$page_title\s*=\s*["\']([^"\']+)["\']|<title>([^<]+)</title>', html, re.IGNORECASE)
        title = (title_m.group(1) or title_m.group(2)) if title_m else os.path.basename(file_path)
        
        clean_text = re.sub(r'<[^>]+>', ' ', html)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        page_data = {
            "url": file_path,
            "title": title,
            "html": html,
            "text": clean_text
        }
        
        page_gsc = gsc_ingestor.get_page_metrics(file_path) if site_gsc["is_active"] else None
        evidence_map = {
            "EVD-TITLE": title,
            "EVD-SCHEMA": "application/ld+json" in html,
            "EVD-TEL": "tel:" in html,
            "EVD-SECTIONS": str(len(re.findall(r'<section\b', html, re.IGNORECASE))),
            "EVD-AUTHORITY": authority_data
        }
        if site_gsc["is_active"]:
            evidence_map["EVD-GSC-SITE"] = site_gsc
        if page_gsc:
            evidence_map["EVD-GSC-PAGE"] = page_gsc
            
        evaluations = []
        for role in active_roles:
            res = role.evaluate(page_data, evidence_map)
            evaluations.append(res)
            
        scored_evals = [e for e in evaluations if e["status"] == "complete" and e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee", "hallucination_redteam"]]
        raw_avg = round(sum(e["score"] for e in scored_evals) / len(scored_evals), 1) if scored_evals else 0.0
        
        is_national = ("roofing seo" in title.lower() or "seo services" in title.lower()) and not any(c in title.lower() for c in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
        commercial_data = {"has_tap_to_call": "tel:" in html, "has_ownership_guarantee": ("100%" in clean_text or "ownership" in clean_text.lower())}
        
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
            "title": title[:42] + "..." if len(title) > 42 else title,
            "raw_score": raw_avg,
            "final_score": gate_decision["final_capped_score"],
            "verdict": gate_decision["verdict"]
        })
        
    # Print Tabular Results by Cluster
    for cluster, rows in results_by_cluster.items():
        print(f"\n--- CLUSTER: {cluster.upper()} ---")
        print(f"{'Page Route':<45} | {'Raw':<5} | {'Final':<5} | {'Consensus Verdict':<32}")
        print("-" * 96)
        for r in rows:
            print(f"{r['path']:<45} | {r['raw_score']:<5.1f} | {r['final_score']:<5.1f} | {r['verdict']:<32}")
            
    print("\n" + "=" * 90 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Run Multi-Cluster SEO Swarm Reality Audit")
    parser.add_argument("--root", default=r"c:\WebSmitherz\websmitherz", help="Root directory of the website")
    parser.add_argument("--gsc-dir", default=None, help="GSC export directory")
    parser.add_argument("--authority-file", default=None, help="Authority profile JSON")
    parser.add_argument("--preset", default="single_page_audit", choices=list(TASK_ACTIVATION_PRESETS.keys()))
    args = parser.parse_args()
    
    execute_multi_cluster_audit(args.root, args.gsc_dir, args.authority_file, args.preset)

if __name__ == "__main__":
    main()
