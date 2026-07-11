"""
RAG Ingestion Pipeline

Reads:
    - CSV Reports
    - HTML Reports

Creates:
    - LangChain Documents
    - Embeddings
    - ChromaDB Vector Store
"""

from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from src.rag.embeddings import get_embeddings
from pathlib import Path
import os

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

# =====================================================
# CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = Path(
    os.getenv(
        "DATA_FOLDER",
        str(PROJECT_ROOT / "data"),
    )
)

CHROMA_DB = Path(
    os.getenv(
        "CHROMA_DB",
        str(PROJECT_ROOT / "chroma_db"),
    )
)

BATCH_SIZE = int(
    os.getenv("INGEST_BATCH_SIZE", "100")
)

# =====================================================
# REQUIRED COLUMNS
# =====================================================

REQUIRED_COLUMNS = [
    "project_id",
    "failure_type",
    "severity",
]

# =====================================================
# HELPERS
# =====================================================


def normalize(value: object, default: str = "UNKNOWN") -> str:
    """
    Normalize dataframe values.
    """

    if pd.isna(value):
        return default

    value = str(value).strip()

    if not value:
        return default

    return value


def validate_dataframe(
    df: pd.DataFrame,
    source: str,
) -> bool:
    """
    Validate required columns.
    """

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        logger.warning(
            "File '%s' missing columns: %s",
            source,
            ", ".join(missing),
        )

    return True


# =====================================================
# FILE LOADERS
# =====================================================


def load_csv(
    file_path: Path,
) -> Optional[pd.DataFrame]:
    """
    Load a CSV report.
    """

    try:

        df = pd.read_csv(file_path)

        validate_dataframe(
            df,
            file_path.name,
        )

        logger.info(
            "Loaded CSV '%s' (%d rows)",
            file_path.name,
            len(df),
        )

        return df

    except Exception:
        logger.exception(
            "Failed loading CSV '%s'",
            file_path,
        )
        return None


def load_html(
    file_path: Path,
) -> Optional[pd.DataFrame]:
    """
    Load an HTML report.
    """

    try:

        tables = pd.read_html(file_path)

        if not tables:
            logger.warning(
                "No tables found in HTML '%s'",
                file_path.name,
            )
            return None

        df = tables[0]

        validate_dataframe(
            df,
            file_path.name,
        )

        logger.info(
            "Loaded HTML '%s' (%d rows)",
            file_path.name,
            len(df),
        )

        return df

    except Exception:
        logger.exception(
            "Failed loading HTML '%s'",
            file_path,
        )
        return None

# =====================================================
# DOCUMENT CREATION
# =====================================================


def create_documents(
    df: pd.DataFrame,
    source_file: str,
    document_type: str,
) -> List[Document]:
    """
    Convert a dataframe into LangChain Documents.
    """

    documents: List[Document] = []

    ingested_at = datetime.utcnow().isoformat()

    for _, row in df.iterrows():

        project_id = normalize(row.get("project_id"))
        failure_type = normalize(row.get("failure_type"))
        severity = normalize(row.get("severity"))

        resolution = normalize(
            row.get("resolution"),
            default=""
        )

        report_date = normalize(
            row.get("report_date"),
            default=""
        )

        payment_status = normalize(
            row.get("payment_status"),
            default=""
        )

        amount_due = normalize(
            row.get("amount_due"),
            default=""
        )

        amount_paid = normalize(
            row.get("amount_paid"),
            default=""
        )

        # Skip completely empty rows
        if (
            project_id == "UNKNOWN"
            and failure_type == "UNKNOWN"
            and severity == "UNKNOWN"
        ):
            continue

        document_id = str(uuid.uuid4())

        text = f"""
Project ID: {project_id}

Failure Type: {failure_type}

Severity: {severity}

Payment Status: {payment_status}

Amount Due: {amount_due}

Amount Paid: {amount_paid}

Resolution: {resolution}

Report Date: {report_date}
""".strip()

        metadata = {
            "document_id": document_id,
            "source_file": source_file,
            "document_type": document_type,
            "ingested_at": ingested_at,

            "project_id": project_id,
            "failure_type": failure_type,
            "severity": severity,
            "payment_status": payment_status,
            "report_date": report_date,
        }

        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    logger.info(
        "Created %d documents from '%s'",
        len(documents),
        source_file,
    )

    return documents


# =====================================================
# PROCESS REPORTS
# =====================================================


def process_reports() -> List[Document]:
    """
    Scan the data folder and create LangChain documents.
    """

    documents: List[Document] = []

    if not DATA_FOLDER.exists():
        logger.error(
            "Data folder '%s' does not exist.",
            DATA_FOLDER,
        )
        return documents

    files = list(DATA_FOLDER.rglob("*"))

    logger.info(
        "Found %d files.",
        len(files),
    )

    for file_path in files:

        suffix = file_path.suffix.lower()

        if suffix == ".csv":

            dataframe = load_csv(file_path)

            if dataframe is None:
                continue

            documents.extend(
                create_documents(
                    dataframe,
                    source_file=file_path.name,
                    document_type="csv",
                )
            )

        elif suffix in [".html", ".htm"]:

            dataframe = load_html(file_path)

            if dataframe is None:
                continue

            documents.extend(
                create_documents(
                    dataframe,
                    source_file=file_path.name,
                    document_type="html",
                )
            )

        else:
            logger.debug(
                "Skipping unsupported file '%s'",
                file_path.name,
            )

    logger.info(
        "Total documents created: %d",
        len(documents),
    )

    return documents

# =====================================================
# VECTOR STORE
# =====================================================


def build_vector_store(
    documents: List[Document],
) -> None:
    """
    Build the Chroma vector database.
    """

    if not documents:
        logger.warning(
            "No documents available for ingestion."
        )
        return

    logger.info(
        "Creating embeddings for %d documents.",
        len(documents),
    )

    try:

        embeddings = get_embeddings()

        db = Chroma(
            persist_directory=str(CHROMA_DB),
            embedding_function=embeddings,
        )

        total_batches = (
            len(documents) + BATCH_SIZE - 1
        ) // BATCH_SIZE

        for batch_number, start in enumerate(
            range(0, len(documents), BATCH_SIZE),
            start=1,
        ):

            batch = documents[
                start:start + BATCH_SIZE
            ]

            logger.info(
                "Processing batch %d of %d (%d documents)",
                batch_number,
                total_batches,
                len(batch),
            )

            db.add_documents(batch)

        logger.info(
            "Successfully indexed %d documents.",
            len(documents),
        )

    except Exception:
        logger.exception(
            "Failed to build Chroma vector store."
        )
        raise


# =====================================================
# MAIN
# =====================================================


def main() -> None:
    """
    Execute the ingestion pipeline.
    """

    logger.info(
        "=" * 60
    )
    logger.info(
        "Starting Payment Report Ingestion"
    )
    logger.info(
        "=" * 60
    )

    try:

        documents = process_reports()

        if not documents:
            logger.warning(
                "No documents were created."
            )
            return

        build_vector_store(documents)

        logger.info(
            "=" * 60
        )
        logger.info(
            "Payment Reports Successfully Indexed"
        )
        logger.info(
            "Total Documents : %d",
            len(documents),
        )
        logger.info(
            "Vector Store    : %s",
            CHROMA_DB,
        )
        logger.info(
            "=" * 60
        )

    except Exception:
        logger.exception(
            "Ingestion pipeline failed."
        )
        raise


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()