
import requests
from ddgs import DDGS
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}


def extract_page_content(url, max_chars=10000):
    """
    Retrieve readable text from a webpage.
    Return an empty string if the page cannot be accessed.
    """

    try:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https"):
            return ""

        if not parsed_url.netloc:
            return ""

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type.lower():
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary webpage elements.
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript",
            "form"
        ]):
            element.decompose()

        main_content = (
            soup.find("article")
            or soup.find("main")
            or soup.body
            or soup
        )

        text = main_content.get_text(
            separator=" ",
            strip=True
        )

        return text[:max_chars]

    except requests.RequestException:
        return ""

    except Exception:
        return ""


def search_web(query, max_results=5):
    """
    Search the web using multiple backends with retries.
    """

    if not query or not query.strip():
        return []

    backends = ["auto", "google", "bing"]

    for backend in backends:

        for attempt in range(2):

            try:
                print(
                    f"Searching with {backend} "
                    f"(attempt {attempt + 1})..."
                )

                results = list(
                    DDGS().text(
                        query,
                        max_results=max_results,
                        backend=backend
                    )
                )

                if not results:
                    continue

                print("RESULTS FOUND:", len(results))

                search_results = []

                for result in results:

                    url = result.get("href", "")
                    snippet = result.get("body", "")

                    page_content = (
                        extract_page_content(url)
                        if url else ""
                    )

                    search_results.append({
                        "title": result.get("title", ""),
                        "url": url,
                        "snippet": snippet,
                        "content": page_content or snippet,
                        "retrieved_full_page": bool(page_content)
                    })

                return search_results

            except Exception as error:
                print(
                    f"{backend} failed: "
                    f"{type(error).__name__}: {error}"
                )

                if attempt == 0:
                    time.sleep(2)

    print("All search backends failed.")
    return []