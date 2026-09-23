from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    "finance_docs"
)


def retrieve(
    query,
    domain=None,
    classification=None
):

    where = {
        key: value
        for key, value in {
            "domain": domain,
            "classification": classification,
        }.items()
        if value is not None
    } or None

    results = collection.query(
        query_texts=[query],
        where=where,
        n_results=3
    )

    return results["documents"][0]


if __name__ == "__main__":
    results = retrieve(
        "declined transactions"
    )

    for result in results:
        print("\n" + "=" * 80)
        print(result)