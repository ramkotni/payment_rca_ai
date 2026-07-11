"""
Embedding model configuration for the Payment AI Platform.
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache

from langchain_ollama import OllamaEmbeddings

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"


@lru_cache(maxsize=1)
def get_embeddings() -> OllamaEmbeddings:
    """
    Returns a singleton Ollama embedding model instance.

    The model name can be configured using:
        OLLAMA_EMBEDDING_MODEL

    Example:
        export OLLAMA_EMBEDDING_MODEL=nomic-embed-text
    """

    model_name = os.getenv(
        "OLLAMA_EMBEDDING_MODEL",
        DEFAULT_EMBEDDING_MODEL,
    )

    logger.info("Loading embedding model: %s", model_name)

    try:
        return OllamaEmbeddings(
            model=model_name
        )

    except Exception:
        logger.exception(
            "Failed to initialize Ollama embedding model."
        )
        raise