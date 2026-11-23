"""
Bentuk data yang diterima API (bagian dari API layer).

File ini hanya berisi deklarasi, tanpa logika. Pydantic membaca deklarasi di
sini, lalu FastAPI menolak request yang tidak sesuai dengan status 422,
sebelum satu baris pun kode endpoint dijalankan.
"""

from pydantic import BaseModel


# 13.3: request validation
class Pesanan(BaseModel):
    nama: str
    jumlah: int


# TODO 1a: class Pertanyaan(BaseModel) dengan field pertanyaan (str)
class Pertanyaan(BaseModel):
    pertanyaan: str

# TODO 3a: class Teks(BaseModel) dengan field teks (str)
class Teks(BaseModel):
    teks: str
