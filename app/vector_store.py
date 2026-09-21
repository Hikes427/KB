import chromadb

client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = client.get_or_create_collection(
    name="finance_docs"
)
def store_chunks(chunks):
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks
    )

    print(f"Stored {len(chunks)} chunks")
results = collection.query(
    query_texts=[
        "declined transactions"
    ],
    n_results=3
)

print(results["documents"])
