"""
Full Site-Wide 62-Role Maximum Red-Team Execution
=================================================
Runs all 62 specialized roles across EVERY public indexable page in a targeted website.
No shortcuts. Logs complete findings, score distributions, and squad-level diagnostic breakdowns.
Accepts portable --root, --output, --gsc-dir, and --authority-file arguments.
"""

import os
import sys
import glob
import re
import json
import argparse
from collections import defaultdict
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from seo_swarm.roles.roster import ALL_62_ROLES
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps
from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation

def run_full_62_role_site_audit(root_dir: str, out_file: str, gsc_dir: Optional[str] = None, authority_file: Optional[str] = None):
    if not os.path.exists(root_dir):
        print(f"[!] Error: Root directory '{root_dir}' does not exist.")
        return

    all_php = glob.glob(os.path.join(root_dir, "**", "*.php"), recursive=True)
    all_html = glob.glob(os.path.join(root_dir, "**", "*.html"), recursive=True)
    all_candidates = all_php + all_html
    
    # Filter out internal/system templates
    public_pages = [
        p.replace("\\", "/") for p in all_candidates
        if not any(x in p.replace("\\", "/") for x in [
            "/includes/", "/components/", "/scratch/", "/api/", "/db/", "/system/", "/templates/", "/vendor/", "/node_modules/"
        ])
    ]
    
    total_pages = len(public_pages)
    if total_pages == 0:
        print(f"[!] Warning: No public pages found under '{root_dir}'.")
        return

    total_evals = total_pages * len(ALL_62_ROLES)
    
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

    print("\n" + "=" * 92)
    print("      MAXIMUM 62-ROLE SITE-WIDE ADVERSARIAL RED-TEAM EXECUTION")
    print(f"      Auditing {total_pages} Public Pages x 62 Specialists = {total_evals:,} Total Evaluations")
    print(f"      Root Directory : {root_dir}")
    print(f"      GSC Ingestion  : {'Active (' + str(site_gsc['complete_days']) + ' days)' if site_gsc['is_active'] else 'Not Loaded (Scores Gated at <= 20/100)'}")
    print(f"      Authority Data : {authority_data['status']}")
    print("=" * 92 + "\n")
    
    conn = init_db()
    
    results = []
    category_scores = defaultdict(list)
    squad_scores = defaultdict(list)
    fatal_flaws_tally = defaultdict(int)
    
    clean_root = root_dir.replace("\\", "/").rstrip("/")
    
    for idx, page_path in enumerate(public_pages, 1):
        rel_path = page_path.replace(clean_root + "/", "")
        with open(page_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
            
        title_m = re.search(r'\$page_title\s*=\s*["\']([^"\']+)["\']|<title>([^<]+)</title>', html, re.IGNORECASE)
        title = (title_m.group(1) or title_m.group(2)) if title_m else os.path.basename(page_path)
        
        clean_text = re.sub(r'<[^>]+>', ' ', html)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        page_data = {
            "url": page_path,
            "title": title,
            "html": html,
            "text": clean_text
        }
        
        page_gsc = gsc_ingestor.get_page_metrics(page_path) if site_gsc["is_active"] else None
        
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
        
        run_id = f"RUN-62-{idx:04d}"
        store_run(conn, run_id, page_path, "full_red_team_all_62")
        
        evaluations = []
        for role in ALL_62_ROLES:
            res = role.evaluate(page_data, evidence_map)
            evaluations.append(res)
            if res["status"] == "complete":
                squad_scores[role.squad].append(res["score"])
            
        scored_evals = [e for e in evaluations if e["status"] == "complete" and e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee", "hallucination_redteam"]]
        raw_page_score = round(sum(e["score"] for e in scored_evals) / len(scored_evals), 1) if scored_evals else 0.0
        
        is_national = ("roofing seo" in title.lower() or "seo services" in title.lower()) and not any(c in title.lower() for c in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
        commercial_data = {"has_tap_to_call": "tel:" in html, "has_ownership_guarantee": ("100%" in clean_text or "ownership" in clean_text.lower())}
        
        gate_decision = apply_hard_reality_caps(
            raw_score=raw_page_score,
            gsc_metrics=site_gsc,
            page_metrics=page_gsc,
            authority_data=authority_data,
            commercial_data=commercial_data,
            is_national_target=is_national
        )
        
        flaws = []
        for e in evaluations:
            for obs in e.get("observations", []):
                if obs.get("type") == "fatal_flaw":
                    flaws.append(obs["statement"])
                    flaw_key = obs["statement"].split(":")[0] if ":" in obs["statement"] else obs["statement"][:45]
                    fatal_flaws_tally[flaw_key] += 1
                    
        # Categorize
        if "/local/" in rel_path:
            cat = "Local Landing Hubs"
        elif "/services/" in rel_path:
            cat = "Core Service Pages"
        elif "/blog/" in rel_path or "/resources/" in rel_path:
            cat = "Blog & Informational Content"
        elif "/tools/" in rel_path:
            cat = "Interactive Utilities & Tools"
        elif "/portfolio/" in rel_path:
            cat = "Portfolio Case Studies"
        elif "/pricing/" in rel_path:
            cat = "Pricing & Packages"
        elif "/compare/" in rel_path:
            cat = "Comparison & Alternative Guides"
        else:
            cat = "Core Brand / Umbrella Pages"
            
        category_scores[cat].append(gate_decision["final_capped_score"])
        
        results.append({
            "path": rel_path,
            "title": title,
            "raw_score": raw_page_score,
            "final_score": gate_decision["final_capped_score"],
            "verdict": gate_decision["verdict"],
            "cat": cat,
            "flaws": flaws
        })
        
        if idx % 25 == 0 or idx == total_pages:
            print(f"[{idx:>3}/{total_pages}] Audited: {rel_path:<48} | Raw: {raw_page_score:>5.1f} | Final: {gate_decision['final_capped_score']:>5.1f}/100 ({gate_decision['verdict']})")
            
    # Ensure parent directory of out_file exists
    out_dir = os.path.dirname(os.path.abspath(out_file))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "=" * 92)
    print("               62-ROLE MAXIMUM RED-TEAM AUDIT REPORT")
    print("=" * 92)
    print(f"Total Pages Audited        : {total_pages}")
    print(f"Total Role Evaluations     : {total_evals:,}")
    print(f"Grand Average Final Score  : {round(sum(r['final_score'] for r in results)/len(results), 1)} / 100")
    print("=" * 92)
    
    print("\n--- 1. CATEGORY REALITY BREAKDOWN ---")
    print(f"{'Page Category':<32} | {'Pages':<6} | {'Avg Score':<10}")
    print("-" * 92)
    for cat, scores in sorted(category_scores.items()):
        print(f"{cat:<32} | {len(scores):<6} | {round(sum(scores)/len(scores), 1):<10}/100")
        
    print("\n--- 2. TOP FATAL FLAWS DETECTED ACROSS ALL 62 SPECIALISTS ---")
    for idx, (flaw, count) in enumerate(sorted(fatal_flaws_tally.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        print(f"  {idx}. [{count} Pages] {flaw}")
        
    print("\n" + "=" * 92)
    print(f"Full JSON report saved to: {out_file}")
    print("=" * 92 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Site-wide 62-Role SEO Swarm Audit Runner")
    parser.add_argument("--root", default=r"c:\WebSmitherz\websmitherz", help="Root directory to audit")
    parser.add_argument("--output", default=r"c:\WebSmitherz\github-tools\seo-swarm-simulator\full_site_audit_62_roles.json", help="Output JSON path")
    parser.add_argument("--gsc-dir", default=None, help="Directory containing GSC export CSVs")
    parser.add_argument("--authority-file", default=None, help="Authority profile JSON file")
    args = parser.parse_args()
    
    run_full_62_role_site_audit(args.root, args.output, args.gsc_dir, args.authority_file)

if __name__ == "__main__":
    main()
