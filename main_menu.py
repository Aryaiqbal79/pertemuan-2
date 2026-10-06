# ================================================================
#   SISTEM MANAJEMEN AKADEMIK & INVENTARIS
#   Menu Interaktif Terpadu
#   Modul: (1) Status Mahasiswa  (2) Diskon Biaya Kuliah
#          (3) Peringatan Stok   (0) Keluar
# ================================================================

import datetime

# ════════════════════════════════════════════════════════════════
#  UTILITAS UMUM
# ════════════════════════════════════════════════════════════════

LEBAR = 65

def garis(kar="=", lebar=LEBAR):
    print(kar * lebar)

def judul_box(teks, kar="=", lebar=LEBAR):
    garis(kar, lebar)
    print(teks.center(lebar))
    garis(kar, lebar)

def input_float(label, batas_bawah=None, batas_atas=None):
    """Input angka desimal dengan validasi rentang opsional."""
    while True:
        try:
            nilai = float(input(label))
            if batas_bawah is not None and nilai < batas_bawah:
                print(f"  [!] Nilai minimal {batas_bawah}. Coba lagi.")
                continue
            if batas_atas is not None and nilai > batas_atas:
                print(f"  [!] Nilai maksimal {batas_atas}. Coba lagi.")
                continue
            return nilai
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

def input_int(label, batas_bawah=0):
    """Input bilangan bulat dengan batas bawah opsional."""
    while True:
        try:
            nilai = int(input(label))
            if nilai < batas_bawah:
                print(f"  [!] Nilai minimal {batas_bawah}. Coba lagi.")
                continue
            return nilai
        except ValueError:
            print("  [!] Masukkan bilangan bulat yang valid.")

def input_yn(label):
    """Input y/n, kembalikan True/False."""
    while True:
        jawaban = input(label).strip().lower()
        if jawaban in ("y", "n"):
            return jawaban == "y"
        print("  [!] Masukkan 'y' atau 'n'.")

def tekan_enter():
    input("\n  [ Tekan Enter untuk kembali ke menu utama... ]")

def format_rupiah(nilai):
    return f"Rp {nilai:>15,.2f}"


# ════════════════════════════════════════════════════════════════
#  MODUL 1 — CEK STATUS MAHASISWA
# ════════════════════════════════════════════════════════════════

def status_mahasiswa_dari_ipk_sks(ipk, sks):
    if ipk < 1.5:
        return "Tidak Aktif"
    elif ipk < 2.0:
        return "Peringatan"
    else:
        return "Aktif" if sks >= 18 else "Peringatan"

def label_status_mhs(status):
    return {"Aktif": "[OK]", "Peringatan": "[!] ", "Tidak Aktif": "[X] "}.get(status, "")

def modul_status_mahasiswa():
    judul_box("  MODUL 1 — CEK STATUS MAHASISWA  ")

    mahasiswa = []
    while True:
        try:
            n = int(input("\n  Masukkan jumlah mahasiswa (1-20): "))
            if 1 <= n <= 20:
                break
            print("  [!] Jumlah harus antara 1 dan 20.")
        except ValueError:
            print("  [!] Masukkan bilangan bulat yang valid.")

    for i in range(1, n + 1):
        print(f"\n  --- Data Mahasiswa ke-{i} ---")
        nim  = input("  NIM  : ").strip() or f"MHS-{i:03}"
        nama = input("  Nama : ").strip() or f"Mahasiswa {i}"
        ipk  = input_float("  IPK  : ", 0.0, 4.0)
        sks  = input_int("  SKS  : ", 0)
        mahasiswa.append({"nim": nim, "nama": nama, "ipk": ipk, "sks": sks})

    # ── Laporan ──────────────────────────────────────────────
    print()
    judul_box("  LAPORAN STATUS MAHASISWA  ", "-")
    print(f"  {'No':<4} {'NIM':<12} {'Nama':<20} {'IPK':<7} {'SKS':<6} Status")
    garis("-")

    hitungan = {"Aktif": 0, "Peringatan": 0, "Tidak Aktif": 0}
    for idx, m in enumerate(mahasiswa, 1):
        st  = status_mahasiswa_dari_ipk_sks(m["ipk"], m["sks"])
        lbl = label_status_mhs(st)
        hitungan[st] += 1
        print(f"  {idx:<4} {m['nim']:<12} {m['nama'][:19]:<20} "
              f"{m['ipk']:<7.2f} {m['sks']:<6} {lbl} {st}")

    garis()
    print(f"\n  Ringkasan ({n} mahasiswa):")
    print(f"    [OK]  Aktif       : {hitungan['Aktif']} mahasiswa")
    print(f"    [!]   Peringatan  : {hitungan['Peringatan']} mahasiswa")
    print(f"    [X]   Tidak Aktif : {hitungan['Tidak Aktif']} mahasiswa")
    garis()
    tekan_enter()


