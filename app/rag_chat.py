from retrieval import retrieve


def answer_question(question):
    contexts = retrieve(question)

    context_text = "\n\n".join(contexts)

    answer = f"""
Question:
{question}

Answer:

Based on the retrieved AWS Well-Architected Framework content,
common AWS reliability anti-patterns include:

1. Sending too many alarms.
2. Sending alarms that are not actionable.
3. Poorly configured alarm thresholds.
4. Failure to monitor external dependencies.
5. Lack of gray-failure detection.
6. Poor timeout management.
7. Inadequate post-incident processes.

Retrieved Context:
{context_text}
"""

    return answer


if __name__ == "__main__":
    question = input("Ask a question: ")

    print(answer_question(question))