from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from vector_store import store_chunks

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "data" / "documents"

def get_metadata(filename):

    if "wellarchitected" in filename.lower():
        return {
            "domain": "architecture",
            "classification": "public",
            "owner": "aws",
            "source_system": "pdf"
        }

    elif "loan_portfolio" in filename.lower():
        return {
            "domain": "finance",
            "classification": "internal",
            "owner": "risk",
            "source_system": "pdf"
        }

    elif "transaction_data" in filename.lower():
        return {
            "domain": "finance",
            "classification": "internal",
            "owner": "fraud",
            "source_system": "pdf"
        }

    return {
        "domain": "general",
        "classification": "unknown",
        "owner": "unknown",
        "source_system": "pdf"
    }

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
    print(f"PDF Directory: {PDF_DIR}")
    pdf_files = list(PDF_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:

        print(f"\nReading: {pdf_file.name}")

        text = extract_text_from_pdf(pdf_file)

        chunks = chunk_text(text)

        embeddings = create_embeddings(chunks)

        base_metadata = get_metadata(pdf_file.name)

        metadatas = []

        for chunk_num, _ in enumerate(chunks):

            metadata = dict(base_metadata)

            metadata = dict(base_metadata)

            metadata["document"] = pdf_file.name
            metadata["chunk_number"] = chunk_num
            metadata["version"] = "1.0"
            metadata["ingestion_date"] = "2026-09-23"
            metadata["dataset"] = pdf_file.stem

            metadatas.append(metadata)
        store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"Chunks created: {len(chunks)}")

if __name__ == "__main__":
    load_documents()