# ════════════════════════════════════════════════════════════════
#  MODUL 2 — KALKULATOR DISKON BIAYA KULIAH
# ════════════════════════════════════════════════════════════════

def hitung_diskon(spp, anak_karyawan, ipk, tepat_waktu):
    """Kembalikan dict hasil kalkulasi diskon."""
    diskon_karyawan = 25 if anak_karyawan else 0
    if   ipk >= 3.8: diskon_ipk = 20
    elif ipk >= 3.5: diskon_ipk = 15
    elif ipk >= 3.0: diskon_ipk = 10
    else:            diskon_ipk = 0
    diskon_tepat  = 5 if tepat_waktu else 0
    diskon_utama  = max(diskon_karyawan, diskon_ipk)
    diskon_total  = min(diskon_utama + diskon_tepat, 100)
    potongan      = spp * diskon_total / 100
    return {
        "diskon_karyawan": diskon_karyawan,
        "diskon_ipk"     : diskon_ipk,
        "diskon_tepat"   : diskon_tepat,
        "diskon_utama"   : diskon_utama,
        "diskon_total"   : diskon_total,
        "potongan"       : potongan,
        "biaya_final"    : spp - potongan,
    }

def modul_diskon_biaya():
    judul_box("  MODUL 2 — KALKULATOR DISKON BIAYA KULIAH  ")

    print("\n[ INPUT DATA MAHASISWA ]\n")
    spp           = input_float("  Biaya SPP (Rp)        : ", batas_bawah=1)
    anak_karyawan = input_yn("  Anak karyawan?        (y/n) : ")
    ipk           = input_float("  IPK                   : ", 0.0, 4.0)
    tepat_waktu   = input_yn("  Bayar tepat waktu?    (y/n) : ")

    h = hitung_diskon(spp, anak_karyawan, ipk, tepat_waktu)

    # ── Laporan ──────────────────────────────────────────────
    print()
    judul_box("  RINCIAN DISKON  ", "-")

    if anak_karyawan:
        print(f"  Anak Karyawan              : {h['diskon_karyawan']}%")
    if h["diskon_ipk"] > 0:
        batas = {20: "3.8", 15: "3.5", 10: "3.0"}[h["diskon_ipk"]]
        print(f"  Diskon IPK >= {batas}           : {h['diskon_ipk']}%")
    else:
        print(f"  Diskon IPK                 : 0%  (IPK < 3.0)")
    if tepat_waktu:
        print(f"  Tepat Waktu (tambahan)     : {h['diskon_tepat']}%")

    garis("-")
    if anak_karyawan and h["diskon_ipk"] > 0:
        pilih = "Karyawan" if h["diskon_karyawan"] >= h["diskon_ipk"] else "IPK"
        print(f"  * Diskon utama ({pilih}) dipilih : {h['diskon_utama']}%")
        garis("-")
    print(f"  Total Diskon               : {h['diskon_total']}%")
    garis()
    print(f"\n  Biaya SPP Awal    : {format_rupiah(spp)}")
    print(f"  Potongan ({h['diskon_total']:>3}%)    : {format_rupiah(h['potongan'])}")
    garis("-")
    print(f"  BIAYA FINAL       : {format_rupiah(h['biaya_final'])}")
    garis()

    if h["diskon_total"] == 0:
        print("\n  Info: Tidak ada diskon yang berlaku.")
    elif h["diskon_total"] >= 30:
        print(f"\n  Selamat! Diskon besar {h['diskon_total']}% berhasil diterapkan.")
    else:
        print(f"\n  Diskon {h['diskon_total']}% berhasil diterapkan.")

    tekan_enter()


