"""Curriculum 8.4, steps 2-3: query the FAISS index and show ranked results."""

import faiss

from common import INDEX_FILE, embed, load_client, load_faq, normalize


if __name__ == "__main__":
    faq = load_faq()
    client = load_client()
    index = faiss.read_index(str(INDEX_FILE))

    query = "reset password"
    query_vector = normalize(embed(client, [query], "RETRIEVAL_QUERY"))
    scores, positions = index.search(query_vector, 3)

    print("Query:", query)
    for rank, (position, score) in enumerate(zip(positions[0], scores[0]), start=1):
        row = faq[position]
        print(f"{rank}. {row['id']} | skor={score:.3f} | {row['pertanyaan']}")
        print(f"   {row['jawaban'][:120]}...")
