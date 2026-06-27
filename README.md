# Mini Project: Integrasi Struktur Data untuk Pipeline Analisis Sederhana
Nama: Rakazaki Putra Hendrawan 
NIM: G0401241056
Mata Kuliah: **Struktur Data Bioinformatika (BIF1223)** — Pertemuan #15
Dosen: Toto Haryanto

## Deskripsi

Pipeline sederhana untuk menganalisis sekuens DNA (format FASTA), meliputi:

1. Membaca file FASTA → disimpan dalam **List**
2. Menghitung frekuensi nukleotida (A/T/G/C) → disimpan dalam **Dictionary**
3. Menghitung **GC Content** setiap sekuens
4. Mengurutkan sekuens berdasarkan GC Content (descending)
5. Menampilkan 3 sekuens dengan GC Content tertinggi
6. Visualisasi GC Content (bar chart)
7. Menyimpan seluruh hasil ke file CSV

## Struktur Repository

```
.
├── mini_project_pipeline.ipynb   # Notebook utama (kode + output, data asli)
├── pipeline.py                   # Versi script .py (sama logika, untuk dijalankan via terminal)
├── hypsibius_dujardini.fasta     # Data sekuens asli (9 sekuens, NCBI)
├── hasil_gc_content.csv          # Output CSV hasil analisis
├── gc_content_chart.png          # Output grafik hasil analisis
├── Laporan_Mini_Project.pdf      # Laporan tugas (PDF)
└── README.md
```

## Cara Menjalankan

```bash
pip install matplotlib pandas
python3 pipeline.py
# atau buka & jalankan mini_project_pipeline.ipynb di Jupyter
```

Untuk menggunakan data lain: ganti file `hypsibius_dujardini.fasta` dengan file FASTA/FASTQ
lain, lalu ubah nama file pada pemanggilan `read_fasta(...)`.

## Data

Sekuens yang dianalisis adalah 9 sekuens dari organisme **_Hypsibius dujardini_** (tardigrade/water
bear), diunduh dari [NCBI Nucleotide](https://www.ncbi.nlm.nih.gov/nuccore):

| Jenis Sekuens | Jumlah | Accession Number |
|---|---|---|
| EST (cDNA), mirip gen RecG (ATP-dependent DNA helicase) | 1 | CF544295.1 |
| Gen COX1 (cytochrome c oxidase subunit I, mitokondria) | 4 | PQ356833.1 - PQ356836.1 |
| Region ITS (Internal Transcribed Spacer, non-coding) | 4 | PQ354674.1 - PQ354677.1 |

> **Catatan taksonomi:** Sejak redeskripsi oleh Gasiorek dkk. (2018), strain laboratorium yang
> banyak digunakan untuk studi genom dan umum disebut *H. dujardini* telah direklasifikasi sebagai
> spesies baru, *H. exemplaris*. Sekuens pada repo ini diunduh dengan label *H. dujardini* sesuai
> NCBI Taxonomy (taxid 232323).

**Insight hasil:** Sekuens region ITS (non-coding) dan EST nuklir punya GC Content lebih tinggi
(49-55%) dibanding gen COX1 mitokondria (37-38%) — sejalan dengan pola AT-richness yang umum pada
genom mitokondria hewan.

## Author

[ISI NAMA KAMU] — [ISI NIM KAMU]
