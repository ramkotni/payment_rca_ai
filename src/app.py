"""
Command-line interface for the Payment AI Platform.
"""

from __future__ import annotations

import logging

from graph import graph
from src.config.logging_config import setuplog

setuplog()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Interactive CLI.
    """

    print("=" * 60)
    print("Payment AI Platform")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        try:
            question = input("\nAsk Question: ").strip()

            if not question:
                continue

            if question.lower() == "exit":
                print("\nGoodbye.")
                break

            logger.info("Processing question.")

            result = graph.invoke(
                {
                    "question": question
                }
            )

            answer = result.get(
                "answer",
                "No relevant information found in the indexed payment reports."
            )

            confidence = result.get("confidence", 0.0)

            sources = result.get("sources", [])

            print("\n" + "=" * 60)
            print("Answer")
            print("=" * 60)
            print(answer)

            print("\nConfidence")
            print(f"{confidence:.2%}")

            if sources:
                print("\nSources")

                for source in sources:
                    print(f"- {source}")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break

        except EOFError:
            print("\n\nSession ended.")
            break

        except Exception:
            logger.exception("Unexpected error.")

            print(
                "\nAn unexpected error occurred while processing the request."
            )


if __name__ == "__main__":
    main()