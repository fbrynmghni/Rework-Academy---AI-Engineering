from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Dua kalimat dengan kata berbeda tapi makna sangat mirip
teks_1 = "Mobil itu sangat cepat"
teks_2 = "Kendaraan tersebut melaju kencang"
corpus = [teks_1, teks_2]

print("=== 1. Representasi Bag-of-Words (TF-IDF) ===")
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)
print("Kosakata (Vocabulary):", vectorizer.get_feature_names_out())

# Hitung kemiripan dengan TF-IDF
sim_tfidf = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
print(f"Kemiripan TF-IDF: {sim_tfidf:.4f} (Gagal mendeteksi kemiripan makna)\n")

print("=== 2. Representasi Text Embedding ===")
# Load model open-source yang ringan
model_st = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model_st.encode(corpus)

# Hitung kemiripan dengan Embedding
sim_embedding = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
print(f"Kemiripan Embedding: {sim_embedding:.4f} (Berhasil mendeteksi kemiripan makna)")