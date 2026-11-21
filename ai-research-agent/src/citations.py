
from urllib.parse import urlparse


def generate_references(search_results):
    """
    Generate a reference list from retrieved search results.
    """

    references = []

    for index, source in enumerate(search_results, start=1):

        title = source.get("title") or "Untitled source"
        url = source.get("url") or "URL unavailable"

        domain = urlparse(url).netloc if urlparse(url).scheme else ""

        retrieval_status = (
            "Full-page content retrieved"
            if source.get("retrieved_full_page")
            else "Search snippet only"
        )

        references.append({
            "number": index,
            "title": title,
            "url": url,
            "domain": domain,
            "retrieval_status": retrieval_status
        })

    return references


def format_references(search_results):
    """
    Format references into a readable Markdown list.
    """

    references = generate_references(search_results)

    if not references:
        return "No references available."

    output = "## References\n\n"

    for reference in references:

        output += (
            f"[{reference['number']}] "
            f"**{reference['title']}**\n\n"
            f"Website: {reference['domain'] or 'Unknown'}\n\n"
            f"URL: {reference['url']}\n\n"
            f"Retrieval status: {reference['retrieval_status']}\n\n"
        )

    return output
