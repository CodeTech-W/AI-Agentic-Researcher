from langchain_core.tools import tool


# =========================================
# Dummy Research Papers
# =========================================

def search_arxiv_papers(topic: str):

    papers = {
        "entries": [
            {
                "title": f"Latest Research Trends in {topic}",
                "summary": f"This paper discusses recent advancements, applications, and future scope of {topic}. The study highlights AI-driven methodologies and modern research techniques.",
                "authors": ["John Smith", "David Lee"],
                "categories": ["cs.AI"],
                "pdf": "https://arxiv.org/"
            },
            {
                "title": f"AI Agentic Systems for {topic}",
                "summary": f"This research explores how autonomous AI agents improve efficiency in {topic} using large language models and intelligent workflows.",
                "authors": ["Alice Brown"],
                "categories": ["cs.LG"],
                "pdf": "https://arxiv.org/"
            }
        ]
    }

    return papers


# =========================================
# LangChain Tool
# =========================================

@tool
def arxiv_search(topic: str) -> list[dict]:
    """
    Search research papers about a topic
    """

    print("ARXIV Agent called")
    print(f"Searching papers about: {topic}")

    papers = search_arxiv_papers(topic)

    print(f"Found {len(papers['entries'])} papers")

    return papers