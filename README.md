# SDI Minggu 9 — Repository dan Pipeline Otomatis

Mata kuliah: Software Deployment and Implementation, TI247010, 3 SKS. Pengampu: Agus Barlianto, M.Kom.

Pada minggu 9, Anda mengubah rancangan pipeline menjadi repository yang dapat dijalankan. Hasil akhirnya adalah CI yang menjalankan pemeriksaan syntax, unit test, integration test CLI, kemudian membuat kandidat beridentitas hanya jika seluruh pemeriksaan berhasil.

## Capaian dan hubungan dengan RPS

RPS minggu 9 menetapkan Sub-CPMK 4: implementasi repository dan pipeline build serta unit test otomatis, dengan unit/integration test dasar. Bukti pengumpulan berupa tautan repo dan laporan. Praktikum ini melanjutkan kontrak modul proyek UTS; minggu 10 membahas deployment otomatis dan verifikasinya.

Setelah praktikum, Anda dapat:

1. Menata source, test, versi, dan workflow pada repository Git.
2. Membedakan unit test fungsi dari integration test yang menjalankan CLI sebagai proses terpisah.
3. Menunjukkan bahwa kegagalan test menghentikan pembuatan kandidat pada run yang sama.
4. Menautkan kandidat ke commit, run, attempt, dan checksum yang sesuai.

## Alokasi kelas 150 menit

| Kegiatan | Menit |
|---|---:|
| Pertanyaan pembuka dan prediksi hasil | 10 |
| Penataan repository dan kontrak | 15 |
| Demo unit test dan integration test | 20 |
| Membaca workflow dan demo gate | 20 |
| Praktikum tiga eksperimen | 60 |
| Pemeriksaan bukti bersama | 15 |
| Exit ticket individual | 10 |
| Total | 150 |

## 1 Persiapan

- Unduh dan ekstrak `Starter_Code_SDI_Minggu_9.zip`. Buka folder `sdi-minggu9`.
- Gunakan Python 3.12 dan terminal editor. Seluruh kode memakai pustaka standar; tidak ada paket pip yang perlu dipasang.
- Untuk perintah dalam panduan, gunakan `python`. Jika berbeda di perangkat Anda, ganti dengan `py -3.12` di Windows atau `python3` di macOS/Linux. Periksa dengan `python --version`.
- Siapkan akun GitHub dan repository latihan baru `sdi-minggu9-NIM`. Gunakan visibility dan akses baca dosen sesuai kebijakan kelas. Aktifkan Actions bila diminta oleh GitHub.
- Jika sudah memakai Codespaces dan dapat membukanya, terminalnya dapat dipakai. Penggunaan layanan cloud mengikuti akses dan kuota akun; Codespaces bukan syarat praktikum.

| File | Fungsi |
|---|---|
| `app.py` | Fungsi bisnis dan pintu masuk command-line interface atau CLI |
| `test_unit.py` | Menguji fungsi `biaya()` secara langsung |
| `test_integration.py` | Menguji parser, fungsi, output, dan exit status melalui proses CLI |
| `package.py` | Membuat ZIP source, manifest dan checksum |
| `verify.py` | Memeriksa satu ZIP terhadap file checksum pendamping |
| `VERSION` | Versi aplikasi pada kandidat |
| `.github/workflows/ci.yml` | Definisi workflow GitHub Actions |
| `.gitignore` | Mengabaikan cache, environment lokal dan hasil packaging |

## 2 Kontrak modul biaya

Kontrak ini sama dengan proyek UTS, termasuk pembebasan biaya di bawah Rp50.000. Latihan CI sebelum UTS pernah memakai aturan tanpa pembebasan biaya; untuk minggu 9 gunakan aturan berikut secara konsisten.

- Fungsi `biaya(amount)` menerima integer rupiah nonnegatif. String, float, boolean, `None`, dan angka negatif ditolak dengan `ValueError`.
- Untuk `amount < 50_000`, hasilnya 0.
- Mulai `amount == 50_000`, biaya adalah 1% dibulatkan ke bawah ke rupiah utuh, maksimal Rp5.000.
- Hasil fungsi bertipe integer. Implementasi memakai pembagian integer agar perhitungan tidak bergantung pada pembulatan floating point.

