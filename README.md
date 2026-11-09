# SDI Minggu 9: Repository dan Pipeline Otomatis

Repositori ini adalah tugas praktikum Software Deployment and Implementation (TI247010) yang dibimbing Bapak Agus Barlianto, M.Kom.

Saya Judika Marpaung (NIM 2314000021), mahasiswa S1 Teknik Informatika, Fakultas Teknologi Informasi, Perbanas Institute Jakarta.

## Isi proyek

Proyek ini adalah program kecil untuk menghitung biaya layanan koperasi lewat command line. Aturannya sama dengan kontrak modul pada proyek UTS:

- nominal di bawah Rp50.000 tidak dikenai biaya;
- mulai Rp50.000, biayanya 1% dari nominal, dibulatkan ke bawah, dan paling besar Rp5.000;
- nilai yang bukan integer nonnegatif (string, float, boolean, `None`, atau angka negatif) ditolak dengan `ValueError`.

Fokus tugas ini bukan pada hitungannya, tetapi pada pipeline di sekitarnya: setiap push dicek otomatis oleh GitHub Actions, dan kandidat hasil build hanya dibuat kalau semua pemeriksaan lulus.

## Cara menjalankan

Cukup Python (saya memakai target 3.12) tanpa paket tambahan. Dari folder yang berisi `app.py`:

```bash
python app.py 50000
python -m unittest -v test_unit
python -m unittest -v test_integration
```

`python app.py 50000` mencetak `500`. Kalau inputnya negatif atau bukan angka, program berhenti dengan exit status 2.

Ada satu hal yang awalnya membingungkan bagi saya: `python app.py 50000` diterima, tetapi `biaya("50000")` dari kode ditolak. Penyebabnya, CLI mengubah teks menjadi integer lebih dulu sebelum memanggil fungsi, sedangkan fungsi itu sendiri ketat soal tipe.

## File di repositori

- `app.py`: fungsi `biaya()` dan pintu masuk CLI.
- `test_unit.py`: 11 unit test yang memanggil `biaya()` langsung.
- `test_integration.py`: 4 test yang menjalankan `app.py` sebagai proses terpisah, lalu memeriksa keluaran dan exit status.
- `package.py`: membuat ZIP kandidat, `manifest.json`, dan file checksum `.sha256`.
- `verify.py`: mencocokkan satu ZIP dengan checksum pendampingnya.
- `VERSION`: versi aplikasi, tetap 1.0.0 selama tiga eksperimen.
- `.github/workflows/ci.yml`: urutan langkah pipeline.

Test tambahan yang saya tulis sendiri ada tiga: `biaya(50_001)` harus 500, `biaya(499_999)` harus 4.999, dan CLI dengan input 49999 harus mencetak `0` dengan exit status 0 (biaya nol adalah hasil yang sah, bukan error).

## Pipeline

Urutan langkahnya: syntax check, unit test, integration test, packaging, lalu upload artifact. Karena langkah berikutnya hanya jalan kalau langkah sebelumnya sukses, test yang gagal otomatis menghentikan pembuatan kandidat.

Untuk memeriksa kandidat yang diunduh dari sebuah run:

```bash
python verify.py sdi-m9-1.0.0-<commit>-<run>-<attempt>.zip
```

Hasil yang benar adalah `MATCH`. Perlu diingat bahwa checksum hanya menunjukkan isi ZIP sama dengan nilai pembandingnya, bukan membuktikan asal-usulnya. Kandidat ini juga baru hasil CI, belum dideploy ke mana pun.

## Tiga eksperimen

Saya mengerjakannya sebagai tiga commit terpisah agar masing-masing punya run sendiri:

- **A (`a8df89b`)**: implementasi yang benar ditambah test tambahan. Semua langkah lulus dan kandidat terbentuk.
- **B (`ab59b29`)**: saya sengaja mengubah `<` menjadi `<=` pada kondisi gratis. Akibatnya `biaya(50_000)` menghasilkan 0, padahal seharusnya 500. Unit test batas gagal dengan pesan `0 != 500`, lalu integration test, packaging, dan upload dilewati. Test tidak saya ubah sama sekali.
- **C (`76e34b1`)**: operator dikembalikan menjadi `<`. Semua langkah lulus lagi dan kandidat terbentuk.

Dari eksperimen B saya melihat langsung bahwa run yang merah justru menandakan pipeline bekerja: bug tertangkap sebelum ada kandidat yang dibuat.
