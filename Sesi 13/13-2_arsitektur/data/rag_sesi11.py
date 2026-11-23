"""
Data layer Sesi 13: retrieval dari knowledge base Sesi 11.

Isinya sama dengan rag_sesi11.py di Sesi 12. Satu-satunya perubahan: file ini
sekarang tinggal di folder data/, bersama index-nya, dan mencari index di
folder ini lebih dulu.

Yang boleh memakai file ini hanya AI logic layer (app/ai/workflow_sesi12.py):

    from data.rag_sesi11 import cari
    potongan = cari("masa tunggu klaim rawat inap", k=3)

API layer (app/main.py) tidak pernah meng-import file ini.

Letakkan dua file dari Sesi 11 di folder data/ ini:
    index_lindungiku.faiss
    potongan.json

Uji data layer sendirian, dari folder bagian (misalnya 13-4_layanan_ai/):
    python -m data.rag_sesi11
"""

import json
import os
import pathlib

import faiss
import numpy as np
import ollama

MODEL_EMBED = "nomic-embed-text:latest"
DIMENSI = 768


def akar_sesi():
    folder_data = pathlib.Path(__file__).resolve().parent

    if (folder_data / "index_lindungiku.faiss").is_file():
        return folder_data

    raise SystemExit(
        "index_lindungiku.faiss tidak ditemukan.\n"
        "Pastikan index dan potongan.json berada di folder data/."
    )


AKAR = akar_sesi()
BERKAS_INDEX = AKAR / "index_lindungiku.faiss"
BERKAS_POTONGAN = AKAR / "potongan.json"

index = faiss.read_index(str(BERKAS_INDEX))
potongan = json.loads(BERKAS_POTONGAN.read_text(encoding="utf-8"))

assert index.ntotal == len(potongan), (
    f"index berisi {index.ntotal} vector, potongan.json berisi {len(potongan)} "
    "potongan. Keduanya harus sama. Bangun ulang dari notebook Sesi 11."
)

client = ollama.Client()


def normalisasi(v):
    panjang = np.linalg.norm(v, axis=1, keepdims=True)
    panjang[panjang == 0] = 1e-12
    return v / panjang


def _embed_pertanyaan(teks):
    # task_type untuk pertanyaan berbeda dari task_type untuk dokumen.
    # Tertukar tidak memunculkan error, hanya membuat hasil pencarian melemah.
    resp = client.embed(
        model=MODEL_EMBED,
        input=teks
    )

    v = np.array(resp.embeddings, dtype="float32")
    return normalisasi(v)


def cari(pertanyaan, k=3):
    """Kembalikan k potongan paling relevan dari knowledge base Sesi 11.

    Setiap potongan adalah dict dengan kunci 'teks' dan 'sumber'.
    """
    q = _embed_pertanyaan(pertanyaan)
    skor, baris = index.search(q, k)
    hasil = []
    for nilai, i in zip(skor[0], baris[0]):
        item = dict(potongan[i])
        item["skor"] = float(nilai)
        hasil.append(item)
    return hasil


def konteks(pertanyaan, k=3):
    """Gabungkan k potongan teratas menjadi satu blok teks siap pakai."""
    return "\n\n".join(p["teks"] for p in cari(pertanyaan, k))


if __name__ == "__main__":
    print(f"index  : {BERKAS_INDEX}")
    print(f"vector : {index.ntotal}")
    for p in cari("masa tunggu klaim rawat inap", k=3):
        print(f"\n[{p['skor']:.3f}] {p['sumber']}")
        print(p["teks"][:160].replace("\n", " "))
