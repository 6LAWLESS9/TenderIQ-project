from app.repositories.memory import MemoryStore


class TenderRepository:
    def __init__(self, db, memory: MemoryStore):
        self.db, self.memory = db, memory

    async def list(self, q: str | None = None, category: str | None = None, status: str | None = None):
        if self.db is not None:
            query = {}
            if category and category != "All categories": query["category"] = category
            if status and status != "all": query["status"] = status
            if q: query["$or"] = [{key: {"$regex": q, "$options": "i"}} for key in ("title", "organization", "summary", "category")]
            docs = await self.db.tenders.find(query, {"_id": 0}).sort("deadline", 1).to_list(200)
            return docs
        docs = self.memory.tenders
        if category and category != "All categories": docs = [x for x in docs if x["category"] == category]
        if status and status != "all": docs = [x for x in docs if x["status"] == status]
        if q:
            term = q.casefold()
            docs = [x for x in docs if term in " ".join([x["title"], x["organization"], x["summary"], x["category"]]).casefold()]
        return sorted(docs, key=lambda x: x["deadline"])

    async def get(self, tender_id: str):
        if self.db is not None:
            return await self.db.tenders.find_one({"id": tender_id}, {"_id": 0})
        return next((x for x in self.memory.tenders if x["id"] == tender_id), None)
