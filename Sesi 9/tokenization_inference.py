# ==========================================
# SESI 9.3: TOKENIZATION & INFERENCE PIPELINE
# ==========================================

from transformers import AutoTokenizer

# 1. Memuat Tokenizer Publik dari Hugging Face
# Menggunakan model 'cahya/t5-base-indonesian-summarization' yang 100% public
model_name = "ardavey/bert2gpt-indosum"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 2. Mendefinisikan contoh teks (Input/Prompt)
teks_singkat = "Halo, selamat datang di sesi Live Bootcamp AI Engineering."
teks_panjang = """
Large Language Model (LLM) telah menjadi komponen inti di berbagai produk digital. 
Pemilihan antara model proprietary (API) dan open-source (self-hosted) harus 
mempertimbangkan aspek kecepatan, kontrol data, dan total biaya infrastruktur.
Ekosistem open-source seperti Hugging Face memungkinkan developer untuk mengakses 
ribuan model secara gratis dan memodifikasinya sesuai kebutuhan privasi aplikasi.
"""

# 3. Proses Tokenisasi (Teks -> Token IDs)
tokens_singkat = tokenizer.encode(teks_singkat)
tokens_panjang = tokenizer.encode(teks_panjang)

print("--- DEMO TOKENIZATION ---")
print(f"Teks Asli:\n{teks_singkat}\n")
print(f"Token IDs (Representasi Numerik):\n{tokens_singkat}\n")

# 4. Membandingkan Jumlah Token
jumlah_token_singkat = len(tokens_singkat)
jumlah_token_panjang = len(tokens_panjang)

print(f"Jumlah Token Teks Singkat: {jumlah_token_singkat} tokens")
print(f"Jumlah Token Teks Panjang: {jumlah_token_panjang} tokens\n")

# 5. Proses Decode (Token IDs -> Teks)
decoded_teks = tokenizer.decode(tokens_singkat, skip_special_tokens=True)
print(f"Hasil Decode kembali:\n{decoded_teks}\n")

# ==========================================
# SIMULASI BIAYA API (Konseptual)
# ==========================================
def estimasi_biaya_api(jumlah_token, harga_per_1000_token):
    return (jumlah_token / 1000) * harga_per_1000_token

# Asumsi harga API (contoh: $0.002 per 1000 token)
harga_api = 0.002 
biaya_singkat = estimasi_biaya_api(jumlah_token_singkat, harga_api)
biaya_panjang = estimasi_biaya_api(jumlah_token_panjang, harga_api)

print("--- ESTIMASI BIAYA INPUT ---")
print(f"Biaya untuk teks singkat: ${biaya_singkat:.6f}")
print(f"Biaya untuk teks panjang: ${biaya_panjang:.6f}")

# Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
# config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5.31k/5.31k [00:00<00:00, 10.5MB/s]
# tokenizer_config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.40k/1.40k [00:00<00:00, 2.45MB/s]
# vocab.txt: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 262k/262k [00:00<00:00, 1.33MB/s]
# special_tokens_map.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 182/182 [00:00<00:00, 402kB/s]
# --- DEMO TOKENIZATION ---
# Teks Asli:
# Halo, selamat datang di sesi Live Bootcamp AI Engineering.

# Token IDs (Representasi Numerik):
# [3, 23442, 15, 6264, 3242, 1495, 8669, 6961, 20219, 2586, 8038, 10239, 15451, 17, 1]

# Jumlah Token Teks Singkat: 15 tokens
# Jumlah Token Teks Panjang: 75 tokens

# Hasil Decode kembali:
# halo, selamat datang di sesi live bootcamp ai engineering.

# --- ESTIMASI BIAYA INPUT ---
# Biaya untuk teks singkat: $0.000030
# Biaya untuk teks panjang: $0.000150