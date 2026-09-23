from rank_bm25 import BM25Okapi


def build_bm25(chunks):

    tokenized_chunks = [
        chunk.lower().split()
        for chunk in chunks
    ]

    return BM25Okapi(tokenized_chunks)


def keyword_search(
    bm25,
    query,
    chunks,
    top_k=3
):

    scores = bm25.get_scores(
        query.lower().split()
    )

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        item[0]
        for item in ranked[:top_k]
    ]