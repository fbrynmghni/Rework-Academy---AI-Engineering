# Sesi 13: Developing AI Backend & API Services

Satu project API yang dibangun bertahap sepanjang sesi. Setiap folder adalah **titik awal** satu bagian: isinya hasil akhir bagian sebelumnya, ditambah TODO untuk hal baru di bagian itu saja. Anda tidak mulai dari nol di setiap bagian.

| Folder | Yang Anda kerjakan |
| :---- | :---- |
| `13-1_hello_api/` | endpoint pertama, `GET /` |
| `13-2_arsitektur/` | tidak ada kode baru; mengenal tiga layer dan menguji masing-masing |
| `13-3_validasi/` | `POST /pesan`, tanpa lalu dengan Pydantic |
| `13-4_layanan_ai/` | `/ask`, `/summarize`, `/analyze`, response yang seragam, error handling |

Tertinggal di satu bagian? Tidak masalah. Pindah saja ke folder bagian berikutnya: isinya sudah memuat hasil akhir bagian yang Anda lewatkan.

## Menyiapkan (lihat juga "Persiapan Sebelum Kelas \- Sesi 13")

Di folder `sesi-13/` (folder ini):

- `.env` berisi `GEMINI_API_KEY`. Satu file untuk semua bagian.  
- `index_lindungiku.faiss` dan `potongan.json` dari Sesi 11, disalin ke `13-2_arsitektur/data/` dan `13-4_layanan_ai/data/`.

## Menjalankan

Server selalu dijalankan dari folder bagian yang sedang dipakai, bukan dari dalam `app/`:

```
cd 13-1_hello_api
uvicorn app.main:app --reload
```

Pindah bagian: hentikan server (`Ctrl + C`), `cd ../13-2_arsitektur`, jalankan lagi.