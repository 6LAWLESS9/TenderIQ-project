from datetime import datetime, timezone

from app.models.company import CompanyProfile
from app.repositories.memory import MemoryStore


class CompanyRepository:
    def __init__(self, db, memory: MemoryStore): self.db, self.memory = db, memory

    async def get(self) -> CompanyProfile:
        if self.db is not None:
            doc = await self.db.company_profiles.find_one({"_id": "default"})
            if doc and doc.get("name"):
                doc.pop("_id", None)
                return CompanyProfile.model_validate(doc)
        return self.memory.company

    async def save(self, profile: CompanyProfile) -> CompanyProfile:
        updated = profile.model_copy(update={"updated_at": datetime.now(timezone.utc)})
        self.memory.company = updated
        if self.db is not None:
            await self.db.company_profiles.replace_one({"_id": "default"}, {"_id": "default", **updated.model_dump(mode="json")}, upsert=True)
        return updated
