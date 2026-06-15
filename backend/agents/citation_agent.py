"""
Agent 3: Citation Formatter Agent
Formats search results as APA-style citations.
"""

import re
from datetime import date
from typing import TypedDict
from urllib.parse import urlparse


class Citation(TypedDict):
    id: int
    apa: str
    url: str
    title: str


def citation_agent(search_results: list[dict]) -> list[Citation]:
    """
    Format a list of search results as APA-style citations.

    APA 7th edition format for web sources:
    Author, A. A. (Year, Month Day). Title of webpage. Site Name. URL

    When author/date are unknown (common for web snippets), we use the
    title and domain name as a best-effort citation.

    Args:
        search_results: List of dicts with title, url, snippet fields.

    Returns:
        List of Citation dicts with id, apa, url, title.
    """
    citations: list[Citation] = []
    retrieval_date = date.today().strftime("%B %d, %Y")

    for i, result in enumerate(search_results, start=1):
        title = result.get("title", "Untitled").strip()
        url = result.get("url", "").strip()

        site_name = _extract_site_name(url)
        short_title = _clean_title(title)

        # APA format for web page with unknown author:
        # Title of webpage. (n.d. or Year). Site Name. Retrieved Month Day, Year, from URL
        apa = (
            f"{short_title}. (n.d.). {site_name}. "
            f"Retrieved {retrieval_date}, from {url}"
        )

        citations.append(
            Citation(id=i, apa=apa, url=url, title=title)
        )

    print(f"[citation_agent] Formatted {len(citations)} citations.")
    return citations


def _extract_site_name(url: str) -> str:
    """Extract a human-readable site name from a URL."""
    if not url:
        return "Unknown Source"
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        # Remove www. prefix
        hostname = re.sub(r"^www\.", "", hostname)
        # Capitalise the domain name portion
        parts = hostname.split(".")
        if parts:
            return parts[0].capitalize()
        return hostname
    except Exception:
        return "Unknown Source"


def _clean_title(title: str) -> str:
    """Trim and sentence-case the title for APA formatting."""
    if not title:
        return "Untitled"
    # APA titles: only first word and proper nouns capitalised
    # We do a simple sentence-case here
    cleaned = title.strip()
    if len(cleaned) > 0:
        cleaned = cleaned[0].upper() + cleaned[1:].lower()
    # Restore acronyms and common proper nouns is beyond scope; return as-is
    return title.strip()
