"""Curriculum 8.4, step 1: create and save a FAISS index."""

import faiss

from common import INDEX_FILE, get_document_embeddings, load_client, load_faq


if __name__ == "__main__":
    faq = load_faq()
    client = load_client()
    embeddings = get_document_embeddings(client, faq)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_FILE))

    print("FAISS index siap.")
    print("Dimensi index:", index.d)
    print("Jumlah vector:", index.ntotal)
    print("Disimpan sebagai:", INDEX_FILE.name)
