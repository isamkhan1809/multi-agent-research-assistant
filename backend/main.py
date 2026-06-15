"""
FastAPI backend for the Multi-Agent Research Assistant.
Exposes a POST /research endpoint that orchestrates three AI agents.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Load environment variables from .env file at startup
load_dotenv()

from agents.orchestrator import run_research_pipeline


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The research question or topic to investigate.",
        examples=["What are the latest developments in quantum computing?"],
    )


class SectionsModel(BaseModel):
    overview: str
    key_findings: list[str]
    implications: str


class CitationModel(BaseModel):
    id: int
    apa: str
    url: str
    title: str


class ResearchResponse(BaseModel):
    report: str
    citations: list[CitationModel]
    sections: SectionsModel
    query: str


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "WARNING: ANTHROPIC_API_KEY is not set. "
            "The summarisation agent will fail. "
            "Create a .env file with ANTHROPIC_API_KEY=your_key."
        )
    else:
        print("ANTHROPIC_API_KEY loaded successfully.")
    yield
    print("Shutting down Research Assistant backend.")


app = FastAPI(
    title="Multi-Agent Research Assistant",
    description=(
        "A multi-agent AI system that searches the web, summarises findings "
        "with Claude, and formats APA citations — orchestrated via LangGraph."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the Vite dev server (port 5173) and production builds
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "message": "Multi-Agent Research Assistant API is running.",
        "endpoints": {
            "research": "POST /research",
            "docs": "/docs",
        },
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}


@app.post("/research", response_model=ResearchResponse, tags=["Research"])
async def research(request: ResearchRequest):
    """
    Run the multi-agent research pipeline for the given query.

    The pipeline:
    1. **Search Agent** — scrapes DuckDuckGo Lite for top 5 results
    2. **Summarise Agent** — uses Claude API to produce structured summary
    3. **Citation Agent** — formats sources as APA-style citations
    4. **Orchestrator** — coordinates all agents via LangGraph StateGraph

    Returns a full research report with structured sections and citations.
    """
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    print(f"\n[/research] Received query: {query!r}")

    try:
        result = run_research_pipeline(query)
    except Exception as e:
        print(f"[/research] Pipeline error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Research pipeline failed: {str(e)}",
        )

    if result.get("error") and not result.get("report"):
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {result['error']}",
        )

    # Normalise citations to ensure correct types
    citations = [
        CitationModel(
            id=int(c.get("id", i + 1)),
            apa=str(c.get("apa", "")),
            url=str(c.get("url", "")),
            title=str(c.get("title", "")),
        )
        for i, c in enumerate(result.get("citations", []))
    ]

    sections_raw = result.get("sections", {})
    sections = SectionsModel(
        overview=str(sections_raw.get("overview", "")),
        key_findings=[str(f) for f in sections_raw.get("key_findings", [])],
        implications=str(sections_raw.get("implications", "")),
    )

    return ResearchResponse(
        report=result.get("report", ""),
        citations=citations,
        sections=sections,
        query=query,
    )


# ---------------------------------------------------------------------------
# Entry point for direct execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
