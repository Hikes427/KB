from fastapi import FastAPI
from app.retrieval import retrieve
from app.llm import generate_answer

app = FastAPI()


@app.get("/")
def root():
    return {"message": "RAG API Running"}


@app.get("/ask")
def ask(
    question: str,
    domain: str | None = None,
    classification: str | None = None
):


    contexts = retrieve(question, domain, classification)

    context_text = "\n\n".join(contexts)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context_text}

Question:
{question}

Answer:
"""

    answer = generate_answer(prompt)

    return {
        {
  "question": "...",
  "answer": "...",
  "sources": [
    {
      "document": "wellarchitected-framework.pdf",
      "classification": "public",
      "owner": "aws"
    }
  ]
}
    }