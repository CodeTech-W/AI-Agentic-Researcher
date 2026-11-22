# ==========================================
# AI Researcher (Groq + Ollama Only)
# ==========================================

import os
from dotenv import load_dotenv

from groq import Groq
import ollama

from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph

from arxiv_tool import arxiv_search
from write_pdf import render_latex_pdf

from langchain_core.messages import HumanMessage, AIMessage

# ==========================================
# Load ENV
# ==========================================

load_dotenv()

# ==========================================
# Groq Client
# ==========================================

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================
# State
# ==========================================

class State(TypedDict):
    messages: Annotated[list, add_messages]

# ==========================================
# Main Research Function
# ==========================================

def generate_research(state: State):

    # ✅ FIXED: correct way to access message
    user_input = state["messages"][-1].content

    print("\nSearching arXiv...\n")

    papers = arxiv_search.invoke(user_input)

    summaries = ""

    for paper in papers["entries"]:
        summaries += f"""
Title:
{paper['title']}

Summary:
{paper['summary']}

"""

    # ======================================
    # GROQ ANALYSIS
    # ======================================

    print("\nUsing Groq...\n")

    groq_response = groq_client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze these research papers and create structured research notes.

{summaries}
"""
            }
        ]
    )

    research_notes = groq_response.choices[0].message.content

    # ======================================
    # OLLAMA FINAL PAPER GENERATION
    # ======================================

    print("\nUsing Ollama for final paper...\n")

    ollama_response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": f"""
Generate concise IEEE-style research paper.

Topic:
{user_input}

Research Notes:
{research_notes}

Format:
- Abstract
- Introduction
- Literature Review
- Methodology
- Results
- Conclusion
- Future Work
- References

IMPORTANT:
Do NOT include documentclass or LaTeX wrapper.
Only content sections.
"""
            }
        ]
    )

    latex_content = ollama_response["message"]["content"]

    # ======================================
    # PDF GENERATION
    # ======================================

    print("\nGenerating PDF...\n")

    pdf_path = render_latex_pdf.invoke(latex_content)

    # ======================================
    # FINAL OUTPUT (LangGraph format FIXED)
    # ======================================

    return {
        "messages": [
            AIMessage(content=f"""
Research Paper Generated Successfully.

PDF Path:
{pdf_path}

Research Content:

{latex_content}
""")
        ]
    }

# ==========================================
# WORKFLOW
# ==========================================

workflow = StateGraph(State)

workflow.add_node("researcher", generate_research)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", END)

graph = workflow.compile()

config = {
    "configurable": {
        "thread_id": "research-thread"
    }
}