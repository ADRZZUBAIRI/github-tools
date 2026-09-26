# SEO Swarm Simulator (62-Role Adversarial Intelligence Engine)

[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.2-blue.svg)](https://pypi.org/project/seo-swarm-simulator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-purple.svg)](https://www.python.org/downloads/)

> **"The Anti-Vanity SEO Swarm"**: A neutral, hardware-safe multi-agent SEO simulation engine that enforces **rigorous search performance and empirical evidence gating** (GSC clickstream verification, 28-day acquisition failure hard caps, verified competitive KD vs. DA reality, information gain utility proof, and commercial buyer friction) across **any web codebase and tech stack**.

---

## 🎯 Why Most SEO Audits Lie

Traditional SEO linters check whether `<title>`, `<h1>`, and `alt` tags exist. They award high scores to pages that are mathematically suppressed on **Page 9 of Google (Positions 60–90)** with 0 clicks for 12 months.

`seo-swarm-simulator` deploys an **adversarial multi-agent swarm architecture** across 8 functional squads that audit:
1. **Search Console Performance Reality**: Ingests Google Search Console CSV exports (`Pages.csv`, `Queries.csv`, `Chart.csv`, `Filters.csv`) and enforces hard reality caps:
   - **Missing GSC Data**: Hard-caps score at `20.0/100` (`GSC_DATA_REQUIRED`). No free passes without verified acquisition data.
   - **28-Day Acquisition Failure**: Sites with verified 28+ day datasets showing $< 500$ impressions and 0 clicks across 50+ pages are hard-capped at `10.0/100` (`CRITICAL_ACQUISITION_FAILURE`).
2. **Authority Evidence Contract**: Separates `VERIFIED` backlink profiles (with matching domain and provider metadata) from `UNKNOWN` states. Domains without verified third-party link evidence are hard-capped at `30.0/100` rather than assuming arbitrary DA numbers.
3. **Competitive KD vs. DA Reality**: Evaluates target query difficulty against domain authority using competitive SERP snapshots (`--serp-file`).
4. **Information Gain Proof**: Demands functional calculation scripts, empirical benchmark tables, or executable code demonstrations over purely narrative prose.
5. **Universal Framework & Profile Separation**: Adapts automatically to **Static HTML, PHP/Laravel, React/Next.js (`.jsx`/`.tsx`), Vue/Nuxt (`.vue`), Astro (`.astro`), and Django**, guided by configurable industry profiles (`generic`, `saas`, `local_services`, `ecommerce`).

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
• Migration & Redirects                                       • Skeptical Trade Persona (*)
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

Audit any web page, template, or entire codebase with verified GSC data and reality gating:

```bash
# 1. Single Page Generic Audit (Static HTML, React, Next.js, PHP, Astro, Vue)
seo-swarm path/to/page.tsx --preset single_page_audit

# 2. SaaS Trial & Pricing Audit
seo-swarm path/to/pricing.jsx --profile saas --preset single_page_audit

# 3. Local Service Landing Page Audit with GSC Export Directory
seo-swarm path/to/landing.html --profile local_services --gsc-dir path/to/gsc_export/

# 4. Verified Competitive Audit with Backlink Profile and SERP Snapshot
seo-swarm path/to/page.php --authority-file ./backlinks.json --serp-file ./serp.json
```

### Site-Wide Cluster and Full-Site Runners

```bash
# Multi-cluster reality audit across auto-discovered taxonomy buckets
python run_multi_cluster_audit.py --root /path/to/codebase --profile saas --gsc-dir /path/to/gsc_export

# Full-site 62-role adversarial audit across all public routes
python run_62_roles_site_audit.py --root /path/to/codebase --output ./site_audit.json --profile generic --gsc-dir /path/to/gsc_export
```

---

## 📄 Profile Configuration Example (`profile.yaml`)

```yaml
profile_id: b2b_saas
brand_name: Acme Cloud
site_url: https://acme.example.com
industry: saas
target_scope: global
target_languages:
  - en
business_model: subscriptions_demos
required_signals:
  - free_trial_or_demo
  - pricing_transparency
  - api_documentation
active_personas:
  - comparison_shopper
  - technical_buyer
  - information_gain_critic
```

---

## 📄 License

MIT License. Free to use, inspect, and modify for commercial and personal audit workflows.
