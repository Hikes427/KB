from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from vector_store import store_chunks

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

PDF_DIR = Path("../data/documents")


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(text)

    return chunks

def create_embeddings(chunks):
    embeddings = model.encode(chunks)

    print(f"Created {len(embeddings)} embeddings")
    print(f"Embedding dimension: {len(embeddings[0])}")

    return embeddings  

def load_documents():
    pdf_files = list(PDF_DIR.glob("*.pdf"))

    for pdf_file in pdf_files:
        print(f"\nReading: {pdf_file.name}")

        text = extract_text_from_pdf(pdf_file)

        chunks = chunk_text(text)
        store_chunks(chunks)
        print(f"Chunks created: {len(chunks)}")

        print("\nFirst Chunk:")
        print(chunks[0][:300])

        embeddings = create_embeddings(chunks)

if __name__ == "__main__":
    load_documents()