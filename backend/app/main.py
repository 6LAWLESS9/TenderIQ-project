from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.database import lifespan

app = FastAPI(title=settings.app_name, version="0.1.0", description="Tender matching and company fit analysis API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=["GET", "PUT", "POST", "DELETE"], allow_headers=["*"])
app.include_router(router, prefix=settings.api_prefix)
