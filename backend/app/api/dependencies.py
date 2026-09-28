from fastapi import Request

from app.repositories.company import CompanyRepository
from app.repositories.tenders import TenderRepository


def tender_repository(request: Request) -> TenderRepository:
    return TenderRepository(request.app.state.db, request.app.state.memory)


def company_repository(request: Request) -> CompanyRepository:
    return CompanyRepository(request.app.state.db, request.app.state.memory)
