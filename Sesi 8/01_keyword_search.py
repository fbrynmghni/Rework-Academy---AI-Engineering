"""Curriculum 8.1: search using exact words only."""

from common import load_faq
from keyword_search import keyword_search


faq = load_faq()


if __name__ == "__main__":
    print(f"{len(faq)} dokumen dimuat.")
    queries = ["kendaraan", "reset password", "duit klaim cair berapa lama", "telat bayar", "pindah rumah"]
    for query in queries:
        print(f"{query:32} -> {keyword_search(query)}")

    print("\nKata yang memang ada di dokumen:")
    print("mobil   ->", keyword_search("mobil"))
    print("autodebit ->", keyword_search("autodebit"))
