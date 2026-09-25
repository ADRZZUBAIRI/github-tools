"""
Full Site-Wide 62-Role Maximum Red-Team Execution
=================================================
Runs all 62 specialized roles across EVERY public indexable page in WebSmitherz.
No shortcuts. 62 evaluations per page x 200+ pages = 12,400+ agent evaluations.
Logs complete findings, score distributions, and squad-level diagnostic breakdowns.
"""

import os
import sys
import glob
import re
import json
from collections import defaultdict

# Add src to path
sys.path.insert(0, os.path.abspath("src"))

from seo_swarm.roles.roster import ALL_62_ROLES, ChiefRefereeRole
from seo_swarm.store.database import init_db, store_run, store_evidence, store_evaluation

def run_full_62_role_site_audit():
    root_dir = "c:/WebSmitherz/websmitherz"
    all_php = glob.glob(os.path.join(root_dir, "**", "*.php"), recursive=True)
    
    # Filter out internal/system templates
    public_pages = [
        p.replace("\\", "/") for p in all_php
        if not any(x in p.replace("\\", "/") for x in [
            "/includes/", "/components/", "/scratch/", "/api/", "/db/", "/system/", "/templates/"
        ])
    ]
    
    total_pages = len(public_pages)
    total_evals = total_pages * len(ALL_62_ROLES)
    
    print("\n" + "=" * 92)
    print("      MAXIMUM 62-ROLE SITE-WIDE ADVERSARIAL RED-TEAM EXECUTION")
    print(f"      Auditing {total_pages} Public Pages x 62 Specialists = {total_evals:,} Total Evaluations")
    print("=" * 92 + "\n")
    
    conn = init_db()
    referee = ChiefRefereeRole()
    
    results = []
    category_scores = defaultdict(list)
    squad_scores = defaultdict(list)
    fatal_flaws_tally = defaultdict(int)
    
    for idx, page_path in enumerate(public_pages, 1):
        rel_path = page_path.replace(root_dir + "/", "")
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
        
        evidence_map = {
            "EVD-TITLE": title,
            "EVD-SCHEMA": "application/ld+json" in html,
            "EVD-TEL": "tel:" in html,
            "EVD-SECTIONS": str(len(re.findall(r'<section\b', html, re.IGNORECASE)))
        }
        
        run_id = f"RUN-62-{idx:04d}"
        store_run(conn, run_id, page_path, "full_red_team_all_62")
        
        evaluations = []
        for role in ALL_62_ROLES:
            res = role.evaluate(page_data, evidence_map)
            evaluations.append(res)
            squad_scores[role.squad].append(res["score"])
            
        # Chief Referee consensus calculation
        referee_evals = [e for e in evaluations if e["agent_id"] not in ["swarm_chief", "evidence_librarian", "portfolio_prioritizer", "chief_referee"]]
        page_score = round(sum(e["score"] for e in referee_evals) / len(referee_evals), 1)
        
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
            
        category_scores[cat].append(page_score)
        
        results.append({
            "path": rel_path,
            "title": title,
            "score": page_score,
            "cat": cat,
            "flaws": flaws
        })
        
        if idx % 25 == 0 or idx == total_pages:
            print(f"[{idx:>3}/{total_pages}] Audited: {rel_path:<48} | Score: {page_score:>5.1f}/100")
            
    # Save full 62-role audit output
    out_file = "c:/WebSmitherz/github-tools/seo-swarm-simulator/full_site_audit_62_roles.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "=" * 92)
    print("               62-ROLE MAXIMUM RED-TEAM AUDIT REPORT")
    print("=" * 92)
    print(f"Total Pages Audited        : {total_pages}")
    print(f"Total Role Evaluations     : {total_evals:,}")
    print(f"Grand Average Site Score   : {round(sum(r['score'] for r in results)/len(results), 1)} / 100")
    print("=" * 92)
    
    print("\n--- 1. SQUAD-BY-SQUAD PERFORMANCE BREAKDOWN ---")
    print(f"{'Squad Name':<32} | {'Evaluations':<11} | {'Avg Score':<10}")
    print("-" * 92)
    for squad, scores in sorted(squad_scores.items()):
        print(f"{squad:<32} | {len(scores):<11} | {round(sum(scores)/len(scores), 1):<10}/100")
        
    print("\n--- 2. CATEGORY REALITY BREAKDOWN ---")
    print(f"{'Page Category':<32} | {'Pages':<6} | {'Avg Score':<10}")
    print("-" * 92)
    for cat, scores in sorted(category_scores.items()):
        print(f"{cat:<32} | {len(scores):<6} | {round(sum(scores)/len(scores), 1):<10}/100")
        
    print("\n--- 3. TOP FATAL FLAWS DETECTED ACROSS ALL 62 SPECIALISTS ---")
    for idx, (flaw, count) in enumerate(sorted(fatal_flaws_tally.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        print(f"  {idx}. [{count} Pages] {flaw}")
        
    print("\n" + "=" * 92)
    print(f"Full JSON report saved to: {out_file}")
    print("=" * 92 + "\n")

if __name__ == "__main__":
    run_full_62_role_site_audit()
