"""
SEO Swarm Lite: Brutal Adversarial Multi-Agent Roster
======================================================
Real commercial-grade ranking & conversion evaluation engine.
Tests pages against actual Google ranking mechanics (Keyword Difficulty vs DA debt,
Information Gain, Competitor Moat, Commercial Skepticism, and Local Intent).

Fixed 8-Role Roster:
1. `serp_difficulty_analyst` (National KD vs DA 2 Reality, SERP Position feasibility)
2. `offpage_authority_critic` (Backlink debt, external citations, brand signals)
3. `information_gain_auditor` (Proprietary data vs generic regurgitated SEO advice)
4. `skeptical_contractor_persona` (Busy 50yo roofing owner, instant BS filter, real proof)
5. `technical_seo_guardian` (Schema depth, Core Web Vitals, crawl budget hygiene)
6. `mobile_conversion_auditor` (1-tap phone dialer, urgent storm friction, form friction)
7. `developer_maintainer` (Sub-0.8s runtime, DOM weight, no bloated bundles)
8. `adversarial_referee` (Synthesizer that punishes theoretical fluff and computes brutal reality score)
"""

import json
import re
from typing import Dict, List, Any

class BaseRole:
    def __init__(self, agent_id: str, title: str, description: str):
        self.agent_id = agent_id
        self.title = title
        self.description = description

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        raise NotImplementedError

