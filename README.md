# Free Google Maps Lead Scraper & Contractor Intelligence Engine

> High-speed, unblockable Google Maps local business scraper with deep website email crawling, mobile phone extraction, and automated lead enrichment. 100% Free & Open Source.

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776ab.svg)](https://python.org)
[![Engineered by WebSmitherz](https://img.shields.io/badge/Maintained_By-WebSmitherz-673de6.svg)](https://websmitherz.com)
[![Free Contractor Schema Generator](https://img.shields.io/badge/Live_Tool-Contractor_Schema_Generator-10b981.svg)](https://websmitherz.com/tools/contractor-schema-generator)

---

## The Problem: Paid Scrapers Are Expensive & Blocked Easily
Traditional scrapers cost $50–$300/month (Apify, Outscraper, PhantomBuster) and get IP blocked by Google Maps bot detection after 50 queries.

This engine uses **headless browser automation with asset-blocking** paired with **50 concurrent asynchronous aiohttp workers** to scrape and enrich hundreds of contractor leads across major cities in under 4 minutes with $0 in proxy or API costs.

---

## Key Features

1. **Turbo Asset-Blocked Playwright Scraper**:
   - Disables images, stylesheets, media, and third-party trackers during Google Maps scrolling for 10x faster scraping and zero bandwidth waste.
   - Extracts business name, verified Google Maps rating, total review count, category/niche, full address, and primary website URL.

2. **Multi-Vector Deep Email Extraction (`aiohttp` Async)**:
   - Crawls high-probability internal routes (`/`, `/contact`, `/about`, `/team`, `/terms`, `/privacy`, `/estimate`).
   - Decodes obfuscated JavaScript mailto links and extracts public contact emails with zero external API dependencies.

3. **E.164 Clean Phone Normalization**:
   - Strips vanity extensions, validates 10-digit US numbers, and formats for 1-tap mobile calling and CRM auto-dialers.

4. **Zero Cost & Open Source**:
   - No credits, no subscriptions, no paid rotating proxy networks required.

---

## Quick Start (Installation & Execution)

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/ADRZZUBAIRI/free-gmaps-lead-scraper.git
cd free-gmaps-lead-scraper
pip install -r requirements.txt
playwright install chromium
```

`requirements.txt`:
```text
playwright>=1.40.0
aiohttp>=3.9.0
beautifulsoup4>=4.12.0
```

### 2. Run the Scraper Across Target Cities

```bash
python free_gmaps_lead_scraper.py
```

The script will automatically crawl configured metro markets (Dallas, Fort Worth, Austin, Houston, San Antonio, Lubbock, Brownsville, Augusta, etc.) and export enriched leads to `texas_contractor_leads_master.csv`.

---

## Output CSV Schema

| Column Name | Description | Example |
| :--- | :--- | :--- |
| `business_name` | Full verified business name | Apex Roofing & Restoration |
| `phone` | Direct contact number | 214-555-0199 |
| `email` | Deep-crawled business email | contact@apexroofingtx.com |
| `website` | Canonical company URL | https://apexroofingtx.com |
| `address` | Google Maps physical address | 1440 Main St, Dallas, TX 75201 |
| `city` | Target market city | Dallas |
| `state` | State code | TX |
| `rating` | Google review star rating | 4.9 |
| `reviews` | Total verified Google reviews | 142 |
| `niche` | Trade classification | Roofing contractor |

---

## 🏗️ Commercial Use Cases & Business Integration

While this scraper is 100% free and open-source, local contractors and service businesses use the underlying architecture for high-ticket growth:

| Operational Bottleneck | Technical Solution | Direct Engineering Hub |
| :--- | :--- | :--- |
| **Low Google Maps 3-Pack Visibility** | Specialized LocalBusiness & Service JSON-LD Schema | [Contractor Schema Generator](https://websmitherz.com/tools/contractor-schema-generator) |
| **High Mobile Bounce Rates (>70%)** | Hand-coded Sub-0.8s Website Architecture | [Roofing SEO & Architecture Playbook](https://websmitherz.com/resources/seo/roofing-seo-guide) |
| **Slow Lead Response Times (>15 min)** | Instant SMS Lead Routing & Webhook Middleware | [Custom Software & CRM Middleware](https://websmitherz.com/services/custom-software) |
| **Google Maps 3-Pack Radius Collapse** | Multi-City Geo-Grid Optimization & Local Citations | [GMB & Local SEO Growth Engine](https://websmitherz.com/services/gmb-local-seo) |

---

## 🛠️ Related Contractor Intelligence & SEO Tools

- **[WebSmitherz Open-Source Contractor Schema Generator](https://websmitherz.com/tools/contractor-schema-generator)**: Generate valid Google Maps 3-Pack and LocalBusiness JSON-LD markup for Roofing, HVAC, and Home Service websites.
- **[Contractor 1-Tap Call Widget](https://websmitherz.com/resources/seo/roofing-seo-guide)**: Plug-and-play mobile call button with automatic Schema.org injection.
- **[WebSmitherz Systems Engineering & CRM Hub](https://websmitherz.com)**: Sub-0.8s mobile architecture blueprints and automated lead routing middleware.
- **[Contractor Web Design & SEO Services](https://websmitherz.com/services/roofing-seo)**: Full-stack custom websites and local search rankings for residential and commercial contractors.

---

## 📜 License

MIT License © 2026 [WebSmitherz Digital Agency](https://websmitherz.com) & [Abdul Rehman Zubairi](https://abdulrehmanz.com).

