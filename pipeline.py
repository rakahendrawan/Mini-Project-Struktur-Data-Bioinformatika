"""
Mini Project - Integrasi Struktur Data untuk Pipeline Analisis Sederhana
Mata Kuliah: Struktur Data Bioinformatika (BIF1223)

Pipeline ini melakukan:
1. Membaca file FASTA -> disimpan dalam List
2. Menghitung frekuensi nukleotida per sekuens -> disimpan dalam Dictionary
3. Menghitung GC Content & mengurutkan sekuens berdasarkan GC Content
4. Menampilkan 3 sekuens dengan GC Content tertinggi
5. Visualisasi GC Content tiap sekuens (bar chart)
6. Menulis hasil ke file CSV
"""

import csv
import matplotlib
matplotlib.use("Agg")  # backend non-interaktif (aman untuk dijalankan tanpa display)
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# 1. BACA FILE FASTA -> List
# ----------------------------------------------------------------------
def read_fasta(filepath):
    """
    Membaca file FASTA dan menyimpan setiap record sebagai dictionary
    di dalam sebuah List.

    Struktur data yang dipakai:
        - List   -> menampung seluruh record sekuens
        - Dict   -> menyimpan id, deskripsi, dan sekuens per record

    Return: List[dict] dengan key: 'id', 'description', 'sequence'
    """
    sequences = []          # <- List utama
    current_id = None
    current_desc = ""
    current_seq = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                # simpan record sebelumnya (kalau ada) sebelum mulai record baru
                if current_id is not None:
                    sequences.append({
                        "id": current_id,
                        "description": current_desc,
                        "sequence": "".join(current_seq).upper()
                    })
                header = line[1:].split(" ", 1)
                current_id = header[0]
                current_desc = header[1] if len(header) > 1 else ""
                current_seq = []
            else:
                current_seq.append(line)

        # simpan record terakhir
        if current_id is not None:
            sequences.append({
                "id": current_id,
                "description": current_desc,
                "sequence": "".join(current_seq).upper()
            })

    return sequences


# ----------------------------------------------------------------------
# 2. HITUNG FREKUENSI NUKLEOTIDA -> Dictionary
# ----------------------------------------------------------------------
def nucleotide_frequency(sequence):
    """
    Menghitung jumlah kemunculan tiap basa nukleotida dalam satu sekuens.
    Struktur data: Dictionary (Hash Map) -> key = basa, value = jumlah.
    """
    freq = {"A": 0, "T": 0, "G": 0, "C": 0, "N": 0}
    for base in sequence:
        if base in freq:
            freq[base] += 1
        else:
            freq["N"] += 1  # basa ambigu (selain A/T/G/C) dihitung sebagai N
    return freq


# ----------------------------------------------------------------------
# 3. HITUNG GC CONTENT
# ----------------------------------------------------------------------
def gc_content(freq, length):
    """GC Content (%) = (jumlah G + jumlah C) / panjang sekuens * 100"""
    if length == 0:
        return 0.0
    return (freq["G"] + freq["C"]) / length * 100


# ----------------------------------------------------------------------
# PIPELINE UTAMA
# ----------------------------------------------------------------------
def run_pipeline(fasta_path, output_csv="hasil_gc_content.csv", output_chart="gc_content_chart.png"):

    # --- Tahap 1: Baca FASTA ---
    sequences = read_fasta(fasta_path)
    print(f"[1] Berhasil membaca {len(sequences)} sekuens dari '{fasta_path}'")

    # --- Tahap 2 & 3: Hitung frekuensi nukleotida + GC content per sekuens ---
    results = []
    for record in sequences:
        seq = record["sequence"]
        freq = nucleotide_frequency(seq)
        gc = gc_content(freq, len(seq))
        results.append({
            "id": record["id"],
            "description": record["description"],
            "length": len(seq),
            "freq": freq,
            "gc_content": round(gc, 2)
        })

    print(f"[2] Frekuensi nukleotida dihitung untuk setiap sekuens (struktur: Dictionary)")

    # Contoh tampilan frekuensi nukleotida sekuens pertama
    contoh = results[0]
    print(f"    Contoh - {contoh['id']}: {contoh['freq']} (panjang={contoh['length']} bp)")

    # --- Tahap 4: Urutkan berdasarkan GC content (descending) ---
    results_sorted = sorted(results, key=lambda x: x["gc_content"], reverse=True)
    print(f"[3] Sekuens diurutkan berdasarkan GC Content (tertinggi -> terendah)")

    # --- Tahap 5: Tampilkan 3 sekuens terbaik ---
    top3 = results_sorted[:3]
    print("\n[4] 3 Sekuens dengan GC Content tertinggi:")
    print(f"    {'No':<4}{'ID':<15}{'Panjang (bp)':<15}{'GC Content (%)':<15}")
    for i, r in enumerate(top3, 1):
        print(f"    {i:<4}{r['id']:<15}{r['length']:<15}{r['gc_content']:<15}")

    # --- Tahap 6: Visualisasi ---
    ids = [r["id"] for r in results_sorted]
    gc_values = [r["gc_content"] for r in results_sorted]
    top3_ids = {r["id"] for r in top3}
    colors = ["#2E86AB" if sid not in top3_ids else "#E63946" for sid in ids]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(ids, gc_values, color=colors)
    plt.axhline(y=sum(gc_values) / len(gc_values), color="gray", linestyle="--",
                linewidth=1, label="Rata-rata GC%")
    plt.xlabel("ID Sekuens")
    plt.ylabel("GC Content (%)")
    plt.title("GC Content per Sekuens (merah = Top 3 tertinggi)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_chart, dpi=150)
    plt.close()
    print(f"\n[5] Grafik GC Content disimpan ke '{output_chart}'")

    # --- Tahap 7: Simpan hasil ke CSV ---
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "ID", "Deskripsi", "Panjang (bp)", "A", "T", "G", "C",
                          "GC_Content (%)"])
        for rank, r in enumerate(results_sorted, 1):
            writer.writerow([
                rank, r["id"], r["description"], r["length"],
                r["freq"]["A"], r["freq"]["T"], r["freq"]["G"], r["freq"]["C"],
                r["gc_content"]
            ])
    print(f"[6] Hasil lengkap disimpan ke '{output_csv}'")

    return results_sorted, top3


if __name__ == "__main__":
    run_pipeline("hypsibius_dujardini.fasta")
