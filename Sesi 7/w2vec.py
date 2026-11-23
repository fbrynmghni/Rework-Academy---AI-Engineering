import gensim.downloader as api

print("Memuat model Word2Vec (GloVe) ke memori...")
# Menggunakan GloVe 50-dimensi karena ukurannya kecil (66MB) cocok untuk live demo
word_vectors = api.load("glove-wiki-gigaword-50") 

# Demo Aritmatika: King - Man + Woman = ?
# Kita menggunakan bahasa inggris menyesuaikan dataset pretrained
hasil = word_vectors.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)

print("\nHasil Operasi Vektor:")
print("King - Man + Woman = ", hasil[0][0])
print(f"Tingkat Keyakinan (Score): {hasil[0][1]:.4f}")