from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

logger = logging.getLogger(__name__)

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)

CHROMA_DB_PATH = Path(
    os.getenv(
        "CHROMA_DB_PATH",
        str(PROJECT_ROOT / "chroma_db"),
    )
)

DEFAULT_TOP_K = int(
    os.getenv("RETRIEVAL_TOP_K", "5")
)

SIMILARITY_THRESHOLD = float(
    os.getenv(
        "RETRIEVAL_SIMILARITY_THRESHOLD",
        "0.30",
    )
)

# =====================================================
# Embeddings
# =====================================================

embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
)

# =====================================================
# Vector Store
# =====================================================

db = Chroma(
    persist_directory=str(CHROMA_DB_PATH),
    embedding_function=embeddings,
)

# =====================================================
# Retriever
# =====================================================


def retrieve_documents(
    query: str,
    *,
    top_k: int = DEFAULT_TOP_K,
    metadata_filter: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Retrieve relevant documents with similarity scores.

    Returns:
        [
            {
                "document": Document,
                "score": float,
                "confidence": float,
            }
        ]
    """

    try:

        results = db.similarity_search_with_relevance_scores(
            query=query,
            k=top_k,
            filter=metadata_filter,
        )

        documents: list[dict[str, Any]] = []

        for document, score in results:

            if score < SIMILARITY_THRESHOLD:
                continue

            documents.append(
                {
                    "document": document,
                    "score": round(score, 4),
                    "confidence": round(score * 100, 2),
                }
            )

        logger.info(
            "Retrieved %s document(s) for query='%s'",
            len(documents),
            query,
        )

        return documents

    except Exception:
        logger.exception(
            "Failed to retrieve documents."
        )
        raise


# =====================================================
# LangChain Retriever
# =====================================================

retriever = db.as_retriever(
    search_kwargs={
        "k": DEFAULT_TOP_K,
    }
)