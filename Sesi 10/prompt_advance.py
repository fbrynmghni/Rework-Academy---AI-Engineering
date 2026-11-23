#%% Cell 1: Import Library
import ollama

#%% Cell 2: Inisialisasi Client & Model
# Inisialisasi Client & Model ID
client = ollama.Client()
MODEL_ID = 'gpt-oss:20b'
# Menyimpan coversation history
messages = []

# %% Cell 3: DEMO 1: Zero-Shot Prompting
# Data ulasan kompleks yang memuat beberapa jenis keluhan sekaligus
ulasan_kompleks = "Saya beli sepatu ini harganya 500 ribu, pas dicoba kebesaran padahal saya udah konsul size chart ke admin dan disuruh ambil size 42. Proses retur barangnya lama banget dan adminnya malah nyolot."

print("--- DEMO 1: Zero-Shot Prompting ---")

prompt_zero_shot = f"""
[TASK] Klasifikasikan ulasan ke dalam: 'pengiriman', 'kualitas produk', 'pelayanan', atau 'harga'.
[FORMAT] Jawab HANYA dengan nama kategori.

[INPUT]
Ulasan: '{ulasan_kompleks}'
"""
# Membuat conversation history baru
messages_1 = [
    {
    'role': 'user',
    'content': prompt_zero_shot
    }
]

# Mengirim prompt ke Ollama
response_1 = client.chat(
    model=MODEL_ID,
    messages=messages_1,
    options={'temperature': 0.0},
)

print("[PROMPT ZERO-SHOT]")
print(prompt_zero_shot)
print(f"\n[HASIL MODEL]: {response_1.message.content.strip()}")


#%% Cell 4: DEMO 2: Few-Shot Prompting
print("\n--- DEMO 2: Few-Shot Prompting ---")

prompt_few_shot = f"""
[TASK] Klasifikasikan ulasan ke dalam: 'pengiriman', 'kualitas produk', 'pelayanan', atau 'harga'.
[FORMAT] Jawab HANYA dengan nama kategori.

[EXAMPLES]
Ulasan: 'Warnanya luntur pas dicuci pertama kali.'
Kategori: kualitas produk

Ulasan: 'Adminnya salah kasih rekomendasi ukuran, padahal udah ditanya baik-baik.'
Kategori: pelayanan

Ulasan: 'Ongkirnya mahal banget nutupin diskonnya.'
Kategori: harga

[INPUT]
Ulasan: '{ulasan_kompleks}'
Kategori:
"""

messages_2 = [
    {
        'role': 'user',
        'content': prompt_few_shot
    }
]

response_2 = client.chat(
    model=MODEL_ID,
    messages=messages_2,
    options={'temperature': 0.0}
)

print("[HASIL FEW-SHOT]")
print(response_2.message.content.strip())

#%% Cell 5: DEMO 3: Zero-Shot Chain-of-Thought (CoT)
print("\n--- DEMO 3: Zero-Shot Chain-of-Thought (CoT) ---")

prompt_cot = f"""
[TASK] Klasifikasikan ulasan ke dalam: 'pengiriman', 'kualitas produk', 'pelayanan', atau 'harga'.
Pilih kategori dominan jika ada lebih dari satu isu.

[FORMAT] 
Berpikir langkah demi langkah:
1. Analisis: Identifikasi semua entitas/masalah yang dikeluhkan.
2. Evaluasi: Tentukan mana keluhan yang menjadi akar masalah (root cause) atau yang paling membuat pelanggan marah.
3. Kategori: Tuliskan satu nama kategori akhirnya.

[INPUT]
Ulasan: '{ulasan_kompleks}'
"""

messages_3 = [
    {
        'role': 'user',
        'content': prompt_cot
    }
]

response_3 = client.chat(
    model=MODEL_ID,
    messages=messages_3,
    options={'temperature': 0.0}
)

print("[HASIL ZERO-SHOT CoT]")
print(response_3.message.content.strip())

# --- DEMO 1: Zero-Shot Prompting ---
# [PROMPT ZERO-SHOT]

# [TASK] Klasifikasikan ulasan ke dalam: 'pengiriman', 'kualitas produk', 'pelayanan', atau 'harga'.
# [FORMAT] Jawab HANYA dengan nama kategori.

# [INPUT]
# Ulasan: 'Saya beli sepatu ini harganya 500 ribu, pas dicoba kebesaran padahal saya udah konsul size chart ke admin dan disuruh ambil size 42. Proses retur barangnya lama banget dan adminnya malah nyolot.'


# [HASIL MODEL]: pelayanan

# --- DEMO 2: Few-Shot Prompting ---
# [HASIL FEW-SHOT]
# pelayanan

# --- DEMO 3: Zero-Shot Chain-of-Thought (CoT) ---
# [HASIL ZERO-SHOT CoT]
# Berpikir langkah demi langkah:
# 1. Analisis: Ulasan ini menyebutkan beberapa masalah: ukuran sepatu yang kebesaran (terkait salah saran *size chart*), proses retur yang sangat lama (terkait pengiriman/proses logistik), dan admin yang bernada kasar atau "nyolot" (terkait pelayanan).
# 2. Evaluasi: Meskipun ada masalah ukuran dan pelayanan admin, akar dari puncak kekecewaan pelanggan yang paling dominan diungkapkan di akhir kalimat adalah proses retur yang sangat lama dan interaksi dengan admin yang buruk saat menangani masalah tersebut, yang mana ini merupakan bagian dari aspek pelayanan keseluruhan (customer service dan penanganan purna jual). Namun, karena isu utamanya adalah interaksi dan penanganan masalah oleh admin (pelayanan), serta proses retur, ini paling tepat dikategorikan ke dalam pelayanan. (Alternatif kuat kedua adalah pengiriman karena masalah proses retur yang lama, tetapi inti dari ketidakpuasan melibatkan penanganan admin). Mari kita lihat akar masalah utamanya: penanganan retur dan sikap admin. Ini murni masalah *pelayanan*.
# 3. Kategori: pelayanan