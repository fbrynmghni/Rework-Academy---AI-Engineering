# Sesi 2 — Bagian 2.4: Git & GitHub (Latihan Merge Conflict)

Folder ini berisi skenario latihan untuk mempraktikkan **merge conflict** — situasi yang pasti akan Anda temui saat berkolaborasi dengan Git.

## Isi folder

- `setup_conflict.sh` — skrip untuk membuat repo Git lokal yang sengaja menghasilkan conflict.  
- `mentor_solution.md` — langkah lengkap penyelesaian (versi mentor).

## Alur latihan (peserta)

1. Jalankan skrip untuk menyiapkan repo:

```sh
bash setup_conflict.sh
cd konflik_demo
```

2. Coba gabungkan branch `feature-harga` ke `main`:

```sh
git merge feature-harga
```

   Git akan melaporkan:

```
CONFLICT (content): Merge conflict in produk.py
Automatic merge failed; fix conflicts and then commit the result.
```

   Ini **normal**, bukan error yang berbahaya. Git hanya minta Anda memilih.

   

3. Buka `produk.py`. Anda akan melihat penanda conflict:

```
<<<<<<< HEAD
harga = 27000
=======
harga = 30000
>>>>>>> feature-harga
```

   - Bagian atas (`HEAD`) \= versi di branch `main`.  
   - Bagian bawah \= versi dari `feature-harga`.

   

4. **Selesaikan** dalam 4 langkah:  
     
   1. Pilih baris yang benar (mis. `harga = 30000`).  
   2. Hapus ketiga penanda (`<<<<<<<`, `=======`, `>>>>>>>`).  
   3. Simpan file, lalu `git add produk.py`.  
   4. `git commit` untuk menyelesaikan merge.

## Referensi

Video git-tower — "Dealing with Merge Conflicts": [https\://www\.git-tower.com/learn/git/ebook/en/command-line/advanced-topics/merge-conflicts](https://www.git-tower.com/learn/git/ebook/en/command-line/advanced-topics/merge-conflicts)

> Catatan: pesan Git (logs, warning, error) sengaja dibiarkan dalam bahasa Inggris.