import os
import json
from pydantic import BaseModel, Field
import ollama


# Inisialisasi Client & Model ID
client = ollama.Client()
MODEL_ID = 'gpt-oss:20b'

# Data Ulasan untuk Demo
ulasan_pelanggan = "Barang sampai lumayan cepat, packaging rapi. Tapi pas dibuka, warna bajunya beda sama di foto produk. Katanya navy tapi ini malah kaya hitam kusam."

print("--- DEMO 1: System Instruction Separation ---")

# System Instruction mengatur identitas dan batas perilaku model
system_instruction = """
Kamu adalah AI Analyst profesional untuk Toko Online.
Tugasmu adalah menganalisis ulasan pelanggan secara objektif dan ringkas.
Jangan pernah berasumsi di luar informasi yang diberikan oleh pelanggan.
"""

messages_1 = [{
    "role": "system",
    "content": system_instruction
}]

prompt_user = f"Analisis ulasan berikut: '{ulasan_pelanggan}'"

messages_1.append({
    "role": "user", 
    "content": prompt_user
    })

chat = client.chat(
    model=MODEL_ID,
    messages=messages_1,
    options={'temperature': 0.0}
    )

response_1 = client.chat(
    model=MODEL_ID,
    messages=messages_1,
    options={'temperature': 0.0}
)

print("[SYSTEM INSTRUCTION DISET]")
print("[USER PROMPT]:", prompt_user)
print("\n[HASIL MODEL]:")
print(response_1.message.content.strip())

print("\n--- DEMO 2: Hyperparameter Tuning (Deterministik) ---")

system_instruction_deterministik = """
Klasifikasikan ulasan pelanggan ke dalam SATU kata kategori:
pengiriman, kualitas produk, pelayanan, atau harga."""

messages_2 = [{
    "role": "system",
    "content": system_instruction_deterministik
}]

messages_2.append({
    "role": "user",
    "content": f"Ulasan: '{ulasan_pelanggan}'"
})

response_2 = client.chat(
    model=MODEL_ID,
    messages=messages_2,
    options={'temperature': 0.0,
             "top_p": 0.8}
)

print("[HASIL MODEL (Temperature 0.0 dan Top P 0.8)]:")
print(response_2.message.content.strip())

print("\n--- DEMO 3: Native JSON Mode ---")

prompt_json = f"""
Ekstrak ulasan berikut ke dalam JSON dengan kunci:
- "kategori": kategori ulasan (pengiriman, kualitas produk, pelayanan, harga)
- "sentimen": sentimen ulasan (positif, negatif, netral)
- "alasan_singkat": ringkasan keluhan utama pelanggan

Ulasan: '{ulasan_pelanggan}'
"""

messages_3 = [{
    "role": "system",
    "content": prompt_json
}]

messages_3.append({
    "role": "user",
    "content": f"Ulasan: '{ulasan_pelanggan}'"
})

response_3 = client.chat(
    model=MODEL_ID,
    messages=messages_3,
    options={'temperature': 0.0}
)

json_text = response_3.message.content.strip()
print("[RAW JSON STRING DARI MODEL]:")
print(json_text)

# Parsing ke Python Dictionary
data_dict = json.loads(json_text)[0]
print("\n🟢 PARSED DICTIONARY:")
print(f"Kategori : {data_dict.get('kategori')}")
print(f"Sentimen : {data_dict.get('sentimen')}")
print(f"Alasan   : {data_dict.get('alasan_singkat')}")

print("\n--- DEMO 4: Strict Schema Enforcement (Pydantic) ---")

# 1. Definisikan Skema Output menggunakan Pydantic
class UlasanAnalysis(BaseModel):
    kategori: str = Field(description="Kategori ulasan: 'pengiriman', 'kualitas produk', 'pelayanan', atau 'harga'")
    sentimen: str = Field(description="Sentimen ulasan: 'positif', 'negatif', atau 'netral'")
    skor_kecewaan: int = Field(description="Skor tingkat kecewa pelanggan dari skala 1 (sangat puas) sampai 5 (sangat kecewa)")
    keluhan_utama: str = Field(description="Ringkasan 1 kalimat poin utama keluhan pelanggan")

# 2. Inisialisasi Chat dengan response_schema
prompt_user = f"Analisis ulasan berikut: '{ulasan_pelanggan}'"

messages_4 = [{
    "role": "system",
    "content": "Kamu adalah sistem otomatis pemrosesan ulasan pelanggan"
},
{
    "role": "user",
    "content": prompt_user
    }
]
# 3. Eksekusi
response_4 = client.chat(
    model=MODEL_ID,
    messages=messages_4,
    options={'temperature': 0.0}
)

# 4. Ambil hasil langsung sebagai Objek Pydantic lewat `response.parsed`
has_parsed: UlasanAnalysis = response_4.parsed

print("[PEMBACAAN VIA PYDANTIC OBJECT (TYPE-SAFE)]:")
print(f"Tipe Data Objek : {type(has_parsed)}")
print(f"Kategori        : {has_parsed.kategori}")
print(f"Sentimen        : {has_parsed.sentimen}")
print(f"Skor Kecewaan   : {has_parsed.skor_kecewaan}/5")
print(f"Keluhan Utama   : {has_parsed.keluhan_utama}")

# --- DEMO 1: System Instruction Separation ---
# [SYSTEM INSTRUCTION DISET]
# [USER PROMPT]: Analisis ulasan berikut: 'Barang sampai lumayan cepat, packaging rapi. Tapi pas dibuka, warna bajunya beda sama di foto produk. Katanya navy tapi ini malah kaya hitam kusam.'

# [HASIL MODEL]:
# Berikut adalah analisis objektif dan ringkas berdasarkan ulasan pelanggan:

# *   **Aspek Positif:**
#     *   Kecepatan pengiriman: Lumayan cepat.
#     *   Pengemasan (*packaging*): Rapi.
# *   **Aspek Negatif (Keluhan Utama):**
#     *   Kesesuaian produk: Warna baju tidak sesuai dengan foto produk. Pelanggan memesan warna *navy*, namun yang diterima berwarna hitam kusam.
# *   **Kesimpulan:** Layanan pengiriman dan pengemasan memuaskan, namun kualitas penyajian informasi produk (akurasi warna) mengecewakan pelanggan.

# --- DEMO 2: Hyperparameter Tuning (Deterministik) ---
# [HASIL MODEL (Temperature 0.0)]:
# kualitas produk

# --- DEMO 3: Native JSON Mode ---
# [RAW JSON STRING DARI MODEL]:
# [
#   {
#     "kategori": "kualitas produk",
#     "sentimen": "negatif",
#     "alasan_singkat": "Warna baju yang diterima berbeda dengan foto produk (navy terlihat seperti hitam kusam)"
#   }
# ]

# 🟢 PARSED DICTIONARY:
# Kategori : kualitas produk
# Sentimen : negatif
# Alasan   : Warna baju yang diterima berbeda dengan foto produk (navy terlihat seperti hitam kusam)

# --- DEMO 4: Strict Schema Enforcement (Pydantic) ---
# [PEMBACAAN VIA PYDANTIC OBJECT (TYPE-SAFE)]:
# Tipe Data Objek : <class '__main__.UlasanAnalysis'>
# Kategori        : kualitas produk
# Sentimen        : negatif
# Skor Kecewaan   : 4/5
# Keluhan Utama   : Warna baju yang diterima berbeda dari foto produk.