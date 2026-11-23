"""
Pengaturan di satu tempat (baru di 13.4).

Sampai 13.3, nama model dan pembacaan API key untuk AI logic layer ditulis
dua kali, di app/ai/workflow_sesi12.py dan app/ai/text_tasks.py. Mengganti
model berarti mengubah dua file, dan mudah terlewat satu. Mulai 13.4, AI logic
layer mengambil keduanya dari sini.

Data layer (data/rag_sesi11.py) sengaja tetap membaca API key sendiri untuk
embedding, supaya bisa diuji sendirian tanpa folder app/.

API layer (main.py) tidak membaca file ini: ia tidak perlu tahu model apa
yang dipakai di belakangnya.
"""

import ollama

MODEL = "gpt-oss:20b"
STUB_SECONDS = 6


def create_ollama_client():
    """Membuat client Ollama."""
    return ollama.Client()