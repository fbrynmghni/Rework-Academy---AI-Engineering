from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model_st = SentenceTransformer('all-MiniLM-L6-v2')

# # --- Skenario 1: Makna Mirip, Kosakata Beda ---
# kalimat_mirip_1 = "Mobil itu melaju dengan sangat cepat."
# kalimat_mirip_2 = "Kendaraan tersebut bergerak dengan kecepatan tinggi."

# # --- Skenario 2: Topik Sama Sekali Berbeda ---
# kalimat_beda_1 = "Kucing itu sedang tidur di atas sofa yang empuk."
# kalimat_beda_2 = "Harga saham perusahaan teknologi melonjak drastis hari ini."


# --- Skenario 1: Makna Mirip, Kosakata Beda (Bahasa Inggris) ---
kalimat_mirip_1 = "A fast car is speeding down the highway."
kalimat_mirip_2 = "The quick vehicle is driving rapidly on the freeway."

# --- Skenario 2: Topik Sama Sekali Berbeda ---
kalimat_beda_1 = "The cute cat is sleeping on the sofa."
kalimat_beda_2 = "Technology company stock prices surged today."

# Ubah ke vektor
emb_mirip_1 = model_st.encode([kalimat_mirip_1])
emb_mirip_2 = model_st.encode([kalimat_mirip_2])
emb_beda_1 = model_st.encode([kalimat_beda_1])
emb_beda_2 = model_st.encode([kalimat_beda_2])

# Hitung skor
skor_mirip = cosine_similarity(emb_mirip_1, emb_mirip_2)[0][0]
skor_beda = cosine_similarity(emb_beda_1, emb_beda_2)[0][0]

print("=== Pengukuran Cosine Similarity ===")
print(f"Pasangan Mirip  : {skor_mirip:.4f} (Mendekati 1.0)")
print(f"Pasangan Berbeda: {skor_beda:.4f} (Skor rendah)")