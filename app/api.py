from fastapi import FastAPI
from app.retrieval import retrieve

app = FastAPI()


@app.get("/")
def root():
    return {"message": "RAG API Running"}


@app.get("/ask")
def ask(question: str):

    contexts = retrieve(question)

    answer = f"""
Based on retrieved AWS documentation:

{contexts[0]}
"""

    return {
        "question": question,
        "answer": answer
    }