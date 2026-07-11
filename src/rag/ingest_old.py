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

from pathlib import Path
import pandas as pd

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# =====================================================
# CONFIGURATION
# =====================================================

DATA_FOLDER = "data"
CHROMA_DB = "./chroma_db"

# =====================================================
# LOAD FILES
# =====================================================


def load_csv(file_path):

    try:
        df = pd.read_csv(file_path)
        print(f"[CSV] Loaded {file_path.name} ({len(df)} rows)")
        return df

    except Exception as e:
        print(f"[ERROR] CSV {file_path}: {e}")
        return None


def load_html(file_path):

    try:

        tables = pd.read_html(file_path)

        if len(tables) == 0:
            return None

        df = tables[0]

        print(
            f"[HTML] Loaded {file_path.name} "
            f"({len(df)} rows)"
        )

        return df

    except Exception as e:
        print(f"[ERROR] HTML {file_path}: {e}")
        return None


# =====================================================
# DOCUMENT CREATION
# =====================================================


def create_documents(df, source_file):

    docs = []

    for _, row in df.iterrows():

        project_id = str(
            row.get("project_id", "UNKNOWN")
        )

        failure_type = str(
            row.get("failure_type", "UNKNOWN")
        )

        severity = str(
            row.get("severity", "UNKNOWN")
        )

        resolution = str(
            row.get("resolution", "UNKNOWN")
        )

        report_date = str(
            row.get("report_date", "")
        )

        payment_status = str(
            row.get("payment_status", "")
        )

        amount_due = str(
            row.get("amount_due", "")
        )

        amount_paid = str(
            row.get("amount_paid", "")
        )

        text = f"""
Project ID: {project_id}

Failure Type: {failure_type}

Severity: {severity}

Payment Status: {payment_status}

Amount Due: {amount_due}

Amount Paid: {amount_paid}

Resolution: {resolution}

Report Date: {report_date}
"""

        doc = Document(
            page_content=text,
            metadata={
                "project_id": project_id,
                "failure_type": failure_type,
                "severity": severity,
                "payment_status": payment_status,
                "report_date": report_date,
                "source_file": source_file,
            },
        )

        docs.append(doc)

    return docs


# =====================================================
# PROCESS FILES
# =====================================================


def process_reports():

    all_docs = []

    data_path = Path(DATA_FOLDER)

    files = list(data_path.rglob("*"))

    print(f"\nFound {len(files)} files\n")

    for file in files:

        if file.suffix.lower() == ".csv":

            df = load_csv(file)

            if df is not None:

                docs = create_documents(
                    df,
                    file.name
                )

                all_docs.extend(docs)

        elif file.suffix.lower() in [".html", ".htm"]:

            df = load_html(file)

            if df is not None:

                docs = create_documents(
                    df,
                    file.name
                )

                all_docs.extend(docs)

    return all_docs


# =====================================================
# STORE TO CHROMADB
# =====================================================


def build_vector_store(documents):

    print(
        f"\nCreating embeddings "
        f"for {len(documents)} documents...\n"
    )

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    try:

        db = Chroma(
            persist_directory=CHROMA_DB,
            embedding_function=embeddings
        )

        batch_size = 100

        for i in range(0, len(documents), batch_size):

            batch = documents[i:i + batch_size]

            print(
                f"Processing batch "
                f"{i + 1} - {i + len(batch)}"
            )

            db.add_documents(batch)

        print(
            f"\nSuccessfully loaded "
            f"{len(documents)} documents "
            f"into ChromaDB\n"
        )

    except Exception as e:

        print("\nERROR DETAILS:\n")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception: {e}")

        import traceback
        traceback.print_exc()

        raise






# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    docs = process_reports()

    print(
        f"\nTotal Documents Created: "
        f"{len(docs)}"
    )

    build_vector_store(docs)

    print(
        "\nPayment Reports Loaded "
        "into ChromaDB Successfully."
    )
