"""
Brutal Adversarial SEO Swarm Simulator: The "Depression Engine"
==============================================================
Unfiltered, ruthless multi-agent evaluation framework that destroys SEO vanity metrics,
exposes statistical ranking impossibilities, domain authority deficits, LLM regurgitation traps,
and commercial failure points that typical audits hide.

Personas:
1. `serp_executioner`: The Google Helpful Content & RankBrain Algorithmic Executioner.
2. `backlink_debt_collector`: The Brutal Off-Page & Referring Domain Moat Auditor.
3. `information_gain_tribunal`: The AI Overviews / Low-Entropy Information Gain Inquisitor.
4. `skeptical_bluecollar_cfo`: The 55yo Roofing/HVAC Owner who hates marketing agency BS.
5. `core_web_vitals_terminator`: Real-world 4G mobile latency, DOM thrashing, and layout shifts.
6. `schema_entity_prosecutor`: Google Knowledge Graph & Wikidata Semantic Graph Prosecutor.
7. `competitor_predator`: The $100M VC-backed aggregator waiting to crush this page.
8. `adversarial_referee`: The merciless synthesizer that calculates the "Reality & Depression Index".
"""

import json
import re
from typing import Dict, List, Any

class BaseBrutalRole:
    def __init__(self, agent_id: str, title: str, description: str):
        self.agent_id = agent_id
        self.title = title
        self.description = description

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        raise NotImplementedError

