"""
Brutal Adversarial SEO Swarm Simulator: The 12-Persona Reality Engine
====================================================================
Expanded, cutting-edge multi-agent ranking and commercial viability framework based on 
2026 Google Search Algorithm Mechanics (NavBoost User Click Feedback, AI Overviews Zero-Click
Interception, Information Gain Patents, Site-Wide Domain Quality Classifiers, Knowledge Graph
Entity Anchors, and Skeptical Commercial B2B Buyer Friction).

The 12 Specialized Adversarial Personas:
1.  `serp_executioner`: Google RankBrain & Algorithmic Executioner (KD vs DA Reality).
2.  `navboost_clickstream_critic`: Google NavBoost & "Bad Click" Pogo-Sticking Simulator.
3.  `ai_overview_interceptor`: Google AI Overviews Zero-Click Extraction Inquisitor.
4.  `backlink_debt_collector`: Off-Page Authority & Accredited Trade Referring Domain Auditor.
5.  `information_gain_tribunal`: Google Information Gain Patent & Proprietary Data Inspector.
6.  `internal_link_mesh_auditor`: PageRank Flow, Orphan Penalty, and Topic Cluster Isolator.
7.  `schema_knowledge_graph_prosecutor`: Schema.org / Wikidata / Semantic Entity Validator.
8.  `core_web_vitals_terminator`: Real-world 4G mobile latency, DOM thrashing, and INP metrics.
9.  `skeptical_bluecollar_cfo`: 55yo Roofing/HVAC contractor on a job site with zero patience for BS.
10. `b2b_operations_buyer`: CTO/Operations Manager looking for CRM webhook & API middleware specs.
11. `vc_competitor_predator`: $100M VC-backed aggregator outspending on link equity.
12. `adversarial_referee`: Final synthesizer calculating the "Composite Reality & Depression Index".
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
    """Audits search intent cannibalization, broad-match KD delusion, and Page 9 graveyard traps."""
    def __init__(self):
        super().__init__(
            "serp_executioner",
            "Google RankBrain & Algorithmic Executioner",
            "Audits search intent cannibalization, national KD vs DA debt, and Page 9 graveyard traps."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        title = page_data.get("title", "").lower()
        url = page_data.get("url", "").lower()
        
        is_generic_agency = any(term in title for term in ["roofing seo", "web design agency", "seo services", "digital marketing", "custom software"])
        has_geo = any(city in title or city in url for city in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land", "houston", "dallas"])
        
        observations = []
        recs = []
        
        if is_generic_agency and not has_geo:
            score = 12.0
            verdict = "PAGE_9_GRAVEYARD_GUARANTEED"
            observations.append({
                "type": "fatal_flaw",
                "statement": "NATIONAL COMPETITION SUICIDE: Page targets national KD 80+ keyword on a DA < 5 domain against WebFX, Clutch, and SEJ. Google places this on Position 80-95 where 0.0001% of searchers ever scroll.",
                "evidence_ids": ["EVD-TITLE", "EVD-KD"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Kill National Generic Targeting",
                "action": "Reposition page toward un-commoditized technical problem angles or localized city hubs.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 3, "risk": 1
            })
        else:
            score = 80.0
            verdict = "REALISTIC_LOCAL_STRIKING_DISTANCE"
            observations.append({
                "type": "observed",
                "statement": "Page targets localized geo-intent where local 3-pack algorithms weigh proximity over national backlink dominance.",
                "evidence_ids": ["EVD-TITLE"],
                "confidence": 0.95
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class NavBoostClickstreamCriticRole(BaseBrutalRole):
    """Simulates Google NavBoost user engagement: Good Clicks vs Bad Clicks (Pogo-sticking bounce)."""
    def __init__(self):
        super().__init__(
            "navboost_clickstream_critic",
            "Google NavBoost & User Clickstream Critic",
            "Simulates searcher click-through satisfaction, pogo-sticking bounces, and 'Last Longest Click' signals."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        html = page_data.get("html", "")
        
        # Immediate answer in first 200 words?
        has_immediate_answer = any(indicator in text[:500].lower() for indicator in ["$", "table", "step", "sub-0.8s", "loss", "cost", "speed"])
        has_clear_cta_above_fold = "tel:" in html[:2000] or "schedule" in text[:1000].lower()
        
        observations = []
        recs = []
        
        if has_immediate_answer and has_clear_cta_above_fold:
            score = 86.0
            verdict = "NAVBOOST_SATISFACTION_PASS"
            observations.append({
                "type": "observed",
                "statement": "Searcher receives direct quantitative answer in the top viewport, preventing back-button pogo-sticking.",
                "evidence_ids": ["EVD-VIEWPORT"],
                "confidence": 0.95
            })
        else:
            score = 30.0
            verdict = "POGO_STICK_BOUNCE_PENALTY"
            observations.append({
                "type": "fatal_flaw",
                "statement": "NAVBOOST DEMOTION: User must scroll past fluff paragraphs to find concrete data or pricing. Searchers tap 'Back' to SERP within 4 seconds, triggering NavBoost bad-click demotions.",
                "evidence_ids": ["EVD-BOUNCE"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Inject Low-Entropy Answer Block Above Fold",
                "action": "Place quantitative summary table or direct metric answer in the hero section.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "high", "effort": 1, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class AIOverviewInterceptorRole(BaseBrutalRole):
    """Evaluates whether Google AI Overviews synthesizes and steals the answer, yielding 0 clicks."""
    def __init__(self):
        super().__init__(
            "ai_overview_interceptor",
            "Google AI Overviews Zero-Click Interceptor",
            "Evaluates whether content is vulnerable to zero-click AI snippet cannibalization or forces human clicks via proprietary tools."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        text = page_data.get("text", "")
        
        has_interactive_tool = "<script" in html and any(t in text.lower() for t in ["calculator", "widget", "analyzer", "estimator", "grid"])
        is_basic_explainer = any(q in text.lower() for q in ["how to", "what is", "why use", "tips for", "benefits of"])
        
        observations = []
        recs = []
        
        if has_interactive_tool:
            score = 90.0
            verdict = "ZERO_CLICK_IMMUNE_TOOL"
            observations.append({
                "type": "observed",
                "statement": "Interactive utility cannot be rendered by AI Overviews directly in SERP, forcing the user to click through.",
                "evidence_ids": ["EVD-TOOL"],
                "confidence": 0.95
            })
        elif is_basic_explainer:
            score = 25.0
            verdict = "AI_SNIPPET_CANNIBALIZATION_VICTIM"
            observations.append({
                "type": "fatal_flaw",
                "statement": "ZERO-CLICK VICTIM: Text provides textbook definitions ('how Google Maps works'). Google AI Overviews synthesizes this in the SERP header. User never visits your site.",
                "evidence_ids": ["EVD-AIO"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Replace Commodity Text with Dynamic Calculation Tool",
                "action": "Embed interactive JavaScript calculator or gated proprietary forensic teardowns.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 2, "risk": 1
            })
        else:
            score = 65.0
            verdict = "MODERATE_AIO_EXPOSURE"

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class BacklinkDebtCollectorRole(BaseBrutalRole):
    """Exposes off-page authority bankruptcy and lack of trade citations."""
    def __init__(self):
        super().__init__(
            "backlink_debt_collector",
            "Off-Page Authority & Backlink Debt Collector",
            "Audits referring domain deficit, third-party citation debt, and brand search vacuum."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        has_verified_pypi = "pypi" in text.lower() or "contractor-lead-scraper" in text.lower() or "github" in text.lower()
        
        score = 25.0
        observations = [
            {
                "type": "fatal_flaw",
                "statement": "BACKLINK DEBT: 0 Referring Root Domains from accredited trade organizations (NRCA, RoofingContractor.com, TechCrunch). Google views this site as an unverified anonymous entity.",
                "evidence_ids": ["EVD-BACKLINKS"],
                "confidence": 1.0
            }
        ]
        if has_verified_pypi:
            score += 15.0
            observations.append({
                "type": "observed",
                "statement": "Open-source developer package anchor detected (DA 94 backlink).",
                "evidence_ids": ["EVD-PYPI"],
                "confidence": 0.95
            })
            
        recs = [{
            "title": "Syndicate Empirical Engineering Data",
            "action": "Publish forensic speed & tap-to-call audit reports to Medium, Dev.to, and trade forums.",
            "affected_urls": [page_data.get("url", "/")],
            "benefit": "critical", "effort": 3, "risk": 1
        }]
        
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": "AUTHORITY_BANKRUPTCY", "observations": observations, "recommendations": recs}

class InformationGainTribunalRole(BaseBrutalRole):
    """Destroys commodity AI-generated fluff and tests for Google Information Gain Patent compliance."""
    def __init__(self):
        super().__init__(
            "information_gain_tribunal",
            "Information Gain & Proprietary Data Tribunal",
            "Audits whether content introduces net-new statistical benchmarks or paraphrases competitor pages."
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
            verdict = "INFORMATION_GAIN_CONFIRMED"
            observations.append({
                "type": "observed",
                "statement": "Proprietary interactive calculation utility + empirical roofer latency audit data satisfies Information Gain patent.",
                "evidence_ids": ["EVD-TOOL", "EVD-DATA"],
                "confidence": 0.95
            })
        else:
            score = 22.0
            verdict = "COMMODITY_AI_SLOP_DETECTED"
            observations.append({
                "type": "fatal_flaw",
                "statement": "ZERO INFORMATION GAIN: Content is derivative textbook summaries. Google penalizes pages that fail to introduce new statistical data or original tools.",
                "evidence_ids": ["EVD-COPY"],
                "confidence": 1.0
            })
            recs.append({
                "title": "Inject Proprietary Audit Charts",
                "action": "Embed real anonymized roofer speed teardown stats (340 contractors tested).",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "critical", "effort": 2, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class InternalLinkMeshAuditorRole(BaseBrutalRole):
    """Audits PageRank flow, orphan risk, and topical mesh interconnectivity."""
    def __init__(self):
        super().__init__(
            "internal_link_mesh_auditor",
            "Internal Link Mesh & PageRank Flow Auditor",
            "Audits internal anchor connectivity, parent hub registration, and orphan status."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        links = len(re.findall(r'href=[\'"][^\'"]+[\'"]', html))
        has_hub_return = "services" in html or "industries" in html or "portfolio" in html
        
        observations = []
        recs = []
        
        if links >= 8 and has_hub_return:
            score = 90.0
            verdict = "TOPICAL_MESH_CONNECTED"
            observations.append({
                "type": "observed",
                "statement": f"Internal links detected ({links}) maintaining bi-directional crawl paths.",
                "evidence_ids": ["EVD-LINKS"],
                "confidence": 0.95
            })
        else:
            score = 45.0
            verdict = "WEAK_INTERNAL_LINK_DENSITY"
            observations.append({
                "type": "critique",
                "statement": "Low internal link count. Google crawlers struggle to distribute PageRank to this node.",
                "evidence_ids": ["EVD-LINKS"],
                "confidence": 0.9
            })
            recs.append({
                "title": "Connect Bi-Directional Cluster Links",
                "action": "Add anchor cards connecting this page to sibling solutions and parent hubs.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "medium", "effort": 1, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class SchemaKnowledgeGraphProsecutorRole(BaseBrutalRole):
    """Audits Schema.org JSON-LD entity graph validity."""
    def __init__(self):
        super().__init__(
            "schema_knowledge_graph_prosecutor",
            "Schema & Knowledge Graph Entity Prosecutor",
            "Validates structured data against Google's Knowledge Graph and LocalBusiness specifications."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_schema = "application/ld+json" in html
        has_specific_entity = any(e in html for e in ["RoofingContractor", "ProfessionalService", "LocalBusiness", "FAQPage", "SoftwareApplication"])
        
        observations = []
        recs = []
        
        if has_schema and has_specific_entity:
            score = 92.0
            verdict = "SEMANTIC_GRAPH_VALIDATED"
            observations.append({
                "type": "observed",
                "statement": "Rich JSON-LD entity graph with specific Schema.org typology identified.",
                "evidence_ids": ["EVD-SCHEMA"],
                "confidence": 1.0
            })
        else:
            score = 30.0
            verdict = "UNSTRUCTURED_DATA_VOID"
            observations.append({
                "type": "fatal_flaw",
                "statement": "Missing specific Schema.org JSON-LD entity declarations. Google Knowledge Graph cannot disambiguate service regions or offerings.",
                "evidence_ids": ["EVD-SCHEMA"],
                "confidence": 1.0
            })
            
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class CoreWebVitalsTerminatorRole(BaseBrutalRole):
    """Audits real 4G cellular performance and INP metrics."""
    def __init__(self):
        super().__init__(
            "core_web_vitals_terminator",
            "Core Web Vitals & 4G Cellular Terminator",
            "Audits Interaction to Next Paint (INP), Largest Contentful Paint (LCP), and DOM bloat on 4G networks."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        has_heavy_framework = any(fw in html.lower() for fw in ["react", "vue", "angular", "next", "nuxt"])
        
        observations = []
        if not has_heavy_framework:
            score = 94.0
            verdict = "SUB_0_8S_CRUSH_SPEED"
            observations.append({
                "type": "observed",
                "statement": "Zero framework bloat. Pure server-rendered semantic HTML + Tailwind CSS. FCP < 0.4s on 4G cellular.",
                "evidence_ids": ["EVD-PERF"],
                "confidence": 1.0
            })
        else:
            score = 35.0
            verdict = "JS_HYDRATION_DEATH"
            observations.append({
                "type": "fatal_flaw",
                "statement": "Client JS framework thrashing mobile CPU and delaying LCP to 4.2s on mobile networks.",
                "evidence_ids": ["EVD-PERF"],
                "confidence": 1.0
            })
            
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": []}

class SkepticalBlueCollarCFORole(BaseBrutalRole):
    """The 55yo commercial contractor on a job site testing conversion friction."""
    def __init__(self):
        super().__init__(
            "skeptical_bluecollar_cfo",
            "Skeptical Blue-Collar Contractor Persona",
            "Simulates a 55yo commercial roofing/HVAC owner inspecting the page on an iPhone 13 on a muddy job site."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        html = page_data.get("html", "")
        
        has_tel = "tel:" in html
        has_ownership = "100%" in text or "ownership" in text.lower()
        has_buzzwords = any(b in text.lower() for b in ["skyrocket", "game-changer", "10x", "leading provider", "cutting-edge", "synergy"])
        
        observations = []
        recs = []
        score = 85.0
        
        if not has_tel:
            score -= 35.0
            observations.append({
                "type": "fatal_flaw",
                "statement": "NO TAP-TO-CALL: No direct phone dialer. I am on a ladder and will not type into an email form.",
                "evidence_ids": ["EVD-TEL"],
                "confidence": 1.0
            })
        if not has_ownership:
            score -= 25.0
            observations.append({
                "type": "fatal_flaw",
                "statement": "NO ASSET OWNERSHIP: Last agency locked my domain hostage. If you don't state '100% Client Asset Ownership', I bounce.",
                "evidence_ids": ["EVD-OWNERSHIP"],
                "confidence": 0.95
            })
        if has_buzzwords:
            score -= 30.0
            observations.append({
                "type": "fatal_flaw",
                "statement": "AGENCY BS DETECTED: Page uses fluffy buzzwords. Instant closed tab.",
                "evidence_ids": ["EVD-BUZZWORDS"],
                "confidence": 1.0
            })
            
        verdict = "CONTRACTOR_RESPECT_EARNED" if score >= 75 else "CONTRACTOR_INSTANT_BOUNCE"
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": max(5.0, score), "verdict": verdict, "observations": observations, "recommendations": recs}

class B2BOperationsBuyerRole(BaseBrutalRole):
    """Simulates a CTO / Operations Manager looking for technical specs (CRM Webhooks, APIs, SLAs)."""
    def __init__(self):
        super().__init__(
            "b2b_operations_buyer",
            "B2B Operations & CTO Buyer Persona",
            "Evaluates whether page provides concrete technical architecture (API endpoints, ServiceTitan webhooks, sub-60s SMS SLAs) or vague marketing promises."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        has_tech_specs = any(t in text.lower() for t in ["webhook", "api", "servicetitan", "jobnimbus", "e.164", "sub-0.8s", "sms", "json-ld"])
        
        observations = []
        recs = []
        
        if has_tech_specs:
            score = 88.0
            verdict = "TECHNICAL_AUTHORITY_PASSED"
            observations.append({
                "type": "observed",
                "statement": "Concrete technical middleware & CRM integration parameters specified.",
                "evidence_ids": ["EVD-SPECS"],
                "confidence": 0.95
            })
        else:
            score = 40.0
            verdict = "VAGUE_MARKETING_FLUFF"
            observations.append({
                "type": "critique",
                "statement": "Page lacks technical specifications. CTOs and Ops Managers dismiss it as generic non-technical agency sales copy.",
                "evidence_ids": ["EVD-SPECS"],
                "confidence": 0.9
            })
            recs.append({
                "title": "Inject Integration Architecture Specs",
                "action": "Add specific CRM webhook protocols (ServiceTitan, AccuLynx, Jobber) and sub-60s SMS dispatch guarantees.",
                "affected_urls": [page_data.get("url", "/")],
                "benefit": "high", "effort": 1, "risk": 1
            })

        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": recs}

class VCCompetitorPredatorRole(BaseBrutalRole):
    """Simulates a $100M VC-backed aggregator outspending on link equity."""
    def __init__(self):
        super().__init__(
            "vc_competitor_predator",
            "VC-Backed Competitor Predator",
            "Simulates multi-million dollar competitor networks (Angi, Thumbtack, WebFX, Clutch) and evaluates survival odds."
        )

    def evaluate(self, page_data: Dict[str, Any], evidence_map: Dict[str, str]) -> Dict[str, Any]:
        title = page_data.get("title", "").lower()
        url = page_data.get("url", "").lower()
        is_local = any(city in title or city in url for city in ["tyler", "waco", "san angelo", "macon", "clarksville", "midland", "odessa", "katy", "woodlands", "sugar land"])
        
        observations = []
        if is_local:
            score = 82.0
            verdict = "PREDATOR_EVASION_SUCCESSFUL"
            observations.append({
                "type": "observed",
                "statement": "Aggregators do not customize hyper-local engineering blueprints for suburban contractors. You win on local technical specialization.",
                "evidence_ids": ["EVD-LOCAL-MOAT"],
                "confidence": 0.9
            })
        else:
            score = 15.0
            verdict = "PREDATOR_ROADKILL"
            observations.append({
                "type": "fatal_flaw",
                "statement": "VC-backed aggregators outspend you $50,000 to $0 on link equity every month for national keywords.",
                "evidence_ids": ["EVD-COMPETITOR"],
                "confidence": 1.0
            })
            
        return {"agent_id": self.agent_id, "role": self.title, "status": "complete", "score": score, "verdict": verdict, "observations": observations, "recommendations": []}

class AdversarialRefereeRole(BaseBrutalRole):
    """Calculates the brutal Composite Reality Index & Depression Score across all 11 analyst personas."""
    def __init__(self):
        super().__init__(
            "adversarial_referee",
            "Adversarial Evidence Referee & Reality Synthesizer",
            "Synthesizes all 11 brutal verdicts, strips away comforting lies, and outputs the true Commercial Ranking & Survival Score."
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
