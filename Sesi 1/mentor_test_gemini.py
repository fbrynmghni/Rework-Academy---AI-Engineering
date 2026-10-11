"""
Sesi 1 - Live Coding: Uji Coba Gemini API
==========================================
Versi MENTOR (kode lengkap dan berjalan)

Cara menjalankan:
    (venv) $ python mentor_test_gemini.py
"""

import os
from dotenv import load_dotenv
from google import genai

# Muat variabel dari file .env (harus berisi GEMINI_API_KEY=...)
load_dotenv()

# Ambil API key dari environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Keep error/debugging messages in English (standard convention),
    # even though the surrounding comments are in Bahasa Indonesia.
    raise ValueError(
        "GEMINI_API_KEY not found. Make sure a .env file exists in the "
        "same folder and contains GEMINI_API_KEY=<your_key>."
    )

# Konfigurasi Gemini dengan API key
client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Halo, Perkenalkan dirimu dalam satu kalimat."
)

# Tampilkan balasan
print(response.text)