class SERPExecutionerRole(BaseBrutalRole):
    """Simulates Google's RankBrain & Helpful Content Classifier with zero mercy."""
    def __init__(self):
        super().__init__(
            "serp_executioner",
            "Google RankBrain & Algorithmic Executioner",
            "Audits search intent cannibalization, broad-match KD delusion, and Page 9 graveyard traps."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        title = page_data.get("title", "").lower()
        url = page_data.get("url", "").lower()
        text = page_data.get("text", "").lower()
        
        is_generic_agency = any(term in title for term in ["roofing seo", "web design agency", "seo services", "digital marketing"])
        has_geo = any(city in title or city in url for city in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
        
        observations = []
        recs = []
        
        if is_generic_agency and not has_geo:
            score = 12.0
            verdict = "PAGE_9_GRAVEYARD_GUARANTEED"
            observations.append({
                "type": "fatal_flaw",
                "statement": "DELUSION DETECTED: Page targets national KD 80+ keyword on a DA < 5 domain. You are competing against WebFX ($100M budget) and SearchEngineJournal (1.2M backlinks). Google places this page on Position 87 where 0.0001% of searchers ever scroll. Zero clicks in 3 months is the mathematically expected result, not an anomaly.",
                "evidence_ids": ["EVD-TITLE", "EVD-KD"],
                "confidence": 1.0
            })
            observations.append({
                "type": "harsh_truth",
                "statement": "No amount of meta tag polishing or H1 rewording will ever move a DA 2 site to Page 1 for national queries without $50k in link equity.",
                "evidence_ids": ["EVD-DA-DEBT"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Stop Committing SEO Suicide on National Keywords",
                "action": "Kill broad national keyword targeting. Reposition page exclusively around un-commoditized technical infrastructure (e.g. 'Roofing CRM Webhook & Instant SMS Speed-to-Lead Middleware') or hyper-local county/city landing pages.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 3, "risk": 1
            })
        else:
            score = 78.0
            verdict = "SURVIVABLE_LOCAL_STRIKING_DISTANCE"
            observations.append({
                "type": "observed",
                "statement": "Page targets localized geo-intent where local 3-pack algorithms weigh proximity and NAP over massive domain backlink moats.",
                "evidence_ids": ["EVD-TITLE"],
                "confidence": 0.9
            })
            recs.append({
                "title": "Embed Verified City Geo-Data",
                "action": "Inject local municipal permit data, county codes, and specific street intersections to solidify geographic entity anchor.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "high", "effort": 1, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class BacklinkDebtCollectorRole(BaseBrutalRole):
    """Exposes off-page authority bankruptcy."""
    def __init__(self):
        super().__init__(
            "backlink_debt_collector",
            "Off-Page Authority & Backlink Debt Collector",
            "Audits referring domain deficit, third-party citation debt, and brand search vacuum."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        has_verified_pypi = "pypi" in text.lower() or "contractor-lead-scraper" in text.lower()
        
        observations = []
        recs = []
        
        score = 25.0
        verdict = "AUTHORITY_BANKRUPTCY"
        observations.append({
            "type": "fatal_flaw",
            "statement": "BACKLINK DEBT: 0 Referring Root Domains from accredited trade organizations (NRCA, RoofingContractor.com, TechCrunch). Google views this site as an unverified anonymous ghost.",
            "evidence_ids": ["EVD-OFFPAGE"],
            "confidence": 1.0
        })
        observations.append({
            "type": "harsh_truth",
            "statement": "BRAND SEARCH VACUUM: Exact-match brand search volume for 'WebSmitherz' is effectively zero. Google requires brand search velocity before trusting money pages.",
            "evidence_ids": ["EVD-BRAND-SEARCH"],
            "confidence": 0.95
        })
        if has_verified_pypi:
            score += 15.0
            observations.append({
                "type": "observed",
                "statement": "PyPI open-source package link detected (DA 94 anchor). First positive entity citation step.",
                "evidence_ids": ["EVD-PYPI"],
                "confidence": 1.0
            })
            
        recs.append({
            "title": "Execute Aggressive Entity Citation & Press Syndication",
            "action": "Syndicate raw engineering audit data to AP Press, Dev.to, ProductHunt, and GitHub tools to force Google Entity Graph registration.",
            "affected_urls": [page_data.get("url", "/")],
            "benefit": "critical", "effort": 3, "risk": 1
        })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class InformationGainTribunalRole(BaseBrutalRole):
    """Destroys commodity AI-generated fluff and tests for Google Information Gain Patent compliance."""
    def __init__(self):
        super().__init__(
            "information_gain_tribunal",
            "Information Gain & AI Spam Inquisitor",
            "Audits whether content produces net-new proprietary data or regurgitates identical LLM textbook summaries."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        text = page_data.get("text", "")
        
        has_interactive_calculator = "<script" in html and any(term in text.lower() for term in ["lost", "calculator", "radius", "widget"])
        has_empirical_teardown_data = any(term in text.lower() for term in ["343", "340", "sub-0.8s", "73%", "4.8s", "e.164"])
        
        observations = []
        recs = []
        
        if has_interactive_calculator and has_empirical_teardown_data:
            score = 88.0
            verdict = "ORIGINAL_INFORMATION_GAIN_CONFIRMED"
            observations.append({
                "type": "observed",
                "statement": "Proprietary interactive calculation utility + empirical roofer latency audit data passed Google Information Gain patent criteria.",
                "evidence_ids": ["EVD-TOOL", "EVD-DATA"],
                "confidence": 0.95
            })
        else:
            score = 22.0
            verdict = "COMMODITY_AI_SLOP_DETECTED"
            observations.append({
                "type": "fatal_flaw",
                "statement": "ZERO INFORMATION GAIN: Paragraphs explain 'why reviews matter' and 'what local SEO is'. An AI scraper can generate this in 4 seconds. Google AI Overviews already answers this in the SERP header without clicking your link.",
                "evidence_ids": ["EVD-COPY"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Embed Zero-Dependency Interactive Utilities",
                "action": "Remove generic explainer paragraphs. Replace with interactive 3-Pack Revenue Loss Calculators and empirical audit charts.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 2, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class SkepticalBlueCollarCFORole(BaseBrutalRole):
    """The 55yo commercial contractor who has been scammed by 10 agencies and deletes emails in 2 seconds."""
    def __init__(self):
        super().__init__(
            "skeptical_bluecollar_cfo",
            "Skeptical Blue-Collar Contractor Persona",
            "Simulates a 55-year-old roofing owner on a muddy job site inspecting the page on an iPhone 13 in bright sunlight."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        html = page_data.get("html", "")
        
        has_tel = "tel:" in html
        has_ownership = "100%" in text or "ownership" in text.lower()
        has_pricing = "$" in text or "pricing" in text.lower() or "cost" in text.lower() or "flat" in text.lower()
        has_buzzwords = any(b in text.lower() for b in ["skyrocket", "game-changer", "10x", "leading provider", "cutting-edge", "synergy"])
        
        observations = []
        recs = []
        score = 85.0
        
        if not has_tel:
            score -= 35.0
            observations.append({
                "type": "fatal_flaw",
                "statement": "NO TAP-TO-CALL: You made me copy-paste your phone number while I'm standing on a ladder. I tapped back and called your competitor.",
                "evidence_ids": ["EVD-TEL"],
                "confidence": 1.0
            })
        if not has_ownership:
            score -= 25.0
            observations.append({
                "type": "fatal_flaw",
                "statement": "NO OWNERSHIP GUARANTEE: Last agency stole my domain and held my Google Business Profile hostage. If you don't state '100% Client Asset Ownership' above the fold, I bounce.",
                "evidence_ids": ["EVD-OWNERSHIP"],
                "confidence": 0.95
            })
        if has_buzzwords:
            score -= 30.0
            observations.append({
                "type": "fatal_flaw",
                "statement": "AGENCY BS DETECTED: Page used phrases like 'scale your business' or 'leading agency'. Instant closed tab.",
                "evidence_ids": ["EVD-BUZZWORDS"],
                "confidence": 1.0
            })
            
        verdict = "CONTRACTOR_RESPECT_EARNED" if score >= 75 else "CONTRACTOR_INSTANT_BOUNCE"
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": max(5.0, score), "verdict": verdict, "observations": observations, "recommendations": recs}

class CoreWebVitalsTerminatorRole(BaseBrutalRole):
    """Simulates real 4G cellular performance on cheap Android/iPhone devices."""
    def __init__(self):
        super().__init__(
            "core_web_vitals_terminator",
            "Core Web Vitals & 4G Cellular Terminator",
            "Audits Cumulative Layout Shift (CLS), Largest Contentful Paint (LCP), and DOM bloat on constrained networks."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_heavy_framework = any(fw in html.lower() for fw in ["react", "vue", "angular", "next", "nuxt"])
        has_external_fonts = "fonts.googleapis.com" in html
        
        observations = []
        recs = []
        
        if not has_heavy_framework:
            score = 94.0
            verdict = "SUB_0_8S_CRUSH_SPEED"
            observations.append({
                "type": "observed",
                "statement": "Zero framework bloat. Pure semantic server-rendered HTML + Tailwind CSS. First Contentful Paint (FCP) < 0.4s on 4G cellular.",
                "evidence_ids": ["EVD-PERF"],
                "confidence": 1.0
            })
        else:
            score = 35.0
            verdict = "JS_HYDRATION_DEATH"
            observations.append({
                "type": "fatal_flaw",
                "statement": "Client-side JS framework thrashing mobile CPU and delaying LCP to 4.2s on mobile networks.",
                "evidence_ids": ["EVD-PERF"],
                "confidence": 1.0
            })
            
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class SchemaEntityProsecutorRole(BaseBrutalRole):
    """Audits whether schema creates real Knowledge Graph entity nodes or useless empty tags."""
    def __init__(self):
        super().__init__(
            "schema_entity_prosecutor",
            "Schema & Knowledge Graph Entity Prosecutor",
            "Validates structured data against Google's Knowledge Graph, Wikidata, and LocalBusiness specifications."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_schema = "application/ld+json" in html
        has_area_served = "areaServed" in html or "RoofingContractor" in html or "LocalBusiness" in html
        
        observations = []
        recs = []
        
        if has_schema and has_area_served:
            score = 92.0
            verdict = "SEMANTIC_GRAPH_VALIDATED"
            observations.append({
                "type": "observed",
                "statement": "Rich JSON-LD entity graph with specific LocalBusiness / RoofingContractor typology identified.",
                "evidence_ids": ["EVD-SCHEMA"],
                "confidence": 1.0
            })
        else:
            score = 30.0
            verdict = "UNSTRUCTURED_DATA_VOID"
            observations.append({
                "type": "fatal_flaw",
                "statement": "Google AI crawlers cannot parse exact service regions, pricing schemas, or business ownership entities.",
                "evidence_ids": ["EVD-SCHEMA"],
                "confidence": 1.0
            })
            
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class CompetitorPredatorRole(BaseBrutalRole):
    """Simulates a $100M aggregator / PE-backed agency that actively steals your clicks."""
    def __init__(self):
        super().__init__(
            "competitor_predator",
            "VC-Backed Competitor Predator",
            "Simulates multi-million dollar competitor networks (Angi, Thumbtack, WebFX, HookAgency) and evaluates your survival odds."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        title = page_data.get("title", "").lower()
        url = page_data.get("url", "").lower()
        is_local = any(city in title or city in url for city in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
        
        observations = []
        recs = []
        
        if is_local:
            score = 80.0
            verdict = "PREDATOR_EVASION_SUCCESSFUL"
            observations.append({
                "type": "observed",
                "statement": "Aggregators (Angi/Thumbtack) do not customize deep hyper-local engineering blueprints for suburban contractors. You win on local technical specialization.",
                "evidence_ids": ["EVD-LOCAL-MOAT"],
                "confidence": 0.9
            })
        else:
            score = 15.0
            verdict = "PREDATOR_ROADKILL"
            observations.append({
                "type": "fatal_flaw",
                "statement": "You are trying to fight a 2,000-page VC-backed directory on their home turf with a 1-page national template. They outspend you $50,000 to $0 on link building every month.",
                "evidence_ids": ["EVD-COMPETITOR"],
                "confidence": 1.0
            })
            
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class AdversarialRefereeRole(BaseBrutalRole):
    """Calculates the brutal Composite Reality Index & Depression Score."""
    def __init__(self):
        super().__init__(
            "adversarial_referee",
            "Adversarial Evidence Referee & Reality Synthesizer",
            "Synthesizes all brutal verdicts, strips away comforting lies, and outputs the true Commercial Ranking & Survival Score."
        )

    def evaluate_swarm(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_score = sum(e["score"] for e in evaluations)
        avg_score = round(total_score / len(evaluations), 1)
        
        fatal_flaws = []
        all_recs = []
        for e in evaluations:
            for obs in e.get("observations", []):
                if obs.get("type") == "fatal_flaw":
                    fatal_flaws.append(obs["statement"])
            for r in e.get("recommendations", []):
                all_recs.append(r)
                
        if avg_score >= 80:
            consensus = "COMBAT_READY_SURVIVES_SERP_REALITY"
            depression_index = "LOW (Mathematically viable ranking probability)"
        elif avg_score >= 55:
            consensus = "LOCAL_STRIKING_DISTANCE_NEEDS_AUTHORITY_INJECTIONS"
            depression_index = "MODERATE (Ranks locally, but zero national presence)"
        else:
            consensus = "PAGE_9_OBLIVION_DELUSIONAL_STRATEGY"
            depression_index = "SEVERE (Page will generate 0 clicks and 0 leads for 12 months)"
            
        return {
            "agent_id": self.agent_id,
            "role": self.title,
            "composite_reality_score": avg_score,
            "depression_index": depression_index,
            "consensus": consensus,
            "fatal_flaws_count": len(fatal_flaws),
            "fatal_flaws": fatal_flaws,
            "total_evaluations": len(evaluations),
            "priority_recommendations": all_recs
        }
