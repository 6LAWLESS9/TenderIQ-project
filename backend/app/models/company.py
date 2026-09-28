from datetime import datetime

from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    name: str = ""
    industry: str = ""
    services: list[str] = Field(default_factory=list)
    years_experience: int = Field(default=0, ge=0)
    employee_count: int = Field(default=0, ge=0)
    annual_turnover_pkr: int | None = Field(default=None, ge=0)
    certifications: list[str] = Field(default_factory=list)
    past_projects: list[str] = Field(default_factory=list)
    location: str = ""
    updated_at: datetime | None = None
