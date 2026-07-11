"""
FastAPI entry point for the Payment AI Platform.
"""

from __future__ import annotations

import logging
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.graph import graph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Payment AI Platform",
    version="1.0.0",
    description="AI-powered Payment Operations Assistant",
)


class Query(BaseModel):
    question: str = Field(..., min_length=3)


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]


@app.post(
    "/ask",
    response_model=QueryResponse,
    tags=["Payment AI"],
)
def ask(query: Query) -> QueryResponse:
    """
    Execute the LangGraph workflow.
    """

    logger.info("Received question: %s", query.question)

    try:
        result = graph.invoke(
            {
                "question": query.question
            }
        )

        answer = result.get(
            "answer",
            "No relevant information found in the indexed payment reports."
        )

        confidence = float(result.get("confidence", 0.0))

        sources = result.get("sources", [])

        logger.info(
            "Graph execution completed successfully."
        )

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
        )

    except Exception:
        logger.exception("Graph execution failed.")

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )


@app.get(
    "/health",
    tags=["Health"],
)
def health() -> dict:
    """
    Health endpoint.
    """

    return {
        "status": "UP",
        "service": "payment-ai-platform",
        "version": "1.0.0",
    }