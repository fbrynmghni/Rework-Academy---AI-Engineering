"""Shared, small helpers for the semantic-search mentoring demo."""

import os
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types


PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR / "faq_dataset"
# The filename includes the source format so an older cache cannot be mixed
# with the current CSV dataset.
CACHE_FILE = PROJECT_DIR / "embeddings_faq.npy"
INDEX_FILE = PROJECT_DIR / "faq.index"
MODEL = "gemini-embedding-2"
DIMENSION = 768


def load_faq():
    """Load the prepared CSV file and return simple dictionaries."""
    csv_file = DATASET_DIR / "faq_lindungiku.csv"
    if not csv_file.exists():
        raise FileNotFoundError(f"Tidak menemukan file dataset: {csv_file}")

    dataframe = pd.read_csv(csv_file, dtype=str).fillna("")
    return dataframe.to_dict(orient="records")


def document_text(row):
    return f"{row['pertanyaan']} {row['jawaban']}"


def load_client():
    """Create the Gemini client only when a semantic demo needs it."""
    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Isi GEMINI_API_KEY di file .env terlebih dahulu.")
    return genai.Client(api_key=api_key)


def embed(client, texts, task_type):
    """Turn text into vectors, in batches of at most 100 texts."""
    vectors = []
    for start in range(0, len(texts), 100):
        batch = texts[start : start + 100]
        response = client.models.embed_content(
            model=MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                output_dimensionality=DIMENSION,
            ),
        )
        if len(response.embeddings) == len(batch):
            vectors.extend(item.values for item in response.embeddings)
            continue

        # Some embedding model versions return one vector for a list of
        # contents. Fall back to one request per text so each FAQ keeps its
        # own vector and FAISS positions still map to FAQ rows correctly.
        for text in batch:
            single = client.models.embed_content(
                model=MODEL,
                contents=[text],
                config=types.EmbedContentConfig(
                    output_dimensionality=DIMENSION,
                ),
            )
            if len(single.embeddings) != 1:
                raise RuntimeError("API tidak mengembalikan satu embedding untuk satu teks.")
            vectors.append(single.embeddings[0].values)
    return np.array(vectors, dtype="float32")


def normalize(vectors):
    """Normalize vectors so their inner product is cosine similarity."""
    lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / lengths


def get_document_embeddings(client, faq):
    """Load cached document embeddings, or create and cache them."""
    if CACHE_FILE.exists():
        cached = np.load(CACHE_FILE)
        if cached.shape == (len(faq), DIMENSION):
            print(f"Memakai embedding dari cache: {CACHE_FILE.name}")
            return cached
        print("Cache embedding tidak cocok dengan jumlah dokumen; membuat ulang.")

    texts = [document_text(row) for row in faq]
    embeddings = normalize(embed(client, texts, "RETRIEVAL_DOCUMENT"))
    np.save(CACHE_FILE, embeddings)
    print(f"Embedding dibuat dan disimpan ke {CACHE_FILE.name}")
    return embeddings