| Input fungsi | Expected output |
|---|---:|
| 0 | 0 |
| 49.999 | 0 |
| 50.000 | 500 |
| 123.456 | 1.234 |
| 275.550 | 2.755 |
| 500.000 | 5.000 |
| 900.000 | 5.000 |
| -1, string, float, boolean, None | ValueError |

CLI membaca teks argumen pengguna dan mengubahnya menjadi integer sebelum memanggil fungsi. Jadi `python app.py 50000` sah, sedangkan pemanggilan langsung `biaya("50000")` tetap ditolak. Jalur parsing CLI dan kontrak tipe fungsi berbeda.

## 3 Menjalankan dan membaca test

Dari folder yang memuat `app.py`, jalankan setiap perintah berikut secara terpisah:

```bash
python app.py 50000
python -m unittest -v test_unit
python -m unittest -v test_integration
python -m unittest -v test_unit test_integration
```

Hasil awal: CLI mencetak `500`; 9 metode unit test dan 3 metode integration test lulus, total 12 metode. `test_wrong_types` memuat beberapa subtest, sehingga jumlah metode bukan jumlah seluruh input uji.

**Unit test** memanggil `biaya()` langsung. Ia menguji aturan gratis, nilai batas, perhitungan, maksimum, dan penolakan input. **Integration test** menjalankan `app.py` melalui `subprocess.run()`, kemudian memeriksa hasil gabungan parser, fungsi bisnis dan keluaran proses.

`sys.executable` memakai interpreter Python yang menjalankan test. `capture_output=True` menangkap stdout dan stderr. `returncode` menunjukkan status akhir proses. Pada CLI ini, input benar menghasilkan status 0, nominal negatif atau teks bukan angka menghasilkan status 2 melalui `argparse`.

Integration test ini terbatas pada CLI dan modul bisnis. Ia belum menguji database, jaringan, antarmuka web, deployment, atau ketahanan production. Test lulus memberi bukti atas kasus yang diuji.

**Latihan mandiri sebelum eksperimen remote:** tambahkan dua metode unit test baru dan satu metode integration test baru, lengkap dengan alasan expected output. Pilih kasus batas yang belum dicakup, misalnya nominal satu rupiah di atas ambang atau satu rupiah di bawah batas cap. Jangan hanya mengganti nama test yang sudah ada. Setelah tambahan ini, minimal 11 metode unit dan 4 metode integration harus lulus.

## 4 Memasang workflow pada GitHub

1. Buat repository latihan melalui GitHub. Beri akses baca dosen jika privat.
2. Masukkan `app.py`, kedua file test, `package.py`, `verify.py`, `VERSION`, `.gitignore`, dan README ke root repository. Source tidak boleh tersimpan satu tingkat di dalam folder `sdi-minggu9` pada repo.
3. Buat workflow terakhir. Melalui browser, pilih **Add file > Create new file**. Ketik nama lengkap `.github/workflows/ci.yml`, lalu salin isi file workflow yang tersedia pada starter kit. Cara ini juga memastikan folder tersembunyi `.github` ikut masuk repo.
4. Commit perubahan. Buka **Actions > SDI Minggu 9**, lalu pilih run untuk commit tersebut. Workflow juga bisa dijalankan manual setelah file ada di default branch.
5. Baca log setiap langkah. Jangan hanya melihat ikon status keseluruhan.

Workflow dipicu oleh push, pull request atau pemicu manual. Satu job memakai runner `ubuntu-latest`, mengambil source dan menyiapkan Python 3.12. Langkah selanjutnya adalah syntax check, unit test, integration test, packaging, dan upload kandidat. Permissions `contents: read` cukup untuk mengambil source dalam latihan ini.

`compileall` memeriksa syntax Python; ia bukan unit test dan bukan kompilasi menjadi aplikasi mandiri. Build kandidat latihan ini mencakup penyiapan serta pengemasan source. ZIP tetap membutuhkan interpreter Python.

Pada workflow yang diberikan, langkah berikutnya berjalan dengan kondisi sukses default. Jangan menambahkan `continue-on-error: true`, `if: always()`, atau menyembunyikan exit status gagal pada langkah gate/packaging. Kegagalan unit test membuat integration test dan langkah berikutnya dilewati; jika unit test lulus tetapi integration test gagal, packaging dan upload dilewati.

