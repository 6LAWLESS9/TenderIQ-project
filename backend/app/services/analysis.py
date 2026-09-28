from datetime import datetime, timezone
from typing import Protocol

from app.models.company import CompanyProfile
from app.models.tender import AnalysisResult, Tender


class AnalysisService(Protocol):
    async def analyze(self, tender: Tender, company: CompanyProfile) -> AnalysisResult: ...


class RulesAnalysisService:
    """Deterministic MVP analyzer; replace via dependency injection with a reviewed model provider."""
    async def analyze(self, tender: Tender, company: CompanyProfile) -> AnalysisResult:
        text = " ".join([tender.title, tender.summary, tender.category, *tender.requirements]).casefold()
        company_terms = [company.industry, *company.services, *company.certifications, *company.past_projects]
        matched = [term for term in company_terms if term.strip() and any(word in text for word in term.casefold().split() if len(word) > 3)]
        strengths = list(dict.fromkeys([f"Relevant capability: {term}" for term in matched[:4]]))
        gaps = []
        for requirement in tender.requirements:
            req = requirement.casefold()
            if any(k in req for k in ("years", "experience")) and company.years_experience < 5:
                gaps.append(f"Confirm experience requirement: {requirement}")
            elif any(k in req for k in ("certification", "certified", "authorization")):
                if not company.certifications: gaps.append(f"Certification evidence may be required: {requirement}")
            elif any(k in req for k in ("three", "3 similar", "comparable")) and not company.past_projects:
                gaps.append(f"Add comparable project evidence: {requirement}")
        score = max(20, min(94, 48 + len(strengths) * 11 - len(gaps) * 9))
        recommendation = "strong_match" if score >= 75 else "review" if score >= 50 else "low_match"
        return AnalysisResult(score=score, recommendation=recommendation, strengths=strengths or ["Company profile is saved and ready to compare"], gaps=gaps, explanation="A preliminary rules-based comparison of tender wording and the saved company profile. Verify every requirement against the official tender documents.", analyzed_at=datetime.now(timezone.utc))
