"""
LangGraph workflow for Payment AI Platform.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from src.agents.intent_agent import intent_agent
from src.agents.search_agent import search_agent
from src.agents.rca_agent import rca_agent
from src.agents.recommendation_agent import recommendation_agent
from src.agents.summary_agent import summary_agent
from src.agents.trend_agent import trend_agent
from src.agents.unknown_agent import unknown_agent

logger = logging.getLogger(__name__)


class GraphState(TypedDict, total=False):
    """Shared state across LangGraph nodes."""

    question: str
    intent: str
    context: str
    root_cause: str
    recommendation: str
    answer: str
    summary: Dict[str, Any]

    # Production-ready fields
    sources: List[str]
    confidence: float
    metadata: Dict[str, Any]
    error: str


def route_intent(state: GraphState) -> str:
    """
    Route execution based on detected intent.
    """

    intent = state.get("intent", "").strip().upper()

    logger.info("Detected intent: %s", intent)

    routes = {
        "SEARCH": "search",
        "RCA": "search",
        "TREND": "trend",
        "SUMMARY": "summary",
        "RECOMMENDATION": "recommend",
        "GREETING": "summary",
        "UNKNOWN": "unknown",
    }

    route = routes.get(intent, "unknown")

    logger.info("Routing to node: %s", route)

    return route


workflow = StateGraph(GraphState)

# -----------------------------
# Nodes
# -----------------------------

workflow.add_node("intent", intent_agent)
workflow.add_node("search", search_agent)
workflow.add_node("rca", rca_agent)
workflow.add_node("recommend", recommendation_agent)
workflow.add_node("summary", summary_agent)
workflow.add_node("trend", trend_agent)
workflow.add_node("unknown", unknown_agent)

# -----------------------------
# Entry
# -----------------------------

workflow.set_entry_point("intent")

# -----------------------------
# Intent Routing
# -----------------------------

workflow.add_conditional_edges(
    "intent",
    route_intent,
    {
        "search": "search",
        "trend": "trend",
        "summary": "summary",
        "recommend": "recommend",
        "unknown": "unknown",
    },
)

# -----------------------------
# RCA Workflow
# -----------------------------

workflow.add_edge("search", "rca")
workflow.add_edge("rca", "recommend")
workflow.add_edge("recommend", "summary")
workflow.add_edge("summary", END)

# -----------------------------
# Trend Workflow
# -----------------------------

workflow.add_edge("trend", "summary")

# -----------------------------
# Unknown Workflow
# -----------------------------

workflow.add_edge("unknown", END)

graph = workflow.compile()