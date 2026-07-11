from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def unknown_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Handles questions that are outside the supported Payment AI domain.
    """

    message = (
        "I can only help with payment operations, incidents, root cause analysis, "
        "trends, recommendations, and payment-related reports. "
        "Please ask a payment-related question."
    )

    state["answer"] = message

    state["confidence"] = 0.0

    state["sources"] = []

    state["metadata"] = {
        "intent": "UNKNOWN"
    }

    logger.info("Unknown intent handled.")

    return state