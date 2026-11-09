# SDI Minggu 9: Repository dan Pipeline Otomatis

Tugas praktikum mata kuliah Software Deployment and Implementation (TI247010).

- Nama: Judika Marpaung
- NIM: 2314000021
- Program studi: S1 Teknik Informatika, Fakultas Teknologi Informasi
- Universitas: Perbanas Institute Jakarta
- Pengampu: Agus Barlianto, M.Kom.

## Tentang proyek

Repositori ini berisi modul penghitung biaya layanan koperasi berbasis command-line interface (CLI), lengkap dengan unit test, integration test, dan pipeline GitHub Actions. Pipeline memeriksa syntax, menjalankan kedua jenis test, lalu membuat kandidat ZIP beridentitas (commit, run, dan attempt) beserta checksum SHA-256, hanya jika seluruh pemeriksaan sebelumnya berhasil.

## Aturan biaya

Fungsi `biaya(amount)` menerima integer rupiah nonnegatif.

| Nominal | Biaya |
|---|---|
| kurang dari 50.000 | 0 |
| mulai 50.000 | 1% dibulatkan ke bawah, maksimal 5.000 |

String, float, boolean, `None`, dan angka negatif ditolak dengan `ValueError`. CLI mengubah teks argumen menjadi integer lebih dahulu, sehingga `python app.py 50000` sah, sedangkan `biaya("50000")` dari kode tetap ditolak.

## Cara menjalankan

Hanya memakai pustaka standar Python (target Python 3.12), tanpa paket tambahan.

```bash
python app.py 50000
python -m unittest -v test_unit
python -m unittest -v test_integration
```

Keluaran `python app.py 50000` adalah `500`. Input negatif atau bukan angka menghasilkan exit status 2.

## Struktur file

| File | Fungsi |
|---|---|
| `app.py` | Fungsi `biaya()` dan pintu masuk CLI |
| `test_unit.py` | 11 unit test untuk `biaya()` |
| `test_integration.py` | 4 integration test yang menjalankan CLI sebagai proses terpisah |
| `package.py` | Membuat ZIP kandidat, `manifest.json`, dan file `.sha256` |
| `verify.py` | Memeriksa satu ZIP terhadap file checksum pendampingnya |
| `VERSION` | Versi aplikasi (1.0.0) |
| `.github/workflows/ci.yml` | Definisi pipeline GitHub Actions |

## Pipeline CI

Urutan langkah pada `ci.yml`: syntax check, unit test, integration test, packaging, lalu upload artifact. Kegagalan pada satu langkah menghentikan langkah sesudahnya.

Memeriksa kandidat yang diunduh dari run:

```bash
python verify.py sdi-m9-1.0.0-<commit>-<run>-<attempt>.zip
```

Hasil yang diharapkan adalah `MATCH`. Checksum hanya membuktikan kesamaan byte terhadap file `.sha256` pendamping; ia tidak membuktikan keaslian sumber. Kandidat ini hasil CI dan belum dideploy.

## Tiga eksperimen

| Eksperimen | Commit | Perubahan | Hasil |
|---|---|---|---|
| A | `a8df89b` | Implementasi benar dan test tambahan | Seluruh langkah lulus, kandidat dibuat |
| B | `ab59b29` | Operator `<` diubah menjadi `<=` secara sengaja | Unit test batas gagal (`0 != 500`), packaging dan upload dilewati |
| C | `76e34b1` | Operator `<` dikembalikan | Seluruh langkah lulus, kandidat dibuat |

Setiap eksperimen dikirim sebagai commit terpisah sehingga memiliki run Actions sendiri.
