from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="finance_docs"
)
def store_chunks(chunks, embeddings, metadatas):
    ids = [
    f"{metadatas[i]['document']}_chunk_{i}"
    for i in range(len(chunks))
]
    collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
)

    print(f"Stored {len(chunks)} chunks")

