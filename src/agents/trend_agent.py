"""
Trend Analysis Agent
"""

from __future__ import annotations

import logging
import os

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

llm = ChatOllama(
    model=os.getenv("OLLAMA_LLM_MODEL", "llama3.2"),
    temperature=0,
)


def trend_agent(state: dict) -> dict:
    """
    Analyze payment trends using retrieved context only.
    """

    context = state.get("context", "").strip()

    confidence = state.get("confidence", 0.0)
    sources = state.get("sources", [])

    # Never allow the LLM to answer without retrieved context
    if not context:
        logger.warning("Trend agent invoked without retrieved context.")

        state["answer"] = (
            "No relevant information found in the indexed payment reports."
        )
        state["confidence"] = 0.0
        state["sources"] = []

        return state

    prompt = f"""
You are a Senior Payment Operations Analyst.

You MUST answer ONLY from the retrieved payment reports.

Rules

- Never fabricate information.
- Never assume missing values.
- Never invent payment IDs.
- Never invent dates.
- Never invent projects.
- Never invent failure counts.
- Never invent recommendations.
- If the requested information is not present, explicitly state that it is unavailable.

Retrieved Context
-----------------
{context}

Provide:

1. Top payment failure categories
2. Failure trend summary
3. Critical failure patterns
4. Business impact observed
5. Evidence used

Do NOT use outside knowledge.
"""

    try:
        logger.info("Running trend analysis.")

        response = llm.invoke(prompt)

        answer = response.content.strip()

        if sources:
            answer += "\n\nSources:\n"

            for source in sources:
                answer += f"- {source}\n"

        state["answer"] = answer
        state["confidence"] = confidence
        state["sources"] = sources

        logger.info("Trend analysis completed.")

    except Exception:
        logger.exception("Trend agent failed.")

        state["answer"] = (
            "Unable to analyze payment trends due to an internal error."
        )
        state["confidence"] = 0.0
        state["sources"] = []

    return state