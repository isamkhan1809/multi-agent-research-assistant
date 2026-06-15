"""
Orchestrator: LangGraph StateGraph
Coordinates the three agents in a sequential pipeline:
  search_agent -> summarise_agent -> citation_agent
"""

from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, END

from .search_agent import search_agent
from .summarise_agent import summarise_agent
from .citation_agent import citation_agent


# ---------------------------------------------------------------------------
# State definition
# ---------------------------------------------------------------------------

class ResearchState(TypedDict):
    query: str
    search_results: list[dict]
    summary: dict          # {overview, key_findings, implications}
    citations: list[dict]  # [{id, apa, url, title}, ...]
    report: str            # Final compiled markdown/text report
    error: str             # Any error message


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

def run_search(state: ResearchState) -> ResearchState:
    """Node 1: Run the web search agent."""
    print(f"[orchestrator] Running search for: {state['query']!r}")
    try:
        results = search_agent(state["query"])
        return {**state, "search_results": results, "error": ""}
    except Exception as e:
        print(f"[orchestrator] Search error: {e}")
        return {**state, "search_results": [], "error": str(e)}


def run_summarise(state: ResearchState) -> ResearchState:
    """Node 2: Run the summarisation agent."""
    if not state.get("search_results"):
        return {
            **state,
            "summary": {
                "overview": "No search results available to summarise.",
                "key_findings": [],
                "implications": "",
            },
        }
    print("[orchestrator] Running summarisation agent.")
    try:
        summary = summarise_agent(state["query"], state["search_results"])
        return {**state, "summary": dict(summary), "error": ""}
    except Exception as e:
        print(f"[orchestrator] Summarise error: {e}")
        return {
            **state,
            "summary": {
                "overview": f"Summarisation failed: {e}",
                "key_findings": [],
                "implications": "",
            },
            "error": str(e),
        }


def run_citations(state: ResearchState) -> ResearchState:
    """Node 3: Run the citation formatter agent."""
    print("[orchestrator] Running citation agent.")
    try:
        citations = citation_agent(state.get("search_results", []))
        return {**state, "citations": [dict(c) for c in citations], "error": ""}
    except Exception as e:
        print(f"[orchestrator] Citation error: {e}")
        return {**state, "citations": [], "error": str(e)}


def compile_report(state: ResearchState) -> ResearchState:
    """Node 4: Compile the final report string from all agent outputs."""
    query = state.get("query", "")
    summary = state.get("summary", {})
    citations = state.get("citations", [])

    overview = summary.get("overview", "")
    key_findings = summary.get("key_findings", [])
    implications = summary.get("implications", "")

    lines = [
        f"# Research Report: {query}",
        "",
        "## Overview",
        overview,
        "",
        "## Key Findings",
    ]
    for finding in key_findings:
        lines.append(f"- {finding}")

    lines += [
        "",
        "## Implications",
        implications,
        "",
        "## Sources",
    ]
    for cite in citations:
        lines.append(f"{cite.get('id', '?')}. {cite.get('apa', '')}")

    report = "\n".join(lines)
    print("[orchestrator] Report compiled.")
    return {**state, "report": report}


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def _build_graph() -> StateGraph:
    graph = StateGraph(ResearchState)

    graph.add_node("search", run_search)
    graph.add_node("summarise", run_summarise)
    graph.add_node("citations", run_citations)
    graph.add_node("compile", compile_report)

    graph.set_entry_point("search")
    graph.add_edge("search", "summarise")
    graph.add_edge("summarise", "citations")
    graph.add_edge("citations", "compile")
    graph.add_edge("compile", END)

    return graph.compile()


_compiled_graph = _build_graph()


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def run_research_pipeline(query: str) -> dict:
    """
    Run the full multi-agent research pipeline for a query.

    Args:
        query: The research question or topic.

    Returns:
        A dict with keys: report, citations, sections (overview, key_findings, implications).
    """
    initial_state: ResearchState = {
        "query": query,
        "search_results": [],
        "summary": {},
        "citations": [],
        "report": "",
        "error": "",
    }

    final_state = _compiled_graph.invoke(initial_state)

    summary = final_state.get("summary", {})

    return {
        "report": final_state.get("report", ""),
        "citations": final_state.get("citations", []),
        "sections": {
            "overview": summary.get("overview", ""),
            "key_findings": summary.get("key_findings", []),
            "implications": summary.get("implications", ""),
        },
        "search_results": final_state.get("search_results", []),
        "error": final_state.get("error", ""),
    }
