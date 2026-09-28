from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.api.dependencies import company_repository, tender_repository
from app.models.company import CompanyProfile
from app.models.tender import Tender, TenderWithAnalysis
from app.repositories.company import CompanyRepository
from app.repositories.tenders import TenderRepository
from app.services.analysis import RulesAnalysisService

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    return {"status": "ok", "database": "connected" if request.app.state.db is not None else "demo_fallback"}


@router.get("/tenders", response_model=list[TenderWithAnalysis])
async def list_tenders(q: str | None = None, category: str | None = None, status: str | None = Query(default=None, pattern="^(open|closing_soon|closed|all)$"), repo: TenderRepository = Depends(tender_repository)):
    docs = await repo.list(q=q, category=category, status=status)
    result = []
    for doc in docs:
        doc = {**doc, "analysis": None}
        result.append(TenderWithAnalysis.model_validate(doc))
    return result


@router.get("/tenders/{tender_id}", response_model=TenderWithAnalysis)
async def get_tender(tender_id: str, repo: TenderRepository = Depends(tender_repository), companies: CompanyRepository = Depends(company_repository)):
    doc = await repo.get(tender_id)
    if not doc: raise HTTPException(status_code=404, detail="Tender not found")
    analysis = await RulesAnalysisService().analyze(Tender.model_validate(doc), await companies.get())
    return TenderWithAnalysis.model_validate({**doc, "analysis": analysis.model_dump(mode="json")})


@router.post("/tenders/{tender_id}/analyze", response_model=object)
async def analyze_tender(tender_id: str, request: Request, repo: TenderRepository = Depends(tender_repository), companies: CompanyRepository = Depends(company_repository)):
    doc = await repo.get(tender_id)
    if not doc: raise HTTPException(status_code=404, detail="Tender not found")
    analysis = await RulesAnalysisService().analyze(Tender.model_validate(doc), await companies.get())
    if request.app.state.db is not None:
        await request.app.state.db.analyses.insert_one({"tender_id": tender_id, **analysis.model_dump(mode="json")})
    return analysis


@router.get("/company", response_model=CompanyProfile)
async def get_company(repo: CompanyRepository = Depends(company_repository)):
    return await repo.get()


@router.put("/company", response_model=CompanyProfile)
async def update_company(profile: CompanyProfile, repo: CompanyRepository = Depends(company_repository)):
    if not profile.name.strip(): raise HTTPException(status_code=422, detail="Company name is required")
    return await repo.save(profile)
