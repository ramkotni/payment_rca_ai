from fastapi import FastAPI
from pydantic import BaseModel

from graph import graph

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):

    result = graph.invoke(
        {
            "question": query.question
        }
    )

    return {
        "answer": result["answer"]
    }

@app.get("/health")
def health():
    return {
        "status":"UP"
    }