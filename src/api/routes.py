"""
API routes for the Payment AI Platform.
"""

from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from graph import graph

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Payment AI"])


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)


class QueryResponse(BaseModel):
    answer: str
    confidence: float = 0.0
    sources: List[str] = []


@router.get("/health")
def health() -> dict:
    """
    Health check endpoint.
    """
    return {
        "status": "UP",
        "service": "payment-ai-platform",
    }


@router.post(
    "/ask",
    response_model=QueryResponse,
)
def ask(request: QueryRequest) -> QueryResponse:
    """
    Execute the LangGraph workflow.
    """

    logger.info("Received question: %s", request.question)

    try:
        result = graph.invoke(
            {
                "question": request.question
            }
        )

        answer = result.get(
            "answer",
            "No relevant information found in the indexed payment reports."
        )

        confidence = float(result.get("confidence", 0.0))
        sources = result.get("sources", [])

        logger.info("Request processed successfully.")

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
        )

    except Exception:
        logger.exception("Error while processing request.")

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )