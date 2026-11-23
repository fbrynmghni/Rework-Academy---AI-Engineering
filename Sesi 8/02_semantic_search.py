"""Curriculum 8.1: semantic search using the same queries as keyword search."""

from common import get_document_embeddings, load_client, load_faq
from keyword_search import keyword_search


def semantic_search(query, faq, embeddings, client, k=3):
    import numpy as np

    from common import embed, normalize

    query_vector = normalize(embed(client, [query], "RETRIEVAL_QUERY"))
    scores = (query_vector @ embeddings.T)[0]
    best_positions = np.argsort(-scores)[:k]
    return [(faq[i], float(scores[i])) for i in best_positions]


if __name__ == "__main__":
    faq = load_faq()
    client = load_client()
    embeddings = get_document_embeddings(client, faq)

    queries = ["kendaraan", "reset password", "telat bayar", "pindah rumah", "mobil", "autodebit"]
    for query in queries:
        result = semantic_search(query, faq, embeddings, client, k=1)[0]
        print(f"\nQuery: {query}")
        print("  keyword :", keyword_search(query))
        print(f"  semantic: {result[0]['id']} | skor={result[1]:.3f} | {result[0]['pertanyaan']}")
