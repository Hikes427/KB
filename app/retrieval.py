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

    if domain and classification:
        where = {
            "$and": [
                {"domain": domain},
                {"classification": classification}
            ]
        }
    elif domain:
        where = {"domain": domain}
    elif classification:
        where = {"classification": classification}
    else:
        where = None

    results = collection.query(
        query_texts=[query],
        where=where,
        n_results=3
    )

    return {
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0],
    }


if __name__ == "__main__":

    results = retrieve(
        query="declined transactions",
        domain="finance",
        classification="internal"
    )

    print("\nDOCUMENTS")
    print("=" * 80)

    for doc in results["documents"]:
        print(doc[:500])
        print()

    print("\nMETADATA")
    print("=" * 80)

    for metadata in results["metadatas"]:
        print(metadata)