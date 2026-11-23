"""Curriculum 8.2: rank results and compare cosine with Euclidean distance."""

import numpy as np

from common import embed, get_document_embeddings, load_client, load_faq, normalize


if __name__ == "__main__":
    faq = load_faq()
    client = load_client()
    embeddings = get_document_embeddings(client, faq)

    query = "Bagaimana klaim untuk mobil yang rusak?"
    query_vector = normalize(embed(client, [query], "RETRIEVAL_QUERY"))
    cosine_scores = (query_vector @ embeddings.T)[0]
    best_positions = np.argsort(-cosine_scores)[:3]

    print("Query:", query)
    print(f"{'rank':<5} {'id':<5} {'cosine':>8} {'euclidean':>10}  pertanyaan")
    for rank, position in enumerate(best_positions, start=1):
        euclidean = np.linalg.norm(query_vector[0] - embeddings[position])
        print(
            f"{rank:<5} {faq[position]['id']:<5} {cosine_scores[position]:>8.3f} "
            f"{euclidean:>10.3f}  {faq[position]['pertanyaan']}"
        )

    print("\nKarena vector sudah dinormalisasi, cosine lebih tinggi biasanya berarti Euclidean lebih kecil.")
