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


def recommendation_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Generates recommendations ONLY from the retrieved payment reports.

    Never invent recommendations.
    """

    confidence = state.get("confidence", 0)
    sources = state.get("sources", [])
    root_cause = state.get("root_cause", {})

    if confidence < MIN_CONFIDENCE:

        logger.warning(
            "Recommendation skipped due to low confidence (%.2f%%)",
            confidence,
        )

        state["recommendation"] = {
            "recommendations": [],
            "message": "No relevant information found in the indexed payment reports.",
            "confidence": confidence,
            "sources": sources,
        }

        return state

    prompt = f"""
You are an Enterprise Payment Operations Recommendation Agent.

IMPORTANT RULES

- ONLY use the supplied Root Cause.
- Never use outside knowledge.
- Never guess.
- Never fabricate actions.
- Never fabricate operational procedures.
- Never invent configuration changes.
- Recommendations MUST be directly supported by the supplied evidence.
- If the evidence is insufficient, return an empty recommendation list.

Root Cause

{json.dumps(root_cause, indent=2)}

Return ONLY valid JSON.

Format

{{
    "recommendations": [
        {{
            "priority": "HIGH",
            "action": "",
            "reason": ""
        }}
    ]
}}
"""

    try:

        response = llm.invoke(prompt)

        result = json.loads(response.content)

    except json.JSONDecodeError:

        logger.exception("Recommendation JSON parsing failed.")

        result = {
            "recommendations": []
        }

    except Exception:

        logger.exception("Recommendation generation failed.")

        result = {
            "recommendations": []
        }

    result["confidence"] = confidence
    result["sources"] = sources

    state["recommendation"] = result

    logger.info(
        "Recommendation generated successfully (confidence %.2f%%).",
        confidence,
    )

    return state