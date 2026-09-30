# TenderIQ

TenderIQ helps a company decide which public tenders fit its capabilities and what eligibility gaps to resolve before bidding. This MVP includes a React dashboard, a FastAPI API, MongoDB persistence, seeded sample tenders, and a replaceable AI analysis interface. It does not scrape procurement sites yet.

## Stack

- `frontend/`: React, TypeScript, Vite
- `backend/`: FastAPI, Pydantic, PyMongo async client
- MongoDB: optional for the first run; the API remains usable with in-memory demo data if MongoDB is unavailable

## Run locally

1. Copy `.env.example` to `.env` in the repository root. No secrets are needed for the demo.
2. Start MongoDB locally if you want persistence. Without it, the API falls back to demo data.
3. Start the API:

   ```powershell
   cd backend
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -e .
   uvicorn app.main:app --reload
   ```

4. In a second terminal, start the frontend:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

5. Open http://localhost:5173. API docs are at http://localhost:8000/docs.

The frontend reads `VITE_API_BASE_URL` (defaults to `http://localhost:8000/api/v1`). Backend settings are loaded from environment variables or the repository root `.env` file. Set `MONGODB_URI` and `MONGODB_DATABASE` to use a MongoDB deployment; never commit real credentials.

## API overview

- `GET /api/v1/health` — API and database status
- `GET /api/v1/tenders` — list/filter tenders (`q`, `category`, `status`)
- `GET /api/v1/tenders/{tender_id}` — tender details and company-fit analysis
- `POST /api/v1/tenders/{tender_id}/analyze` — analyze against a company profile
- `GET /api/v1/pipeline` — list saved tenders with their bid stages and notes
- `PUT /api/v1/pipeline/{tender_id}` — save a tender or update its stage (`Interested`, `Preparing`, `Submitted`, `Won`, `Lost`) and notes
- `DELETE /api/v1/pipeline/{tender_id}` — remove a tender from the pipeline
- `GET /api/v1/company` — current company profile
- `PUT /api/v1/company` — create or update the company profile

Seed records are inserted into MongoDB only when the tender collection is empty. In demo fallback mode, changes live only for the backend process lifetime.

## Architecture

`api/` owns HTTP validation and serialization; `services/` owns tender, profile, and analysis behavior; `repositories/` handles persistence; `ingestion/` is the future adapter boundary for EPADS and other procurement sources. The current AI service is a deterministic rules-based implementation of an `AnalysisService` protocol, so a hosted model can be introduced without coupling provider code to routes or data models. Treat scores as triage guidance, not a legal eligibility determination.

## MVP scope and next steps

The dashboard includes search, category/status filters, deadline and fit summaries, tender detail analysis, an editable company profile, and a saved bid pipeline with notes. Tender data is clearly marked as sample data. Pipeline records persist in MongoDB when available and otherwise last for the backend process lifetime. Before real use with company data, add authentication and organization-level access controls, then add source-specific ingestion adapters, durable job scheduling, audit history, and a reviewed model/provider integration.
