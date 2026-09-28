from app.repositories.memory import demo_tenders


async def seed_database(db) -> None:
    if await db.tenders.count_documents({}) == 0:
        await db.tenders.insert_many(demo_tenders())
    if await db.company_profiles.count_documents({}) == 0:
        await db.company_profiles.insert_one({"_id": "default"})
