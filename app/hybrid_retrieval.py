import pickle

from bm25_search import (
    build_bm25,
    keyword_search
)

from retrieval import retrieve
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

bm25 = build_bm25(chunks)


def reciprocal_rank_fusion(
    vector_docs,
    keyword_docs,
    k=60
):

    scores = {}

    for rank, doc in enumerate(vector_docs):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank + 1)

    for rank, doc in enumerate(keyword_docs):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank + 1)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        doc
        for doc, score in ranked
    ]


def hybrid_search(query):

    vector_results = retrieve(query)

    keyword_results = keyword_search(
        bm25,
        query,
        chunks
    )

    combined = reciprocal_rank_fusion(
        vector_results["documents"],
        keyword_results
    )

    return combined[:5]
if __name__ == "__main__":

    results = hybrid_search(
        "TXN-50004"
    )

    for result in results:
        print("\n" + "=" * 80)
        print(result[:500])