# ════════════════════════════════════════════════════════════════
#  MODUL 3 — PERINGATAN STOK INVENTARIS
# ════════════════════════════════════════════════════════════════

INVENTARIS = [
    {"kode":"ITM-001","nama":"Laptop Asus VivoBook",   "kategori":"Elektronik",  "stok":42, "stok_min":10,"harga":8_500_000},
    {"kode":"ITM-002","nama":"Mouse Wireless Logitech","kategori":"Aksesori",    "stok":18, "stok_min":15,"harga":  250_000},
    {"kode":"ITM-003","nama":"Keyboard Mechanical",    "kategori":"Aksesori",    "stok":7,  "stok_min":10,"harga":  750_000},
    {"kode":"ITM-004","nama":"Monitor LED 24\"",       "kategori":"Elektronik",  "stok":0,  "stok_min":5, "harga":2_200_000},
    {"kode":"ITM-005","nama":"Kertas HVS A4 (rim)",    "kategori":"ATK",         "stok":3,  "stok_min":20,"harga":   55_000},
    {"kode":"ITM-006","nama":"Tinta Printer Canon",    "kategori":"ATK",         "stok":12, "stok_min":15,"harga":   85_000},
    {"kode":"ITM-007","nama":"Headset Gaming Rexus",   "kategori":"Aksesori",    "stok":55, "stok_min":8, "harga":  450_000},
    {"kode":"ITM-008","nama":"Flash Disk 64GB",        "kategori":"Penyimpanan", "stok":0,  "stok_min":10,"harga":   95_000},
    {"kode":"ITM-009","nama":"SSD 256GB Samsung",      "kategori":"Penyimpanan", "stok":9,  "stok_min":5, "harga":  550_000},
    {"kode":"ITM-010","nama":"Webcam HD Logitech",     "kategori":"Elektronik",  "stok":30, "stok_min":5, "harga":  480_000},
]

PRIORITAS_STOK = {"HABIS": 1, "RENDAH": 2, "PERINGATAN": 3, "AMAN": 4}
LABEL_STOK     = {"HABIS": "[HABIS]", "RENDAH": "[RENDAH]",
                  "PERINGATAN": "[PERINGATAN]", "AMAN": "[AMAN]   "}

def status_stok(stok, stok_min):
    if stok == 0:           return "HABIS"
    if stok < stok_min:     return "RENDAH"
    if stok < stok_min * 2: return "PERINGATAN"
    return "AMAN"

