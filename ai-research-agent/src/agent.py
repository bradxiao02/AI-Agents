from src.search import search_web
from src.researcher import analyze_research
from src.memory import initialize_database, save_research
from src.citations import format_references

def conduct_research(query, max_results=5, mode="general"):
    """Execute the complete research workflow."""

    if not query or not query.strip():
        raise ValueError("Research topic cannot be empty.")

    initialize_database()

    results = search_web(query, max_results=max_results)

    if not results:
        return {
            "success": False,
            "error": "No search results found.",
            "sources": [],
            "report": ""
        }

    report = analyze_research(query, results, mode=mode)

    references = format_references(results)

    report = f"{report}\n\n{references}"

    if report.startswith("AI analysis error:"):
        return {
            "success": False,
            "error": report,
            "sources": results,
            "report": ""
        }

    save_research(query, report)

    return {
        "success": True,
        "topic": query,
        "sources": results,
        "report": report
    }


def main():
    initialize_database()

    print("\n===== AI RESEARCH AGENT =====")

    while True:
        query = input("\nResearch topic (or 'exit'): ").strip()

        if query.lower() in ("exit", "quit"):
            print("Research session ended.")
            break

        try:
            print("\n[Agent] Conducting research...")

            result = conduct_research(query)

            if result["success"]:
                print("\n" + result["report"])
                print(f"\n[Agent] Analysed {len(result['sources'])} sources.")
            else:
                print(result["error"])

        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
