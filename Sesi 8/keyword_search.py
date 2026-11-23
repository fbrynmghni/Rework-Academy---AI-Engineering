"""Reusable keyword-search function for the 8.1 demo."""

from common import load_faq


faq = load_faq()


def full_text(row):
    return f"{row['pertanyaan']} {row['jawaban']}".lower()


def keyword_search(query):
    """Return document IDs containing every word in query."""
    words = query.lower().split()
    return [row["id"] for row in faq if all(word in full_text(row) for word in words)]
