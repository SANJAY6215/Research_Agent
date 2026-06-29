from langchain.tools import tool
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    try:
        output = []
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        for r in results:
            output.append(
                f"Title: {r.get('title', '')}\n"
                f"URL: {r.get('href', '')}\n"
                f"Snippet: {r.get('body', '')}\n"
            )

        return "\n----------------\n".join(output)

    except Exception as e:
        return f"Search Error: {str(e)}"

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL."""
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:5000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


