import json
from pathlib import Path

from langchain_core.runnables import RunnableLambda


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ramayana_english.jsonl"


def load_ramayana_data(_):
    """Load translated Ramayana JSONL."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"File not found: {DATA_PATH}"
        )

    chunks = []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
                chunks.append(chunk)

            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {e}"
                )

    print(f"Loaded {len(chunks)} translated chunks.")

    return chunks


load_data_runnable = RunnableLambda(
    load_ramayana_data
)


if __name__ == "__main__":

    chunks = load_data_runnable.invoke(None)

    print("First chunk:")
    print(chunks[0])

    print("\nChunk ID:", chunks[0]["chunk_id"])
    print("Q&A count:", len(chunks[0]["qa_pairs"]))