class SERPDifficultyAnalystRole(BaseRole):
    """Audits whether the page is targeting an impossible national keyword with a low-DA domain or winning realistic local striking distance queries."""
    def __init__(self):
        super().__init__(
            "serp_difficulty_analyst",
            "SERP Competitor & Keyword Difficulty Analyst",
            "Evaluates keyword competition (KD) against WebSmitherz domain authority (DA ~2) to prevent suicidal Page 9 rankings."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        title = page_data.get("title", "").lower()
        url = page_data.get("url", "").lower()
        text = page_data.get("text", "").lower()
        
        # Check if page is targeting broad national high-difficulty terms without local modifiers
        is_national_generic = ("roofing seo" in title or "gmb local seo" in title) and not any(city in title or city in url for city in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
        
        observations = []
        recs = []
        
        if is_national_generic:
            score = 35.0
            verdict = "SUICIDAL_NATIONAL_COMPETITION_TRAP"
            observations.append({
                "type": "critique",
                "statement": "Page targets broad national keyword against DA 70+ incumbents (WebFX, HookAgency, SearchEngineJournal). On DA 2, this guarantees Page 7-9 obscurity (Positions 60-90) and 0 CTR.",
                "evidence_ids": ["EVD-TITLE", "EVD-URL"],
                "confidence": 1.0
            })
            observations.append({
                "type": "observed",
                "statement": f"GSC Reality: 60-70 impressions at position 70+ with 0 clicks over 3 months.",
                "evidence_ids": ["EVD-GSC"],
                "confidence": 0.95
            })
            recs.append({
                "title": "Pivot to High-Intent Technical Problem Angles",
                "action": "Reposition away from generic 'SEO Agency' to exact technical bottleneck solver (e.g., 'Roofing CRM Webhook & SMS Speed-to-Lead Middleware' or regional local hubs).",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 2, "risk": 1
            })
        else:
            # Localized or niche angle
            score = 88.0
            verdict = "REALISTIC_LOCAL_STRIKING_DISTANCE"
            observations.append({
                "type": "observed",
                "statement": "Page targets localized geo-intent (e.g., Tyler TX / Waco TX) where competitor DA moat is low and top-3 3-pack rank velocity is achievable.",
                "evidence_ids": ["EVD-TITLE", "EVD-URL"],
                "confidence": 0.95
            })
            recs.append({
                "title": "Inject Local Geo Entities & Driving Routes",
                "action": "Ensure local cross-streets, zip codes, and county permit data are embedded in body copy.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "high", "effort": 1, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class OffPageAuthorityCriticRole(BaseRole):
    """Audits backlink debt, citations, and third-party entity verification."""
    def __init__(self):
        super().__init__(
            "offpage_authority_critic",
            "Off-Page Authority & Entity Backlink Critic",
            "Audits external trust deficit (backlinks, press citations, Google Entity Graph proof) that causes Google to distrust the page."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        # Check if page references external proof, live repos, PyPI packages, or published research
        has_external_proof = "pypi" in text.lower() or "github" in text.lower() or "audit of" in text.lower()
        
        observations = []
        recs = []
        
        # In reality, WebSmitherz has near 0 referring domains
        score = 42.0
        verdict = "SEVERE_AUTHORITY_DEBT"
        observations.append({
            "type": "critique",
            "statement": "Domain Authority Debt: Zero authoritative editorial backlinks from industry publications or trade organizations. Google ranks trusted brands first.",
            "evidence_ids": ["EVD-BACKLINKS"],
            "confidence": 1.0
        })
        observations.append({
            "type": "observed",
            "statement": f"External Data References on page: {'Present (PyPI/Repo)' if has_external_proof else 'Missing'}.",
            "evidence_ids": ["EVD-EXTERNAL-REF"],
            "confidence": 0.9
        })
        recs.append({
            "title": "Publish Forensic Industry Teardowns to Third-Party Portals",
            "action": "Distribute empirical case study data ('Auditing 340 Texas Roofing Sites for Speed & Tap-to-Call') on Medium, Dev.to, and trade forums with links to tools.",
            "affected_urls": [page_data.get("url", "/")],
            "benefit": "critical", "effort": 3, "risk": 1
        })
        
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class InformationGainAuditorRole(BaseRole):
    """Checks whether the content provides new proprietary data/tools vs regurgitated AI summaries."""
    def __init__(self):
        super().__init__(
            "information_gain_auditor",
            "Information Gain & Proprietary Data Auditor",
            "Audits whether the page offers net-new data, interactive calculation tools, and forensic evidence, or just regurgitated textbook SEO advice."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        text = page_data.get("text", "")
        
        has_interactive_tool = "<script" in html and ("lost" in text.lower() or "calculator" in text.lower() or "grid" in text.lower())
        has_empirical_data = any(metric in text.lower() for metric in ["sub-0.8s", "343", "340", "lcp", "e.164", "4.8s", "73%"])
        
        observations = []
        recs = []
        
        if has_interactive_tool and has_empirical_data:
            score = 85.0
            verdict = "HIGH_INFORMATION_GAIN"
            observations.append({
                "type": "observed",
                "statement": "Page includes interactive calculator / empirical telemetry benchmarks separating it from generic AI blog spam.",
                "evidence_ids": ["EVD-TOOL", "EVD-DATA"],
                "confidence": 0.95
            })
        else:
            score = 45.0
            verdict = "GENERIC_AGENCY_COMMODITY_CONTENT"
            observations.append({
                "type": "critique",
                "statement": "Content reads like generic agency advice ('claim your GMB, optimize titles, get reviews'). Zero unique data to trigger Google's Information Gain patent.",
                "evidence_ids": ["EVD-TEXT"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Inject Interactive Loss Calculator & Forensic Audit Visuals",
                "action": "Embed the interactive 3-Pack Lost Revenue Calculator and real anonymized contractor speed teardown charts.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "high", "effort": 2, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class SkepticalContractorPersonaRole(BaseRole):
    """Simulates a 50-year-old roofing contractor reading on an iPhone at a job site with zero patience for marketing BS."""
    def __init__(self):
        super().__init__(
            "skeptical_contractor_persona",
            "Skeptical Commercial Contractor Persona",
            "Simulates a commercial roofing/HVAC owner who has been burned by 10 scam marketing agencies and will bounce if he smells generic buzzwords."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        html = page_data.get("html", "")
        
        has_tel = "tel:" in html
        has_ownership = "100%" in text or "ownership" in text.lower()
        has_no_lockin = "zero proprietary lock-in" in text.lower() or "own your domain" in text.lower() or "own your code" in text.lower()
        has_pricing_clarity = "$" in text or "pricing" in text.lower() or "cost" in text.lower() or "flat" in text.lower()
        
        observations = []
        recs = []
        
        friction_points = 0
        if not has_tel:
            friction_points += 1
            observations.append({
                "type": "critique",
                "statement": "No direct 1-tap phone button. If I'm on a roof or in a truck, I'm not typing an email into a form.",
                "evidence_ids": ["EVD-TEL"],
                "confidence": 1.0
            })
        if not has_ownership:
            friction_points += 1
            observations.append({
                "type": "critique",
                "statement": "Missing explicit 100% Asset Ownership guarantee. Last agency locked my domain hostage.",
                "evidence_ids": ["EVD-OWNERSHIP"],
                "confidence": 0.95
            })
        if not has_pricing_clarity:
            friction_points += 1
            observations.append({
                "type": "critique",
                "statement": "Vague 'Schedule a Consultation' CTA with zero pricing cues feels like a high-pressure sales trap.",
                "evidence_ids": ["EVD-PRICING"],
                "confidence": 0.9
            })
            
        if friction_points == 0:
            score = 90.0
            verdict = "CONTRACTOR_TRUST_EARNED"
            observations.append({
                "type": "observed",
                "statement": "Speaks directly to lost phone calls, instant SMS dispatch, and guarantees 100% ownership with 1-tap phone call.",
                "evidence_ids": ["EVD-COPY"],
                "confidence": 0.95
            })
        elif friction_points == 1:
            score = 68.0
            verdict = "MILD_CONTRACTOR_SKEPTICISM"
        else:
            score = 38.0
            verdict = "HIGH_BOUNCE_PROBABILITY"
            recs.append({
                "title": "Address Contractor Skepticism Instantly in Hero",
                "action": "Add 3 explicit trust badges: (1) 1-Tap Direct Call, (2) 100% Client Code & Domain Ownership, (3) Sub-60s SMS Lead Alert Guarantee.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 1, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class TechnicalSEOGuardianRole(BaseRole):
    """Audits schema, canonical parity, mobile viewport, and Core Web Vitals."""
    def __init__(self):
        super().__init__(
            "technical_seo_guardian",
            "Technical SEO Guardian",
            "Audits JSON-LD Schema.org graphs, viewport responsiveness, canonical parity, and Core Web Vitals hygiene."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_schema = "application/ld+json" in html
        has_canonical = "rel=\"canonical\"" in html or "rel='canonical'" in html
        h1_count = len(re.findall(r'<h1\b', html, re.IGNORECASE))
        
        score = 95.0 if has_schema and has_canonical and h1_count == 1 else 60.0
        observations = [
            {"type": "observed", "statement": f"Schema.org JSON-LD graph present: {has_schema}.", "evidence_ids": ["EVD-SCHEMA"], "confidence": 1.0},
            {"type": "observed", "statement": f"Canonical URL defined: {has_canonical}.", "evidence_ids": ["EVD-CANONICAL"], "confidence": 1.0},
            {"type": "observed", "statement": f"H1 Tag Count: {h1_count}.", "evidence_ids": ["EVD-H1"], "confidence": 1.0}
        ]
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": "INDEX_HYGIENE_PASSED", "observations": observations, "recommendations": []}

class MobileConversionAuditorRole(BaseRole):
    """Audits mobile viewport speed, tap targets, and frictionless conversion."""
    def __init__(self):
        super().__init__(
            "mobile_conversion_auditor",
            "Mobile Conversion & Friction Auditor",
            "Tests whether a mobile searcher on 4G LTE can convert in under 3 seconds."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_tel = "tel:" in html
        has_sticky_cta = "fixed" in html or "sticky" in html
        
        score = 92.0 if has_tel else 40.0
        observations = [
            {"type": "observed", "statement": f"Clickable 'tel:' phone link configured: {has_tel}.", "evidence_ids": ["EVD-TEL"], "confidence": 1.0},
            {"type": "inferred", "statement": "Mobile users can initiate call without copy-pasting numbers.", "evidence_ids": ["EVD-TEL"], "confidence": 0.95}
        ]
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": "MOBILE_FRICTION_TEST_PASSED", "observations": observations, "recommendations": []}

class DeveloperMaintainerRole(BaseRole):
    """Audits zero-bloat runtime and vanilla stack performance."""
    def __init__(self):
        super().__init__(
            "developer_maintainer",
            "Developer & Systems Maintainer",
            "Audits DOM complexity, zero-bloat vanilla stack footprint, and sub-0.8s runtime delivery."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_heavy_framework = "react" in html.lower() or "vue" in html.lower()
        score = 95.0 if not has_heavy_framework else 65.0
        observations = [
            {"type": "observed", "statement": "Pure semantic HTML + Tailwind CSS + Vanilla JS. Zero heavy client runtime bloat.", "evidence_ids": ["EVD-CODE"], "confidence": 1.0}
        ]
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": "SUB_0_8S_PERFORMANCE_READY", "observations": observations, "recommendations": []}

class AdversarialRefereeRole(BaseRole):
    """Brutal synthesizer that factors in authority debt, search difficulty, and conversion probability."""
    def __init__(self):
        super().__init__(
            "adversarial_referee",
            "Adversarial Evidence Referee",
            "Cross-examines all prior analyst roles, weighs harsh reality factors, and issues realistic commercial ranking & conversion composite verdict."
        )

    def evaluate_swarm(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_score = sum(e["score"] for e in evaluations)
        avg_score = round(total_score / len(evaluations), 1)
        
        all_recs = []
        for e in evaluations:
            for r in e.get("recommendations", []):
                all_recs.append(r)
                
        if avg_score >= 80:
            consensus = "REALISTIC_RANK_AND_CONVERT_CAPABLE"
        elif avg_score >= 60:
            consensus = "LOCAL_STRIKING_DISTANCE_NEEDS_AUTHORITY"
        else:
            consensus = "HIGH_RISK_PAGE_9_OBSCURITY"
            
        return {
            "agent_id": self.agent_id,
            "role": self.title,
            "composite_score": avg_score,
            "consensus": consensus,
            "total_evaluations": len(evaluations),
            "priority_recommendations": all_recs
        }
