from fastapi import APIRouter
from pydantic import BaseModel

from src.graph import graph

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.get("/health")
def health():
    return {
        "status": "UP"
    }


@router.post("/ask")
def ask(request: QueryRequest):

    result = graph.invoke(
        {
            "question": request.question
        }
    )

    return {
        "answer": result["answer"]
    }