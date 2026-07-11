from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from agents.search_agent import search_agent
from agents.rca_agent import rca_agent
from agents.recommendation_agent import recommendation_agent
from agents.summary_agent import summary_agent
from agents.intent_agent import intent_agent
from agents.trend_agent import trend_agent


class GraphState(TypedDict):

    question: str
    intent: str
    context: str
    root_cause: str
    recommendation: str
    answer: str


# ----------------------------
# Intent Router
# ----------------------------

from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.intent_agent import intent_agent
from agents.search_agent import search_agent
from agents.rca_agent import rca_agent
from agents.recommendation_agent import recommendation_agent
from agents.summary_agent import summary_agent
from agents.trend_agent import trend_agent
from agents.unknown_agent import unknown_agent


class GraphState(TypedDict):

    question: str
    intent: str
    context: str
    root_cause: str
    recommendation: str
    answer: str


# ------------------------------------
# Intent Router
# ------------------------------------
def route_intent(state: GraphState):

    intent = state.get("intent", "").upper()

    print(f"Routing to: {intent}")

    if intent == "RCA":
        return "search"

    elif intent == "TREND":
        return "trend"

    elif intent == "SUMMARY":
        return "summary"

    elif intent == "RECOMMENDATION":
        return "recommend"

    # Default
    #return "search"
    elif intent == "GREETING":
        return "greeting"

    elif intent == "SEARCH":
        return "search"

    elif intent == "UNKNOWN":
        return "unknown"


workflow = StateGraph(GraphState)

# ----------------------------
# Nodes
# ----------------------------

workflow.add_node(
    "intent",
    intent_agent
)

workflow.add_node(
    "search",
    search_agent
)

workflow.add_node(
    "rca",
    rca_agent
)

workflow.add_node(
    "recommend",
    recommendation_agent
)

workflow.add_node(
    "summary",
    summary_agent
)

workflow.add_node(
    "trend",
    trend_agent
)

workflow.add_node(
    "unknown",
    unknown_agent
)

# ----------------------------
# Entry Point
# ----------------------------

workflow.set_entry_point("intent")

# ----------------------------
# Conditional Routing
# ----------------------------

workflow.add_conditional_edges(
    "intent",
    route_intent,
    {
        "search": "search",
        "trend": "trend",
        "summary": "summary",
        "recommend": "recommend",
        "UNKNOWN": "unknown"
    }
)

# ----------------------------
# RCA Flow
# ----------------------------

workflow.add_edge(
    "search",
    "rca"
)

workflow.add_edge(
    "rca",
    "recommend"
)

workflow.add_edge(
    "recommend",
    "summary"
)

workflow.add_edge(
    "summary",
    END
)

# ----------------------------
# Trend Flow
# ----------------------------

#workflow.add_edge(
 #   "trend",
  #  END
#)

workflow.add_edge(
    "trend",
    "summary"
)

workflow.add_edge(
    "unknown",
    END
)


graph = workflow.compile()