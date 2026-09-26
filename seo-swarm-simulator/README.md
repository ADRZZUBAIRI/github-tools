# SEO Swarm Simulator (62-Role Adversarial Intelligence Engine)

[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.1-blue.svg)](https://pypi.org/project/seo-swarm-simulator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-purple.svg)](https://www.python.org/downloads/)
[![Maintained by WebSmitherz](https://img.shields.io/badge/Maintained%20by-WebSmitherz-orange.svg)](https://websmitherz.com)

> **"The Anti-Vanity SEO Engine"**: While traditional SEO linters award empty 95/100 scores for basic tag presence, `seo-swarm-simulator` enforces **rigorous search performance and empirical evidence gating** (GSC clickstream verification, 28-day acquisition failure hard caps, information gain utility requirements, unverified authority gating, and commercial buyer friction).

---

## 🎯 Why Most SEO Audits Lie

Traditional SEO linters check whether `<title>`, `<h1>`, and `alt` tags exist. They award high scores to pages that are mathematically suppressed on **Page 9 of Google (Positions 60–90)** with 0 clicks for 12 months.

`seo-swarm-simulator` deploys an **adversarial multi-agent swarm architecture** across 8 functional squads that audit:
1. **Search Console Performance Reality**: Ingests Google Search Console CSV exports (`Pages.csv`, `Queries.csv`, `Chart.csv`, `Filters.csv`) and enforces hard reality caps:
   - **Missing GSC Data**: Hard-caps score at `20.0/100` (`GSC_DATA_REQUIRED`). No free passes without verified acquisition data.
   - **28-Day Acquisition Failure**: Sites with verified 28+ day datasets showing $< 500$ impressions and 0 clicks across 50+ pages are hard-capped at `10.0/100` (`CRITICAL_ACQUISITION_FAILURE`).
2. **Authority Evidence Contract**: Separates `VERIFIED` backlink profiles from `UNKNOWN` states. Domains without verified third-party link evidence are hard-capped at `30.0/100` rather than assuming arbitrary DA numbers.
3. **Information Gain Patent**: Demands proprietary calculation tools and empirical telemetry over derivative textbook definitions.
4. **Commercial Buyer Skepticism**: Simulates trade business decision-makers testing for 1-tap `tel:` phone actions and explicit 100% asset ownership guarantees.
5. **Zero Vanity Inflation**: Unimplemented roles are explicitly reported as `not_implemented` (score: 0.0) and excluded from scoring averages.

---

## 🏛️ The 62-Role Master Squad Architecture

```
========================================================================================
                              62-ROLE ADVERSARIAL SQUADS
========================================================================================
[A. Command & Decision (5)]     [B. Search Data (8)]          [C. Keyword & SERP (8)]
• SEO Swarm Chief (*)           • GSC Analytics Analyst (*)   • Keyword Universe Researcher
• Research Question Architect   • GA4 Conversion Analyst      • SERP Difficulty & Realist (*)
• Evidence Librarian (*)        • Server Log Crawl Analyst    • SERP Feature Analyst
• Portfolio Prioritizer (*)     • SEO Data Engineer           • Search Intent Classifier
• Chief Referee (Gatekeeper)    • Stats Experiment Scientist  • Query Cluster Architect
                                • Trend & Seasonality         • Competitor Content Analyst
                                • Attribution & Incrementality• Competitive Gap Strategist
                                • Measurement QA              • Entity & Knowledge Graph

[D. Technical SEO (13)]         [E. Content Quality (9)]      [F. Off-Page Authority (6)]
• Crawl & Index Guardian (*)    • Content Strategy Director   • Off-Page & Backlinks (*)
• Technical SEO Auditor (*)     • Information Gain Critic (*) • Digital PR & Outreach
• JavaScript & Rendering (*)    • Original Data Journalist    • Brand, Entity & Reputation
• Internal Link Architect (*)   • E-E-A-T & Fact Checker      • Local Citation & Reviews
• Core Web Vitals Engineer (*)  • Content Decay Editor        • Link Risk & Spam Auditor
• Schema & Structured Data (*)  • SERP Snippet Copywriter (*) • Proof Acquisition Manager
• International & Hreflang      • Semantic Coverage Analyst   
• Local SEO Tech Specialist (*) • Localization Editor         [G. Conversion & Buyers (7)]
• Ecommerce Faceted Nav         • Multimedia Producer         • Voice-of-Customer Analyst
• Migration & Redirects                                       • Skeptical Contractor (*)
• CMS Code Architect (*)                                      • Mobile-First Customer (*)
• Multimedia Search                                           • Comparison Shopper
• Security & Privacy SEO                                      • UX & CRO Funnel Analyst (*)
                                                              • Sales & Lead Analyst
[H. Implementation & Red-Team (6)]                            • Offer & Pricing Strategist
• Developer & Maintainer (*)
• Release Manager
• Spam Policy Red-Team
• Hallucination Red-Team (*)
• Negative SEO Reviewer
• Rollback & Resilience Reviewer
========================================================================================
(*) = Active Evaluators in Core Task Presets
```

---

## 🚀 Quickstart & Installation

Install the package directly via pip:

```bash
pip install seo-swarm-simulator
```

Or clone the repository:

```bash
git clone https://github.com/ADRZZUBAIRI/github-tools.git
cd github-tools/seo-swarm-simulator
pip install -e .
```

---

## 💻 CLI Usage

Audit local PHP templates, HTML files, or entire site repositories with verified GSC data and reality gating:

```bash
# 1. Single Page Audit without GSC (Correctly capped at 20/100 GSC_DATA_REQUIRED)
seo-swarm path/to/page.php --preset single_page_audit

# 2. Single Page Audit with Verified 28-Day GSC Export Directory
seo-swarm path/to/page.php --preset single_page_audit --gsc-dir path/to/gsc_export/

# 3. Local Contractor Landing Page Audit
seo-swarm path/to/local-roofing-page.php --preset local_roofing_audit --gsc-dir path/to/gsc_export/

# 4. Full Technical Architecture Audit
seo-swarm path/to/index.php --preset full_technical_audit

# 5. Full 62-Role Squad Audit
seo-swarm path/to/page.php --preset full_red_team_all_62 --gsc-dir path/to/gsc_export/
```

### Site-Wide Cluster and Full-Site Runners

```bash
# Multi-cluster reality audit across Core, Local, Blog, and Tools
python run_multi_cluster_audit.py --root /path/to/site --gsc-dir /path/to/gsc_export

# Full-site 62-role adversarial audit across all public pages
python run_62_roles_site_audit.py --root /path/to/site --output ./full_site_audit.json --gsc-dir /path/to/gsc_export
```

---

## 📊 Sample Output (The Brutal Truth)

```
########################################################################################
                    62-ROLE ADVERSARIAL SEO SWARM ENGINE
                  Task Preset: [SINGLE_PAGE_AUDIT] (19 Active Specialists)
########################################################################################
 Target File  : pages/services/roofing-seo.php
 GSC Ingestion: Active (7 days: 488 impr, 1 clicks across 186 pages)
 Authority    : UNKNOWN (0 ref domains)
 Run ID       : RUN-A78C1E44 | Mode: Uninflated Reality Execution
########################################################################################

[FAIL] [C. Keyword/SERP] SERP Difficulty & Realist Competitor Analyst (Score: 15.0/100) -> HIGH_NATIONAL_KD_RISK
   |-- [FATAL] UNVERIFIED SERP: Page title targets highly saturated national query. High probability of Page 9 suppression without substantial DA.

[PASS] [G. Conversion] Skeptical Commercial Contractor Persona (Score: 85.0/100) -> CONTRACTOR_TRUST_EARNED
   |-- [OBS] Contractor conversion criteria satisfied (1-tap call & ownership).

[FAIL] [E. Content] Information Gain & Original Data Critic (Score: 25.0/100) -> DERIVATIVE_CONTENT_RISK
   |-- [FATAL] LOW INFORMATION GAIN: Content contains mainly static descriptive text without proprietary calculators or verified empirical datasets.

[WARN] [F. Authority] Off-Page Authority & Entity Backlink Auditor -> INSUFFICIENT_EVIDENCE (AUTHORITY_DATA_UNVERIFIED)
   |-- [MISSING DATA] No external backlink dataset (Ahrefs/Moz/GSC links) loaded. Authority status is UNKNOWN.

========================================================================================
                      CHIEF REFEREE SYNTHESIZED DECISION
========================================================================================
 Raw Heuristic Score     : 56.4 / 100
 Final Capped Score      : 20.0 / 100
 Decision Verdict        : GSC_DATA_REQUIRED / SHORT_WINDOW_RESTRICTED
 Scored Specialists      : 10 evaluated (of 19 active in preset)

[!] HARD REALITY CAPS APPLIED BY CHIEF REFEREE:
   * [CAP 20.0/100] GSC SHORT-WINDOW WARNING (7 days): 488 impressions and 1 click recorded. Insufficient full 28-day baseline; capped at 20.0/100.
   * [CAP 30.0/100] UNVERIFIED AUTHORITY GATE: No backlink dataset/API configured. Domain authority status is UNKNOWN. Score hard-capped at 30.0/100.

[!] FATAL STRUCTURAL FLAWS EXPOSED:
   1. UNVERIFIED SERP: Page title targets highly saturated national query. High probability of Page 9 suppression without substantial DA.
   2. LOW INFORMATION GAIN: Content contains mainly static descriptive text without proprietary calculators or verified empirical datasets.

[+] MANDATORY RESCUE ACTIONS:
   * [CRITICAL] Embed Interactive Utility: Replace static copy with interactive estimate or loss calculators.
   * [CRITICAL] Target Local Intent or Integration Hub: Narrow targeting to geo-modifiers or exact CRM webhook solutions.
========================================================================================
```

---

## 🛠️ Resources & Engineering Hub

Maintained by [WebSmitherz Systems Engineering](https://websmitherz.com).
- [Free Contractor Schema Generator](https://websmitherz.com/tools/contractor-schema-generator)
- [Roofing SEO & Web Design Systems](https://websmitherz.com/services/roofing-seo)
- [Local Google Business Profile SEO Engine](https://websmitherz.com/services/gmb-local-seo)

---

## 📄 License

MIT License. Free to use, inspect, and modify for commercial and personal audit workflows.
