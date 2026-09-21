import chromadb

client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = client.get_collection(
    "finance_docs"
)


def retrieve(query):
    results = collection.query(
        query_texts=[query],
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