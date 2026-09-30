from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from app.api.dependencies import company_repository, tender_repository
from app.models.company import CompanyProfile
from app.models.tender import Tender, TenderWithAnalysis
from app.repositories.company import CompanyRepository
from app.repositories.tenders import TenderRepository
from app.services.analysis import RulesAnalysisService

router = APIRouter()


class PipelineUpdate(BaseModel):
    status: str = Field(pattern="^(Interested|Preparing|Submitted|Won|Lost)$")
    notes: str = Field(default="", max_length=5000)


@router.get("/pipeline")
async def list_pipeline(request: Request, repo: TenderRepository = Depends(tender_repository)):
    records = await request.app.state.db.pipeline.find({}, {"_id": 0}).to_list(500) if request.app.state.db is not None else list(request.app.state.memory.pipeline.values())
    result = []
    for record in records:
        tender = await repo.get(record["tender_id"])
        if tender:
            result.append({**record, "tender": tender})
    return result


@router.put("/pipeline/{tender_id}")
async def update_pipeline(tender_id: str, update: PipelineUpdate, request: Request, repo: TenderRepository = Depends(tender_repository)):
    if not await repo.get(tender_id):
        raise HTTPException(status_code=404, detail="Tender not found")
    previous = await request.app.state.db.pipeline.find_one({"tender_id": tender_id}, {"_id": 0}) if request.app.state.db is not None else request.app.state.memory.pipeline.get(tender_id)
    record = {"tender_id": tender_id, "status": update.status, "notes": update.notes, "saved_at": previous.get("saved_at") if previous else datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat()}
    if request.app.state.db is not None:
        await request.app.state.db.pipeline.replace_one({"tender_id": tender_id}, record, upsert=True)
    else:
        request.app.state.memory.pipeline[tender_id] = record
    return record


@router.delete("/pipeline/{tender_id}")
async def remove_pipeline(tender_id: str, request: Request):
    if request.app.state.db is not None:
        await request.app.state.db.pipeline.delete_one({"tender_id": tender_id})
    else:
        request.app.state.memory.pipeline.pop(tender_id, None)
    return {"ok": True}


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
