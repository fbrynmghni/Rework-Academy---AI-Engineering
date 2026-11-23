"""
Bentuk data yang diterima API (bagian dari API layer).

File ini hanya berisi deklarasi, tanpa logika. Pydantic membaca deklarasi di
sini, lalu FastAPI menolak request yang tidak sesuai dengan status 422,
sebelum satu baris pun kode endpoint dijalankan.
"""

from pydantic import BaseModel


# TODO 2a: class Pesanan(BaseModel) dengan field nama (str) dan jumlah (int)
class Pesanan(BaseModel):
    nama: str
    jumlah: int