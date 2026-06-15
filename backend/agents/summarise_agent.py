"""
Agent 2: Summarisation Agent
Uses Anthropic Claude API to produce a structured summary from search results.
Reads ANTHROPIC_API_KEY from the environment.
"""

import json
import os
from typing import TypedDict

import anthropic
from dotenv import load_dotenv

load_dotenv()


class SummaryOutput(TypedDict):
    overview: str
    key_findings: list[str]
    implications: str


def summarise_agent(query: str, search_results: list[dict]) -> SummaryOutput:
    """
    Summarise the search results into structured sections using Claude.

    Args:
        query: The original research query.
        search_results: List of dicts with title, url, snippet fields.

    Returns:
        SummaryOutput with overview, key_findings, and implications.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Please add it to your .env file or environment variables."
        )

    client = anthropic.Anthropic(api_key=api_key)

    # Build the context from search results
    results_text = "\n\n".join(
        f"[{i + 1}] Title: {r.get('title', 'N/A')}\n"
        f"    URL: {r.get('url', 'N/A')}\n"
        f"    Snippet: {r.get('snippet', 'N/A')}"
        for i, r in enumerate(search_results)
    )

    system_prompt = (
        "You are an expert research assistant. Your job is to synthesize web search "
        "results into a clear, structured research summary. You must respond with "
        "valid JSON only — no markdown fences, no extra text.\n\n"
        "The JSON must have exactly these fields:\n"
        "{\n"
        '  "overview": "<2-3 sentence overview of the topic>",\n'
        '  "key_findings": ["<finding 1>", "<finding 2>", "<finding 3>", ...],\n'
        '  "implications": "<1-2 sentence discussion of broader implications>"\n'
        "}\n\n"
        "Base your summary only on the provided search results."
    )

    user_prompt = (
        f"Research Query: {query}\n\n"
        f"Search Results:\n{results_text}\n\n"
        "Please synthesize these results into a structured JSON summary."
    )

    print(f"[summarise_agent] Calling Claude for query: {query!r}")

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw_text = message.content[0].text.strip()

    # Strip markdown fences if model added them despite instructions
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"[summarise_agent] JSON parse error: {e}\nRaw: {raw_text}")
        # Return a safe fallback
        parsed = {
            "overview": raw_text[:500] if raw_text else "Summary not available.",
            "key_findings": ["Could not parse structured findings."],
            "implications": "Please try again.",
        }

    return SummaryOutput(
        overview=parsed.get("overview", ""),
        key_findings=parsed.get("key_findings", []),
        implications=parsed.get("implications", ""),
    )
