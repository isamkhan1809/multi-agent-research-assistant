"""
Agent 1: Web Search Agent
Uses DuckDuckGo Lite HTML scraping to retrieve top 5 search results.
No API key required.
"""

import requests
from bs4 import BeautifulSoup
from typing import TypedDict


class SearchResult(TypedDict):
    title: str
    url: str
    snippet: str


def search_agent(query: str) -> list[SearchResult]:
    """
    Search DuckDuckGo Lite for the given query and return top 5 results.

    Args:
        query: The search query string.

    Returns:
        A list of up to 5 SearchResult dicts with title, url, snippet.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.post(
            "https://lite.duckduckgo.com/lite/",
            data={"q": query, "kl": "us-en"},
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[search_agent] Request failed: {e}")
        return _fallback_results(query)

    soup = BeautifulSoup(response.text, "html.parser")
    results: list[SearchResult] = []

    # DuckDuckGo Lite result structure:
    # Each result is a set of <tr> rows containing the link and snippet
    result_links = soup.select("a.result-link")
    result_snippets = soup.select("td.result-snippet")

    for i, (link_tag, snippet_tag) in enumerate(zip(result_links, result_snippets)):
        if i >= 5:
            break

        title = link_tag.get_text(strip=True)
        url = link_tag.get("href", "")
        snippet = snippet_tag.get_text(strip=True)

        if title and url:
            results.append(
                SearchResult(title=title, url=url, snippet=snippet)
            )

    # Fallback: try alternate selectors if the above yielded nothing
    if not results:
        results = _parse_alternate(soup, query)

    if not results:
        results = _fallback_results(query)

    print(f"[search_agent] Found {len(results)} results for: {query!r}")
    return results


def _parse_alternate(soup: BeautifulSoup, query: str) -> list[SearchResult]:
    """Try alternate parsing strategy for DuckDuckGo Lite HTML variants."""
    results: list[SearchResult] = []
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        i = 0
        while i < len(rows) and len(results) < 5:
            row = rows[i]
            link = row.find("a")
            if link and link.get("href", "").startswith("http"):
                title = link.get_text(strip=True)
                url = link["href"]
                # Next row usually has the snippet
                snippet = ""
                if i + 1 < len(rows):
                    snippet = rows[i + 1].get_text(strip=True)
                if title and url:
                    results.append(
                        SearchResult(title=title, url=url, snippet=snippet)
                    )
                i += 2
            else:
                i += 1

    return results


def _fallback_results(query: str) -> list[SearchResult]:
    """Return placeholder results when scraping fails."""
    return [
        SearchResult(
            title=f"Search result for: {query}",
            url="https://duckduckgo.com/?q=" + query.replace(" ", "+"),
            snippet=(
                f"No live results could be fetched for '{query}'. "
                "This may be due to network restrictions or rate limiting. "
                "Please try again or check your internet connection."
            ),
        )
    ]
