"""
SEO Swarm Simulation Engine (MiroFish-Inspired Multi-Agent Architecture)
=======================================================================
Spawns synthetic persona swarms to audit, stress-test, and critique 
websites, landing pages, and SEO strategies before publishing.

Agent Personas:
1. High-Intent Commercial Customer (Homeowner / Commercial Buyer)
2. Senior Technical SEO & Systems Architect (Core Web Vitals & Schemas)
3. Direct Response Copywriter & CRO Auditor (Friction & CTA Hook Analysis)
4. AI Search & Semantic Entity Indexer (Perplexity / ChatGPT / SGE Crawler)
5. Skeptical Competitor / Market Rival (Weakness & Vulnerability Exploiter)
"""

import json
import re
import urllib.request
from typing import Dict, List, Any

class AgentPersona:
    def __init__(self, name: str, role: str, perspective: str, criteria: List[str], bias: str):
        self.name = name
        self.role = role
        self.perspective = perspective
        self.criteria = criteria
        self.bias = bias

    def evaluate(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Base evaluation logic tailored to each persona's heuristics."""
        raise NotImplementedError

class HomeownerCustomerAgent(AgentPersona):
    def __init__(self):
        super().__init__(
            name="Marcus Vance",
            role="High-Intent Homeowner (Commercial Buyer)",
            perspective="Needs an urgent roof replacement estimate on mobile after a severe storm. Impatient, values trust, transparent pricing, and 1-tap phone calls.",
            criteria=["Instant Contact Clarity", "Social Proof & Reviews", "Sub-1s Mobile UX", "Zero Gimmicks / Transparent Terms"],
            bias="Will bounce within 3 seconds if phone number is not clickable or if page loads slowly on 5G."
        )

    def evaluate(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        text = page_data.get("text", "")
        
        has_tel = "tel:" in html or "tel:+" in html
        has_reviews = bool(re.search(r'review|rating|5-star|star|testimoni', text, re.IGNORECASE))
        has_trust_badges = bool(re.search(r'guarantee|license|insured|bonded|bbb|certified', text, re.IGNORECASE))
        has_pricing_hint = bool(re.search(r'\$|price|pricing|estimate|quote', text, re.IGNORECASE))
        
        score = 0
        findings = []
        
        if has_tel:
            score += 30
            findings.append("[PASS] Direct 1-tap phone action is immediately accessible.")
        else:
            findings.append("[CRITICAL] Missing click-to-call 'tel:' action. Homeowners cannot tap to dial.")

        if has_reviews:
            score += 25
            findings.append("[PASS] Local review signals & homeowner testimonials detected.")
        else:
            findings.append("[WARN] No prominent customer reviews or ratings visible above fold.")

        if has_trust_badges:
            score += 25
            findings.append("[PASS] Licensed, insured, or warranty trust anchors confirmed.")
        else:
            findings.append("[WARN] Missing explicit licensing / insurance trust badges.")

        if has_pricing_hint:
            score += 20
            findings.append("[PASS] Transparent estimate / pricing cues present.")
        else:
            findings.append("[WARN] Zero pricing orientation causes prospective buyers to hesitate.")

        verdict = "CONVERT" if score >= 75 else ("HESITATE" if score >= 50 else "BOUNCE")
        
        return {
            "agent": self.name,
            "role": self.role,
            "score": score,
            "verdict": verdict,
            "findings": findings,
            "feedback": (
                "The page communicates clear authority and direct booking action." if score >= 75
                else "Friction in contact options or lack of social proof risks customer drop-off."
            )
        }

class TechnicalSEOArchitectAgent(AgentPersona):
    def __init__(self):
        super().__init__(
            name="Dr. Elena Rostova",
            role="Senior Technical SEO & Web Architect",
            perspective="Inspects Core Web Vitals, Schema.org JSON-LD graph integrity, canonical hierarchy, DOM depth, and zero-error indexability.",
            criteria=["Structured Data (JSON-LD)", "Canonical URL Parity", "Semantic Heading Hierarchy", "Mobile Viewport Standards", "Title Budget (<60 chars)"],
            bias="Strict algorithmic compliance. Flags missing microdata, duplicate tags, or bloat."
        )

    def evaluate(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        title = page_data.get("title", "")
        meta_desc = page_data.get("meta_desc", "")
        
        has_schema = "application/ld+json" in html
        has_canonical = '<link rel="canonical"' in html or "<link rel='canonical'" in html
        has_viewport = 'name="viewport"' in html or "name='viewport'" in html
        h1_count = len(re.findall(r'<h1\b', html, re.IGNORECASE))
        title_len = len(title)
        
        score = 0
        findings = []
        
        if has_schema:
            score += 30
            findings.append("[PASS] Structured Schema.org JSON-LD graph active.")
        else:
            findings.append("[CRITICAL] Missing Schema.org structured data graph.")

        if has_canonical:
            score += 20
            findings.append("[PASS] Canonical URL link tag defined.")
        else:
            findings.append("[WARN] Missing canonical link tag.")

        if has_viewport:
            score += 15
            findings.append("[PASS] Mobile responsive viewport meta configured.")
        else:
            findings.append("[CRITICAL] Missing viewport tag.")

        if h1_count == 1:
            score += 20
            findings.append("[PASS] Exactly 1 semantic H1 header detected.")
        elif h1_count == 0:
            findings.append("[CRITICAL] Missing H1 semantic heading.")
        else:
            score += 10
            findings.append(f"[WARN] Multiple ({h1_count}) H1 headings detected.")

        if 30 <= title_len <= 65:
            score += 15
            findings.append(f"[PASS] Title tag length ({title_len} chars) is optimal for SERP snippets.")
        else:
            findings.append(f"[WARN] Title tag length ({title_len} chars) outside optimal 30-65 char budget.")

        verdict = "INDEX_HIGH_CONFIDENCE" if score >= 80 else ("INDEX_WITH_WARNINGS" if score >= 55 else "FAIL_AUDIT")

        return {
            "agent": self.name,
            "role": self.role,
            "score": score,
            "verdict": verdict,
            "findings": findings,
            "feedback": (
                "Technical foundation is solid with valid structured schema and semantic tags." if score >= 80
                else "Technical gaps detected that may limit indexing performance."
            )
        }

class CROCopywriterAgent(AgentPersona):
    def __init__(self):
        super().__init__(
            name="Sloan Sterling",
            role="Direct-Response Copywriter & CRO Specialist",
            perspective="Audits AIDA flow, headline hooks, value proposition clarity, button copy, and cognitive friction in lead forms.",
            criteria=["Outcome-Driven Headline", "Zero Marketing Buzzwords", "High-Converting CTA Copy", "Structured FAQ Accordions", "Low-Friction Form Fields"],
            bias="Ruthlessly flags sloppy marketing fluff, vague button labels ('Submit'), or cluttered forms."
        )

    def evaluate(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        html = page_data.get("html", "")
        
        # Fluff checks
        banned_buzzwords = ["skyrocket", "game-changer", "synergy", "10x", "leading provider", "cutting-edge", "all-in-one solution"]
        fluff_found = [w for w in banned_buzzwords if w in text.lower()]
        
        has_specific_cta = bool(re.search(r'Claim|Get Free|Audit|Estimate|Schedule|Book|Download', text, re.IGNORECASE))
        has_faqs = bool(re.search(r'faq|frequently asked questions', text, re.IGNORECASE))
        section_count = len(re.findall(r'<section\b', html, re.IGNORECASE))
        
        score = 0
        findings = []
        
        if not fluff_found:
            score += 35
            findings.append("[PASS] Zero spam buzzwords. Understated, senior engineering peer tone maintained.")
        else:
            findings.append(f"[CRITICAL] Detected banned marketing fluff: {', '.join(fluff_found)}")

        if has_specific_cta:
            score += 25
            findings.append("[PASS] High-converting, outcome-driven CTA buttons detected.")
        else:
            findings.append("[WARN] CTA text is generic or lacks compelling value proposition.")

        if has_faqs:
            score += 20
            findings.append("[PASS] Structured FAQ section addresses buyer objections directly.")
        else:
            findings.append("[WARN] Missing FAQ objection-handling blocks.")

        if section_count >= 6:
            score += 20
            findings.append(f"[PASS] Rich modular section depth ({section_count} standalone sections).")
        else:
            score += 10
            findings.append(f"[WARN] Thin page structure ({section_count} sections). Needs deeper AIDA flow.")

        verdict = "HIGH_CONVERSION" if score >= 80 else ("MODERATE_CONVERSION" if score >= 55 else "LOW_CONVERSION")

        return {
            "agent": self.name,
            "role": self.role,
            "score": score,
            "verdict": verdict,
            "findings": findings,
            "feedback": (
                "Copy resonates with clear commercial outcomes and low-friction action triggers." if score >= 80
                else "Refine headlines and eliminate passive phrasing to increase conversion rates."
            )
        }

class AISearchCrawlerAgent(AgentPersona):
    def __init__(self):
        super().__init__(
            name="Synthetix-7",
            role="AI Search Engine Crawler (ChatGPT / Perplexity / SGE)",
            perspective="Extracts low-entropy direct answers, entity relationships, structured tables, and factual data for AI generation.",
            criteria=["Direct Answer Callout", "Entity Relationship Graphs", "Structured Comparison Tables", "Verified Statistics & Data"],
            bias="Favors high information gain, concise answers, and semantic structured data over narrative filler."
        )

    def evaluate(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        html = page_data.get("html", "")
        text = page_data.get("text", "")
        
        has_table = "<table" in html or "grid-cols-" in html
        has_faq_data = "acceptedAnswer" in html
        has_summary_callout = bool(re.search(r'Executive Summary|Takeaway|Finding|Architecture|Benchmark', text, re.IGNORECASE))
        has_stats = bool(re.search(r'\d+(\.\d+)?%|\$\d+|\d+s|\d+ days', text))
        
        score = 0
        findings = []
        
        if has_summary_callout:
            score += 30
            findings.append("[PASS] Low-entropy answer callout block available for AI extraction.")
        else:
            findings.append("[WARN] Missing explicit Executive Summary / Answer block for LLM retrieval.")

        if has_faq_data:
            score += 30
            findings.append("[PASS] Structured Q&A schemas provide verified AI citation anchors.")
        else:
            findings.append("[WARN] Missing structured FAQPage JSON-LD entities.")

        if has_table:
            score += 20
            findings.append("[PASS] Structured data / comparison table detected.")
        else:
            findings.append("[WARN] Missing comparison or feature matrix tables.")

        if has_stats:
            score += 20
            findings.append("[PASS] Specific quantifiable metrics, speed stats, and numbers present.")
        else:
            findings.append("[WARN] Copy lacks quantifiable numerical data points.")

        verdict = "CITED_AS_PRIMARY_SOURCE" if score >= 80 else ("ELIGIBLE_FOR_SNIPPET" if score >= 55 else "IGNORED_BY_AI")

        return {
            "agent": self.name,
            "role": self.role,
            "score": score,
            "verdict": verdict,
            "findings": findings,
            "feedback": (
                "High information density. AI models can easily parse and cite this content as an authority." if score >= 80
                else "Increase factual density and add structured tables for better AI search citations."
            )
        }

class CompetitorRivalAgent(AgentPersona):
    def __init__(self):
        super().__init__(
            name="Vance Kincaid",
            role="Aggressive Competitor Agency Lead",
            perspective="Audits page for weaknesses, missing local territories, unaddressed customer fears, and vulnerabilities to exploit.",
            criteria=["Unique Value Proposition", "Competitive Moat", "Local Territory Locking", "Guarantees & Risk Reversals"],
            bias="Looks for unbacked claims, hidden costs, or weak positioning to outrank or counter-pitch."
        )

    def evaluate(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        text = page_data.get("text", "")
        
        has_ownership_moat = bool(re.search(r'100% (client )?ownership|zero (shared|lock-in)|exclusive', text, re.IGNORECASE))
        has_speed_moat = bool(re.search(r'sub-0\.8s|sub-second|0\.8s|0\.7s', text, re.IGNORECASE))
        has_guarantee = bool(re.search(r'guarantee|30-day|sla|support', text, re.IGNORECASE))
        has_local_focus = bool(re.search(r'county|3-pack|maps|local', text, re.IGNORECASE))
        
        score = 0
        findings = []
        
        if has_ownership_moat:
            score += 30
            findings.append("[PASS] Strong moat: 100% client asset ownership counter-positions against locked agencies.")
        else:
            findings.append("[VULNERABILITY] Missing strong ownership guarantee. Competitors can exploit lock-in fear.")

        if has_speed_moat:
            score += 30
            findings.append("[PASS] Sub-0.8s engineering guarantee creates a hard-to-replicate speed moat.")
        else:
            findings.append("[VULNERABILITY] Speed claims lack concrete sub-second benchmarks.")

        if has_guarantee:
            score += 20
            findings.append("[PASS] Clear risk reversal / guarantee builds high barrier to deflection.")
        else:
            findings.append("[VULNERABILITY] Lacks explicit risk-reversal guarantee.")

        if has_local_focus:
            score += 20
            findings.append("[PASS] Hyper-localized territory targeting prevents national dilution.")
        else:
            findings.append("[VULNERABILITY] Positioning is too broad; vulnerable to local specialist rivals.")

        verdict = "HARD_TO_BEAT" if score >= 80 else ("CONTESTABLE" if score >= 55 else "EASILY_DISRUPTED")

        return {
            "agent": self.name,
            "role": self.role,
            "score": score,
            "verdict": verdict,
            "findings": findings,
            "feedback": (
                "Positioning is defensible with clear speed, ownership, and local moats." if score >= 80
                else "Tighten guarantees and emphasize unique engineering assets to close competitive vulnerabilities."
            )
        }

class SEOSwarmOrchestrator:
    """Orchestrates multi-agent swarm evaluations across any URL or local PHP/HTML file."""
    
    def __init__(self):
        self.swarm: List[AgentPersona] = [
            HomeownerCustomerAgent(),
            TechnicalSEOArchitectAgent(),
            CROCopywriterAgent(),
            AISearchCrawlerAgent(),
            CompetitorRivalAgent()
        ]

    def audit_page(self, title: str, meta_desc: str, html_content: str) -> Dict[str, Any]:
        # Strip HTML tags to extract raw text content
        clean_text = re.sub(r'<[^>]+>', ' ', html_content)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        page_data = {
            "title": title,
            "meta_desc": meta_desc,
            "html": html_content,
            "text": clean_text
        }
        
        agent_reports = []
        total_score = 0
        
        for agent in self.swarm:
            rep = agent.evaluate(page_data)
            agent_reports.append(rep)
            total_score += rep["score"]
            
        composite_score = round(total_score / len(self.swarm), 1)
        
        # Determine overall swarm consensus
        if composite_score >= 80:
            consensus = "HIGH_AUTHORITY_PRODUCTION_READY"
        elif composite_score >= 60:
            consensus = "OPTIMIZATION_RECOMMENDED"
        else:
            consensus = "REMEDIAL_ACTION_REQUIRED"
            
        return {
            "title": title,
            "composite_score": composite_score,
            "consensus": consensus,
            "agent_evaluations": agent_reports
        }

if __name__ == "__main__":
    import sys
    
    # Test on live local template
    target_file = r"c:\WebSmitherz\websmitherz\pages\local\roofing-seo-tyler-tx.php"
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    title_match = re.search(r'\$page_title\s*=\s*["\']([^"\']+)["\']', content)
    desc_match = re.search(r'\$meta_description\s*=\s*["\']([^"\']+)["\']', content)
    
    title = title_match.group(1) if title_match else "Tyler Roofing SEO"
    desc = desc_match.group(1) if desc_match else "High performance roofing SEO for Tyler TX."
    
    orchestrator = SEOSwarmOrchestrator()
    results = orchestrator.audit_page(title, desc, content)
    
    print("=" * 70)
    print(f"SEO MULTI-AGENT SWARM SIMULATION REPORT: {title}")
    print(f"Composite Swarm Score: {results['composite_score']}/100 | Consensus: {results['consensus']}")
    print("=" * 70 + "\n")
    
    for report in results["agent_evaluations"]:
        print(f"[{report['agent']}] ({report['role']})")
        print(f"Score: {report['score']}/100 | Verdict: {report['verdict']}")
        for f in report["findings"]:
            print(f"  {f}")
        print(f"Feedback: {report['feedback']}\n")
