# Rework Academy — AI Engineering

Dokumentasi perjalanan belajar dan praktik **AI Engineering** melalui program Rework Academy. Repository ini berisi materi pembelajaran, eksperimen, notebook, latihan, dan individual assignment yang dikerjakan secara bertahap.

Fokus utama repository ini adalah memahami fondasi teknis sekaligus membangun aplikasi AI yang dapat digunakan untuk menyelesaikan permasalahan nyata.

> **Learning by building:** mempelajari konsep, mengimplementasikannya dengan Python, menguji hasilnya, lalu mendokumentasikan proses dan evaluasinya.

---

## Daftar Isi

- [Learning Objectives](#learning-objectives)
- [Learning Topics](#learning-topics)
- [Repository Structure](#repository-structure)
- [Projects and Assignments](#projects-and-assignments)
- [Technology Stack](#technology-stack)
- [Development Environment](#development-environment)
- [How to Use This Repository](#how-to-use-this-repository)
- [Learning Approach](#learning-approach)

---

## Learning Objectives

Repository ini dikembangkan sebagai ruang praktik untuk:

- Memperkuat fundamental Python dan problem-solving.
- Mengolah data melalui proses data ingestion, cleaning, transformation, dan preparation.
- Memahami workflow Machine Learning, mulai dari data preparation hingga model evaluation.
- Memahami konsep Deep Learning, NLP, embeddings, dan Large Language Models (LLM).
- Mengembangkan aplikasi berbasis LLM dengan prompt engineering dan structured output.
- Membangun semantic search dan Retrieval-Augmented Generation (RAG).
- Mengorkestrasi workflow AI menggunakan tools dan graph-based workflows.
- Mengembangkan AI application menjadi backend service menggunakan FastAPI.
- Menerapkan software engineering practices seperti modularisasi kode, environment management, version control, dan dokumentasi.

## Learning Topics

Materi disusun mengikuti perkembangan pembelajaran AI Engineering.

| Area | Topik yang dipelajari |
|---|---|
| Python Fundamentals | Variables, data types, control flow, loops, functions, data structures, OOP, dan problem-solving |
| Development Workflow | Git, GitHub, virtual environment, dependency management, dan penggunaan `uv` |
| Data Engineering | Data ingestion, exploratory data analysis, missing values, duplicates, data cleaning, transformation, dan feature engineering |
| Machine Learning | Supervised learning, classification, model training, inference, dan evaluation |
| Model Evaluation | Accuracy, precision, recall, F1-score, confusion matrix, dan feature importance |
| LLM Engineering | LLM fundamentals, model inference, prompt engineering, temperature, dan structured output |
| Embeddings & Semantic Search | Text embeddings, vector representation, similarity search, dan FAISS |
| Retrieval-Augmented Generation | Knowledge base, retrieval pipeline, context management, dan grounded generation |
| AI Orchestration | Tool calling, workflow routing, LangChain, LangGraph, dan multi-step AI workflows |
| Backend Development | FastAPI, API endpoints, request/response validation, dan pemisahan application layers |

*Daftar ini merupakan peta topik pembelajaran, bukan klaim bahwa seluruh topik telah selesai atau seluruhnya diimplementasikan dalam satu aplikasi.*

## Repository Structure

Repository ini menggabungkan materi sesi pembelajaran dan project assignment. Struktur aktual dapat berkembang seiring penambahan materi dan eksperimen.

```text
Rework-Academy---AI-Engineering/
├── Assignment/
│   ├── data-pipeline-assignment/
│   ├── model-experiment-assignment/
│   └── semantic-search-assignment/
│
├── [session folders]/
│   ├── notebooks/
│   ├── scripts/
│   └── supporting files
│
└── README.md
```

Beberapa assignment dikelola sebagai **Git submodule**. Karena itu, setelah clone repository utama, submodule perlu diinisialisasi agar isi repository assignment ikut tersedia.

## Projects and Assignments

### 1. Data Pipeline Assignment

Latihan membangun pipeline pengolahan data. Area praktiknya mencakup pembacaan dataset, pemeriksaan kualitas data, data cleaning, transformation, dan penyimpanan hasil pengolahan.

### 2. Model Experiment Assignment

Eksperimen penerapan Machine Learning pada dataset, termasuk proses persiapan data, training model, prediksi, dan evaluasi performa.

### 3. Semantic Search & LLM Application

Membangun prototype semantic search yang menghubungkan knowledge base FAQ dengan LLM.

Alur sistem yang menjadi fokus:

```text
Knowledge Base
      │
      ▼
    Ingest
      │
      ▼
   Embedding
      │
      ▼
 FAISS Vector Index
      │
      ▼
 Semantic Retrieval
      │
      ▼
 Prompt + Retrieved Context
      │
      ▼
      LLM
      │
      ▼
  AI Response
```

Komponen utama assignment:

- Memuat dan menyiapkan knowledge base FAQ.
- Mengubah setiap entri FAQ menjadi embedding.
- Menyimpan embedding ke FAISS.
- Mengambil FAQ yang relevan berdasarkan semantic similarity.
- Menyisipkan hasil retrieval ke dalam prompt sebagai context.
- Menghasilkan jawaban menggunakan LLM berdasarkan context yang tersedia.
- Menguji retrieval dan kualitas jawaban menggunakan beberapa variasi query.

**Catatan:** detail implementasi, hasil pengujian, dan cara menjalankan setiap assignment dijelaskan di README masing-masing subproject.

## Technology Stack

Tools dan library yang digunakan dalam proses pembelajaran dan eksperimen antara lain:

| Category | Tools / Libraries |
|---|---|
| Programming Language | Python |
| Environment & Package Management | `uv`, `venv` |
| Data Processing | Pandas, NumPy |
| Machine Learning | scikit-learn |
| Notebook | Jupyter Notebook |
| LLM & Embeddings | Gemini API, Ollama |
| Vector Search | FAISS |
| AI Orchestration | LangChain, LangGraph |
| Backend API | FastAPI |
| Version Control | Git, GitHub |
| Development Tools | Visual Studio Code |

Penggunaan tools dapat berbeda pada setiap sesi atau assignment. Lihat file dependency dan dokumentasi pada masing-masing project untuk mengetahui kebutuhan yang tepat.

## Development Environment

Project Python di repository ini menggunakan pendekatan environment terisolasi. Untuk project yang menyediakan `pyproject.toml`, environment dapat disiapkan menggunakan `uv`.

### Clone repository

```bash
git clone --recurse-submodules https://github.com/fbrynmghni/Rework-Academy---AI-Engineering.git

cd Rework-Academy---AI-Engineering
```

Jika repository sudah terlanjur di-clone tanpa submodule:

```bash
git submodule update --init --recursive
```

Untuk mengambil pembaruan submodule:

```bash
git submodule update --remote --recursive
```

### Menyiapkan environment pada project

Masuk ke folder project yang ingin dijalankan. Jika project tersebut memiliki `pyproject.toml`:

```bash
uv sync
```

Aktifkan environment:

```bash
source .venv/bin/activate
```

Jika project hanya menyediakan `requirements.txt`, buat environment dan install dependency dengan `uv`:

```bash
uv venv
uv pip install -r requirements.txt
```

Jalankan notebook atau script sesuai instruksi pada masing-masing project.

### API keys

Beberapa eksperimen yang menggunakan layanan eksternal memerlukan API key. Simpan credential di file `.env` pada project terkait dan jangan pernah commit file tersebut ke GitHub.

Contoh:

```env
GEMINI_API_KEY=your_api_key
```

Pastikan `.env`, `.venv/`, cache, dan file lokal lain yang tidak diperlukan sudah tercantum di `.gitignore`.

## How to Use This Repository

1. Clone repository beserta submodule.
2. Pilih folder sesi atau assignment yang ingin dipelajari.
3. Baca README atau dokumentasi di dalam folder tersebut jika tersedia.
4. Siapkan environment dan dependency sesuai konfigurasi project.
5. Jalankan notebook atau script dari awal hingga akhir.
6. Periksa hasil eksperimen, lakukan pengujian, dan dokumentasikan temuan.
7. Gunakan Git untuk mencatat perubahan dan perkembangan project.

Setiap folder dapat memiliki konfigurasi environment dan instruksi eksekusi yang berbeda. Jangan mengasumsikan satu environment atau satu perintah dapat menjalankan seluruh project.

## Learning Approach

Pembelajaran dilakukan dengan menekankan pemahaman konsep dan implementasi langsung:

- **Understand the fundamentals** — memahami konsep sebelum mengandalkan abstraksi framework.
- **Build incrementally** — memecah sistem menjadi komponen kecil yang dapat diuji.
- **Experiment and evaluate** — tidak hanya menjalankan model, tetapi juga memeriksa metrik dan kualitas output.
- **Debug systematically** — memahami error, menelusuri penyebab, dan memperbaiki implementasi.
- **Document the process** — mencatat keputusan teknis, hasil eksperimen, serta keterbatasan sistem.

---

## Author

**Febryan Mughni**

AI Engineering Learner | Rework Academy

- GitHub: [@fbrynmghni](https://github.com/fbrynmghni)

---

*This repository is a continuous learning log. Its contents may evolve as new sessions, experiments, and assignments are added.*
