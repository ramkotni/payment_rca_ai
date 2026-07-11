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


def rca_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Root Cause Analysis Agent.

    Generates RCA strictly from retrieved payment report context.
    """

    confidence = state.get("confidence", 0)
    context = state.get("context", "").strip()

    # Never allow hallucinations
    if not context or confidence < MIN_CONFIDENCE:
        logger.warning(
            "Skipping RCA due to insufficient retrieval confidence (%.2f%%).",
            confidence,
        )

        state["root_cause"] = {
            "issue": "No relevant information found.",
            "category": "UNKNOWN",
            "severity": "UNKNOWN",
            "root_cause": "No relevant information found in the indexed payment reports.",
            "evidence": [],
            "confidence": confidence,
            "sources": state.get("sources", []),
        }

        return state

    prompt = f"""
You are a Payment Failure Root Cause Analysis AI Agent.

IMPORTANT RULES

- Answer ONLY using the supplied context.
- Never use outside knowledge.
- Never guess.
- Never fabricate:
    - Root cause
    - Payment IDs
    - Failure counts
    - Dates
    - Recommendations
- If evidence is insufficient, return:
  "No relevant information found in the indexed payment reports."

Context:
{context}

Question:
{state.get("question")}

Return ONLY valid JSON.

{{
    "issue": "",
    "category": "",
    "severity": "",
    "root_cause": "",
    "evidence": [
        ""
    ]
}}
"""

    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)

    except json.JSONDecodeError:
        logger.exception("Failed to parse RCA JSON response.")

        result = {
            "issue": "Unable to determine.",
            "category": "UNKNOWN",
            "severity": "UNKNOWN",
            "root_cause": "Model returned invalid JSON.",
            "evidence": [],
        }

    except Exception:
        logger.exception("Unexpected error while generating RCA.")

        result = {
            "issue": "Processing error.",
            "category": "UNKNOWN",
            "severity": "UNKNOWN",
            "root_cause": "Unable to process request.",
            "evidence": [],
        }

    result["confidence"] = confidence
    result["sources"] = state.get("sources", [])

    state["root_cause"] = result

    logger.info(
        "RCA generated successfully with confidence %.2f%%.",
        confidence,
    )

    return state