def modul_peringatan_stok():
    judul_box("  MODUL 3 — PERINGATAN STOK INVENTARIS  ")

    # Evaluasi tiap item
    data = []
    for item in INVENTARIS:
        st = status_stok(item["stok"], item["stok_min"])
        data.append({**item,
                     "status"   : st,
                     "prioritas": PRIORITAS_STOK[st],
                     "nilai"    : item["stok"] * item["harga"]})

    data_sorted = sorted(data, key=lambda x: (x["prioritas"], x["nama"]))

    # ── Tabel Utama ───────────────────────────────────────────
    print(f"\n  {'LAPORAN INVENTARIS — Urut Prioritas':^{LEBAR-2}}")
    garis("-")
    print(f"  {'No':<4}{'Kode':<10}{'Nama Item':<23}{'Stok':>5}{'Min':>4}  {'Status':<13}{'Nilai Stok':>14}")
    garis("-")

    for no, item in enumerate(data_sorted, 1):
        lbl   = LABEL_STOK[item["status"]]
        stoks = "0(!)" if item["stok"] == 0 else str(item["stok"])
        nilai = f"Rp{item['nilai']:>12,.0f}"
        print(f"  {no:<4}{item['kode']:<10}{item['nama'][:22]:<23}"
              f"{stoks:>5}{item['stok_min']:>4}  {lbl:<13}{nilai}")

    garis("-")
    total_nilai = sum(i["nilai"] for i in data)
    print(f"  {'TOTAL NILAI INVENTARIS':>{LEBAR-20}} Rp{total_nilai:>12,.0f}")
    garis()

    # ── Ringkasan Statistik ───────────────────────────────────
    print(f"\n  {'RINGKASAN STATISTIK':^{LEBAR-2}}")
    garis("-")

    per_st = {"HABIS": [], "RENDAH": [], "PERINGATAN": [], "AMAN": []}
    for item in data:
        per_st[item["status"]].append(item["nama"])

    for st in ["HABIS", "RENDAH", "PERINGATAN", "AMAN"]:
        nama_singkat = ", ".join(n[:15] for n in per_st[st]) or "-"
        print(f"  {LABEL_STOK[st]:<14} {len(per_st[st]):>2} item  |  {nama_singkat}")

    garis("-")
    stok_list = [i["stok"] for i in data]
    print(f"  Total item    : {len(data)}")
    print(f"  Stok tertinggi: {max(stok_list)} unit  "
          f"({next(i['nama'] for i in data if i['stok']==max(stok_list))})")
    print(f"  Stok terendah : {min(stok_list)} unit  "
          f"({next(i['nama'] for i in data if i['stok']==min(stok_list))})")
    print(f"  Rata-rata stok: {sum(stok_list)/len(stok_list):.1f} unit")
    garis()

    # ── Tindakan Darurat ─────────────────────────────────────
    darurat = [i for i in data if i["status"] in ("HABIS", "RENDAH")]
    if darurat:
        print(f"\n  {'!! TINDAKAN SEGERA DIPERLUKAN !!':^{LEBAR-2}}")
        garis("-")
        for item in sorted(darurat, key=lambda x: x["prioritas"]):
            kekurangan = max(0, item["stok_min"] - item["stok"])
            print(f"  >> {item['kode']}  {item['nama'][:22]:<23} "
                  f"Stok:{item['stok']:>3}  Restock: +{kekurangan} unit")
        garis()
    else:
        print("\n  [OK] Semua item dalam kondisi aman.\n")
        garis()

    tekan_enter()


# ════════════════════════════════════════════════════════════════
#  MENU UTAMA
# ════════════════════════════════════════════════════════════════

def tampilkan_menu():
    sekarang = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M")
    print()
    judul_box("  SISTEM MANAJEMEN AKADEMIK & INVENTARIS  ")
    print(f"  Waktu : {sekarang}".ljust(LEBAR))
    garis("-")
    print("  [1]  Cek Status Mahasiswa")
    print("  [2]  Hitung Diskon Biaya Kuliah")
    print("  [3]  Cek Peringatan Stok Inventaris")
    garis("-")
    print("  [0]  Keluar")
    garis()

def main():
    MENU = {
        "1": modul_status_mahasiswa,
        "2": modul_diskon_biaya,
        "3": modul_peringatan_stok,
    }

    while True:
        tampilkan_menu()
        pilihan = input("  Pilih menu [0-3] : ").strip()

        if pilihan == "0":
            print()
            judul_box("  Terima kasih! Program selesai.  ")
            print()
            break
        elif pilihan in MENU:
            print()
            MENU[pilihan]()
        else:
            print("\n  [!] Pilihan tidak valid. Masukkan angka 0, 1, 2, atau 3.\n")

if __name__ == "__main__":
    main()
