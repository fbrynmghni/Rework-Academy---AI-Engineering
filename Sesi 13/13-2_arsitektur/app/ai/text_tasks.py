"""
AI logic layer: dua kemampuan tambahan untuk /summarize dan /analyze.

Di sinilah prompt-nya tinggal. Jika tim AI ingin mengganti prompt atau model,
cukup file ini yang disentuh. main.py tidak ikut berubah.

File ini tidak dipanggil langsung oleh API layer. main.py memanggilnya lewat
app/ai/adapter.py.
"""

import os

from dotenv import load_dotenv
from google import genai

MODEL = "gemini-2.5-flash"

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])   # error jika key kosong; adapter menangkapnya


PROMPT_SUMMARIZE = """Ringkas teks berikut dalam maksimal tiga kalimat Bahasa Indonesia.
Jangan menambah informasi yang tidak ada di teks.

TEKS:
{teks}"""


# Few-shot prompting dari Sesi 10: beri contoh dulu, baru minta jawaban.
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


def _call_llm(prompt):
    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return (resp.text or "").strip()


def summarize_text(teks):
    return {"ringkasan": _call_llm(PROMPT_SUMMARIZE.format(teks=teks))}


def classify_text(teks):
    kata = _call_llm(PROMPT_CLASSIFY.format(teks=teks)).lower().split()
    label = kata[0].strip(".,:") if kata else ""
    if label not in VALID_LABELS:
        label = "tidak_diketahui"          # jaring pengaman
    return {"label": label}