Versi action pada contoh: `checkout@v6`, `setup-python@v5` dan `upload-artifact@v4`, mengikuti contoh dokumentasi resmi yang diperiksa pada 27 Oktober 2026. Ini bukan klaim bahwa semuanya versi paling baru. `python-version: '3.12'` mengatur versi Python, bukan versi action. Latihan memakai GitHub.com dengan GitHub-hosted runner.

## 5 Tiga eksperimen wajib

Simpan eksperimen sebagai tiga commit berbeda. Pertahankan test saat sengaja memasukkan bug.

| Eksperimen | Perubahan | Hasil yang diharapkan |
|---|---|---|
| A Baseline | Implementasi benar dan tambahan test mahasiswa | Syntax, unit, integration, package dan upload berhasil |
| B Bug batas | Pada `app.py`, ubah `if amount < 50_000:` menjadi `if amount <= 50_000:` | Test input 50.000 gagal: expected 500, actual 0. Packaging dan upload run B dilewati |
| C Perbaikan | Kembalikan operator `<`; pertahankan seluruh test | Test lulus, kandidat dari commit/run C tersedia |

Jangan menghapus atau mengubah expected output menjadi 0 agar eksperimen B lulus. Saat menjalankan seluruh starter test lokal, bug tersebut menggagalkan unit test batas dan integration test CLI batas. Dalam workflow, unit test lebih dahulu gagal sehingga langkah integration belum dijalankan.

Artifact run A boleh tetap tersedia ketika run B gagal. Keberadaannya tidak menunjukkan bahwa run B menghasilkan kandidat. Cocokkan commit dan run pembuatnya. Perubahan label versi juga tidak membuktikan suatu kandidat lulus test.

Biarkan `VERSION` tetap `1.0.0` untuk ketiga eksperimen agar peran identitas commit/run terlihat. Bug sengaja ini bukan rilis production. Nomor versi saja tidak menggantikan identitas build. `run_attempt` membedakan percobaan ulang pada run yang sama.

## 6 Memeriksa kandidat

1. Pada ringkasan run C, unduh artifact bernama `sdi-m9-...`.
2. Ekstrak ZIP pembungkus unduhan GitHub. Di dalamnya ada ZIP kandidat `sdi-m9-1.0.0-...zip` dan file `.zip.sha256`. Jangan menghitung checksum pembungkus sebagai pengganti ZIP kandidat.
3. Salin `verify.py` ke folder yang memuat kedua file tersebut, atau panggil script dengan path yang sesuai.
4. Ganti nama contoh di bawah dengan nama ZIP kandidat yang benar:

```bash
python verify.py sdi-m9-1.0.0-CONTOH.zip
```

Nama `CONTOH` adalah placeholder, bukan file yang disediakan. Pilih satu ZIP yang sedang diperiksa; jangan mencampur pasangan file dari run lain. Hasil harus `MATCH`.

5. Ekstrak ZIP kandidat ke folder baru dan baca `manifest.json`. Cocokkan versi, commit, `build_run`, dan `run_attempt` dengan run pembuatnya.
6. Dari hasil ekstraksi, jalankan `python app.py 50000`; hasilnya `500`.

Checksum mendukung kesamaan byte relatif terhadap nilai pembanding. Jika ZIP dan file checksum sama-sama diganti, hasil MATCH saja belum membuktikan sumber terpercaya. Gunakan nilai dan metadata dari run pembuat yang dapat ditelusuri. Workflow ini menghasilkan kandidat CI; ia belum melakukan deployment ke staging atau production.

## 7 Bukti dan tugas individual

Unggah laporan maksimal 2 halaman ke eLearning. Tenggat mengikuti aktivitas tugas pada eLearning. Lampirkan:

1. Nama/NIM, tautan repo, dan tautan tiga run A/B/C.
2. Tabel tiga commit dan run, hasil unit/integration test, status packaging/upload serta identitas kandidat yang tersedia. Tulis “dilewati” jika suatu langkah belum berjalan, bukan “lulus”.
3. Dua unit test baru dan satu integration test baru yang dibuat sendiri, termasuk alasan expected output.
4. Manifest kandidat C dan hasil verifikasi checksum, dengan nama file yang diperiksa.
5. Jawaban singkat: mengapa unit test gagal pada B, mengapa artifact A tetap tersedia, apa tambahan yang diuji lewat CLI, dan apa yang belum dibuktikan test/checksum ini.

