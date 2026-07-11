"""
Intent Classification Agent
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

llm = ChatOllama(
    model=os.getenv("OLLAMA_LLM_MODEL", "llama3.2"),
    temperature=0,
)

RULES: Dict[str, List[str]] = {
    "RCA": [
        "why",
        "root cause",
        "failed",
        "failure",
        "reason",
        "error",
        "timeout",
        "declined",
    ],
    "TREND": [
        "trend",
        "statistics",
        "report",
        "last month",
        "last quarter",
        "dashboard",
    ],
    "SUMMARY": [
        "summary",
        "summarize",
        "overview",
        "executive summary",
    ],
    "RECOMMENDATION": [
        "recommend",
        "recommendation",
        "solution",
        "fix",
        "prevent",
        "improve",
        "best practice",
    ],
    "GREETING": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ],
}

VALID_INTENTS = {
    "RCA",
    "TREND",
    "SUMMARY",
    "RECOMMENDATION",
    "GREETING",
    "UNKNOWN",
}


def _rule_based_intent(question: str) -> str | None:
    """Return an intent using keyword rules."""

    q = question.lower()

    for intent, keywords in RULES.items():
        if any(keyword in q for keyword in keywords):
            return intent

    return None


def intent_agent(state: dict) -> dict:
    """
    Detect the user's intent using rule-based routing first,
    then fall back to the LLM if needed.
    """

    question = state.get("question", "").strip()

    if not question:
        state["intent"] = "UNKNOWN"
        logger.warning("Received empty question.")
        return state

    intent = _rule_based_intent(question)

    if intent:
        logger.info("Rule-based intent detected: %s", intent)
        state["intent"] = intent
        return state

    prompt = f"""
You are an intent classification model for a Payment Operations AI platform.

Your job is ONLY to classify the user's question.

Supported intents:

RCA
TREND
SUMMARY
RECOMMENDATION
GREETING
UNKNOWN

Rules:

- Return ONLY one of the above labels.
- Never explain your answer.
- If the question is unrelated to payment operations,
  return UNKNOWN.

Question:
{question}
"""

    try:
        response = llm.invoke(prompt)

        intent = response.content.strip().upper()

        if intent not in VALID_INTENTS:
            logger.warning("Invalid intent returned: %s", intent)
            intent = "UNKNOWN"

    except Exception:
        logger.exception("Intent classification failed.")
        intent = "UNKNOWN"

    state["intent"] = intent

    logger.info("Detected intent: %s", intent)

    return state