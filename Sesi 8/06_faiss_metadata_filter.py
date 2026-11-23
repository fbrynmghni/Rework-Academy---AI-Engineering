"""Curriculum 8.4 bonus: FAISS search combined with metadata filtering."""

import faiss

from common import embed, get_document_embeddings, load_client, load_faq, normalize


def filtered_search(query, category, faq, embeddings, client, k=3):
    positions = [i for i, row in enumerate(faq) if row["kategori"] == category]
    small_index = faiss.IndexFlatIP(embeddings.shape[1])
    small_index.add(embeddings[positions])

    query_vector = normalize(embed(client, [query], "RETRIEVAL_QUERY"))
    scores, local_positions = small_index.search(query_vector, min(k, len(positions)))
    return [(faq[positions[i]], float(score)) for i, score in zip(local_positions[0], scores[0])]


if __name__ == "__main__":
    faq = load_faq()
    client = load_client()
    embeddings = get_document_embeddings(client, faq)

    print("Query: berapa lama prosesnya | filter kategori: klaim\n")
    for row, score in filtered_search("berapa lama prosesnya", "klaim", faq, embeddings, client):
        print(f"{row['id']} | skor={score:.3f} | {row['pertanyaan']}")
