
"""
AI logic layer: dua kemampuan tambahan untuk /summarize dan /analyze.

Model dan client Ollama diambil dari app/config.py.

API layer tidak memanggil file ini secara langsung.
main.py memanggilnya melalui app/ai/adapter.py.
"""

from app.config import MODEL, create_ollama_client

client = create_ollama_client()


PROMPT_SUMMARIZE = """Ringkas teks berikut dalam maksimal tiga kalimat Bahasa Indonesia.
Jangan menambah informasi yang tidak ada di teks.

TEKS:
{teks}"""


PROMPT_CLASSIFY = """Klasifikasikan pesan nasabah ke SATU label: keluhan, pertanyaan, atau pujian.
Jawab dengan satu kata saja.

Pesan: Klaim saya sudah dua minggu belum diproses, ini keterlaluan.
Label: keluhan

Pesan: Apakah polis saya menanggung rawat jalan?
Label: pertanyaan

Pesan: Terima kasih, agennya sangat membantu kemarin.
Label: pujian

Pesan: {teks}
Label:"""

VALID_LABELS = {"keluhan", "pertanyaan", "pujian"}


def _call_llm(prompt: str) -> str:
    resp = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return (resp.message.content or "").strip()


def summarize_text(teks: str) -> dict:
    ringkasan = _call_llm(
        PROMPT_SUMMARIZE.format(teks=teks)
    )

    return {"ringkasan": ringkasan}


def classify_text(teks: str) -> dict:
    kata = _call_llm(
        PROMPT_CLASSIFY.format(teks=teks)
    ).lower().split()

    label = kata[0].strip(".,:") if kata else ""

    if label not in VALID_LABELS:
        label = "tidak_diketahui"

    return {"label": label}