Siapkan penjelasan individual sekitar 2 menit: jalankan satu test pilihan dosen dan jelaskan hubungan commit, run serta kandidat. Bantuan AI diperbolehkan untuk belajar dan memperbaiki kode; nyatakan bagian yang dibantu dan cara memeriksa hasilnya. Anda harus dapat menjelaskan perubahan sendiri. Jangan memasukkan password/token ke source, screenshot atau laporan.

| Aspek | Poin |
|---|---:|
| Struktur repository dan kontrak program benar | 20 |
| Unit test dan alasan kasus tambahan | 25 |
| Integration test CLI dan pemahaman exit status | 20 |
| Tiga eksperimen CI serta keterlacakan kandidat | 25 |
| Laporan dan penjelasan individual | 10 |
| Total skala aktivitas | 100 |

RPS mengalokasikan bobot 5% pada minggu 9. Rubrik 100 poin di atas adalah usulan skala penilaian aktivitas; penerapannya mengikuti kontrak kelas dan diumumkan sebelum pengumpulan. Praktikum ini bukan pengganti komponen proyek UTS 40%.

## 8 Troubleshooting dan jalur cadangan

| Gejala | Pemeriksaan pertama |
|---|---|
| Modul tidak ditemukan | Terminal dan file Python berada pada root repo, nama file tepat |
| Actions tidak muncul | Path `.github/workflows/ci.yml`, YAML dan izin Actions repo |
| Workflow merah sebelum test | Baca log checkout/setup/syntax, jangan langsung mengubah test |
| Bug B tetapi run hijau | Operator pada commit/run yang benar, test batas masih aktif |
| Tidak ada kandidat run B | Ini hasil yang benar jika gate gagal dan upload dilewati |
| Verifikasi MISMATCH | Nama dan pasangan ZIP/checksum, pembungkus versus kandidat |
| Artifact lama masih terlihat | Periksa run pemilik dan masa retensi; jangan menganggapnya hasil run baru |
| GitHub menolak menjalankan Actions | Periksa kebijakan repo/organisasi dan pembatasan akun |

Jika internet atau Actions belum tersedia, lakukan percobaan lokal dengan perintah terpisah. Jalankan packaging **hanya sesudah** seluruh test lulus. Untuk B, berhenti setelah test gagal. Labeli bukti sebagai “lokal”, bukan run GitHub; manifest akan mencatat run/attempt `local`. Jika belum ada Git repo, commit juga `local`. Lengkapi bukti remote ketika akses tersedia sesuai arahan dosen. Local run tidak membuktikan CI otomatis.

Untuk membuat kandidat lokal setelah test lulus:

```bash
python package.py
```

File tersimpan di `dist`. Folder ini tidak di-commit. Script packaging tidak menjalankan test sendiri: urutan dan penolakan kandidat menjadi tanggung jawab workflow atau prosedur lokal yang Anda ikuti.

## Exit ticket

1. Bagian apa yang diuji integration test CLI tetapi tidak dicakup pemanggilan langsung fungsi?
2. Mengapa run B yang merah dapat menunjukkan gate bekerja dengan benar?
3. Bukti apa yang Anda cocokkan agar ZIP yang diunduh benar-benar berasal dari run C?
4. Apakah kandidat ini sudah dideploy? Apa yang perlu ditambahkan pada minggu 10?

## Referensi

- RPS kelas, `RPS - Software Deployment and Implementation_TI.docx`, tabel rencana pembelajaran minggu 9–10, halaman PDF hasil pembacaan 9.
- Materi kelas sebelumnya, `SDI_Minggu_Ini_CICD_Artifact_Versioning.md`.
- GitHub, Building and testing Python: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- GitHub, Store and share data with workflow artifacts: https://docs.github.com/en/actions/tutorials/store-and-share-data
- GitHub, Evaluate expressions in workflows: https://docs.github.com/en/actions/reference/evaluate-expressions-in-workflows-and-actions
- Python 3.12, unittest: https://docs.python.org/3.12/library/unittest.html
- Python 3.12, subprocess: https://docs.python.org/3.12/library/subprocess.html

Dokumentasi daring diperiksa 27 Oktober 2026. Paket pembelajaran ini menargetkan Python 3.12; hasil eksekusi pada akun GitHub mahasiswa perlu dibuktikan melalui run masing-masing.
