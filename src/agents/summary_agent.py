"""
Executive Summary Agent for Payment AI Platform.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
MIN_CONFIDENCE = float(os.getenv("MIN_RETRIEVAL_CONFIDENCE", "70"))

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=0,
)


def _default_summary(
    confidence: float,
    sources: list[str],
    message: str,
) -> dict[str, Any]:
    """Return a default summary payload."""

    return {
        "incident_summary": message,
        "impact": "UNKNOWN",
        "root_cause_summary": "",
        "recommended_actions": [],
        "next_steps": [],
        "priority": "UNKNOWN",
        "confidence": confidence,
        "sources": sources,
    }


def summary_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Generate the executive summary from validated RCA
    and recommendations.
    """

    confidence = float(state.get("confidence", 0))
    sources = state.get("sources", [])

    # ---------------------------------------------------------
    # Skip summarization if retrieval confidence is too low
    # ---------------------------------------------------------
    if confidence < MIN_CONFIDENCE:

        logger.warning(
            "Executive summary skipped due to low confidence (%.2f%%).",
            confidence,
        )

        summary = _default_summary(
            confidence,
            sources,
            "No relevant information found in the indexed payment reports.",
        )

        state["summary"] = summary
        state["answer"] = summary["incident_summary"]
        state["confidence"] = confidence
        state["sources"] = sources

        return state

    prompt = f"""
You are an Enterprise Payment Incident Executive Summary Agent.

IMPORTANT RULES

- ONLY use the supplied Root Cause and Recommendation.
- Never use outside knowledge.
- Never invent:
    - incidents
    - payment IDs
    - dates
    - failure counts
    - recommendations

If evidence is insufficient, return:

"No relevant information found in the indexed payment reports."

Root Cause

{json.dumps(state.get("root_cause", {}), indent=2)}

Recommendation

{json.dumps(state.get("recommendation", {}), indent=2)}

Return ONLY valid JSON.

{{
    "incident_summary": "",
    "impact": "",
    "root_cause_summary": "",
    "recommended_actions": [],
    "next_steps": [],
    "priority": "HIGH"
}}
"""

    try:

        response = llm.invoke(prompt)

        content = response.content.strip()

        # Remove markdown fences if Ollama returns them
        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        result = json.loads(content)

    except json.JSONDecodeError:

        logger.exception("Failed to parse summary JSON.")

        result = _default_summary(
            confidence,
            sources,
            "Unable to generate summary.",
        )

    except Exception:

        logger.exception("Unexpected error while generating summary.")

        result = _default_summary(
            confidence,
            sources,
            "Unable to generate summary.",
        )

    # ---------------------------------------------------------
    # Populate metadata
    # ---------------------------------------------------------

    result["confidence"] = confidence
    result["sources"] = sources

    # Full structured summary
    state["summary"] = result

    # Simple string answer for the API
    state["answer"] = result.get(
        "incident_summary",
        "Unable to generate summary.",
    )

    state["confidence"] = confidence
    state["sources"] = sources

    logger.info(
        "Executive summary generated successfully (confidence %.2f%%).",
        confidence,
    )

    return state