# ================================================================
#   RINGKASAN ALGORITMA — TIGA STUDI KASUS
#   (a) Status Mahasiswa   (b) Diskon Biaya Kuliah
#   (c) Peringatan Stok Inventaris
# ================================================================

import datetime

# ════════════════════════════════════════════════════════════════
#  DATASET BAWAAN (SAMPLE DATA)
# ════════════════════════════════════════════════════════════════

DATA_MAHASISWA = [
    {"nama": "Budi Santoso",    "ipk": 3.50, "sks": 20},
    {"nama": "Siti Rahayu",     "ipk": 1.80, "sks": 19},
    {"nama": "Ahmad Rizki",     "ipk": 1.20, "sks": 15},
    {"nama": "Dewi Lestari",    "ipk": 2.10, "sks": 16},
    {"nama": "Eko Prasetyo",    "ipk": 0.90, "sks": 10},
    {"nama": "Fitriani",        "ipk": 3.80, "sks": 22},
    {"nama": "Galuh Permata",   "ipk": 2.50, "sks": 18},
    {"nama": "Hendra Wijaya",   "ipk": 1.60, "sks": 20},
    {"nama": "Indira Sari",     "ipk": 2.00, "sks": 17},
    {"nama": "Joko Susilo",     "ipk": 3.20, "sks": 21},
]

DATA_DISKON = [
    {"nama": "Mahasiswa A", "spp": 5_000_000, "anak_karyawan": True,  "ipk": 3.90, "tepat_waktu": True},
    {"nama": "Mahasiswa B", "spp": 4_500_000, "anak_karyawan": False, "ipk": 3.60, "tepat_waktu": False},
    {"nama": "Mahasiswa C", "spp": 4_000_000, "anak_karyawan": False, "ipk": 3.10, "tepat_waktu": True},
    {"nama": "Mahasiswa D", "spp": 5_500_000, "anak_karyawan": True,  "ipk": 2.80, "tepat_waktu": False},
    {"nama": "Mahasiswa E", "spp": 3_500_000, "anak_karyawan": False, "ipk": 2.50, "tepat_waktu": True},
    {"nama": "Mahasiswa F", "spp": 6_000_000, "anak_karyawan": False, "ipk": 3.85, "tepat_waktu": True},
    {"nama": "Mahasiswa G", "spp": 4_200_000, "anak_karyawan": True,  "ipk": 3.50, "tepat_waktu": False},
    {"nama": "Mahasiswa H", "spp": 4_800_000, "anak_karyawan": False, "ipk": 2.90, "tepat_waktu": True},
]

DATA_INVENTARIS = [
    {"kode": "ITM-001", "nama": "Laptop Asus VivoBook",    "kategori": "Elektronik",  "stok": 42, "stok_min": 10, "harga": 8_500_000},
    {"kode": "ITM-002", "nama": "Mouse Wireless Logitech", "kategori": "Aksesori",    "stok": 18, "stok_min": 15, "harga":   250_000},
    {"kode": "ITM-003", "nama": "Keyboard Mechanical",     "kategori": "Aksesori",    "stok":  7, "stok_min": 10, "harga":   750_000},
    {"kode": "ITM-004", "nama": "Monitor LED 24\"",        "kategori": "Elektronik",  "stok":  0, "stok_min":  5, "harga": 2_200_000},
    {"kode": "ITM-005", "nama": "Kertas HVS A4 (rim)",     "kategori": "ATK",         "stok":  3, "stok_min": 20, "harga":    55_000},
    {"kode": "ITM-006", "nama": "Tinta Printer Canon",     "kategori": "ATK",         "stok": 12, "stok_min": 15, "harga":    85_000},
    {"kode": "ITM-007", "nama": "Headset Gaming Rexus",    "kategori": "Aksesori",    "stok": 55, "stok_min":  8, "harga":   450_000},
    {"kode": "ITM-008", "nama": "Flash Disk 64GB",         "kategori": "Penyimpanan", "stok":  0, "stok_min": 10, "harga":    95_000},
    {"kode": "ITM-009", "nama": "SSD 256GB Samsung",       "kategori": "Penyimpanan", "stok":  9, "stok_min":  5, "harga":   550_000},
    {"kode": "ITM-010", "nama": "Webcam HD Logitech",      "kategori": "Elektronik",  "stok": 30, "stok_min":  5, "harga":   480_000},
]


# ════════════════════════════════════════════════════════════════
#  LOGIKA DOMAIN (sama persis dengan program sebelumnya)
# ════════════════════════════════════════════════════════════════

def status_mhs(ipk, sks):
    if ipk < 1.5:           return "Tidak Aktif"
    if ipk < 2.0:           return "Peringatan"
    return "Aktif" if sks >= 18 else "Peringatan"

def hitung_diskon_persen(anak_karyawan, ipk, tepat_waktu):
    dk = 25 if anak_karyawan else 0
    di = 20 if ipk >= 3.8 else (15 if ipk >= 3.5 else (10 if ipk >= 3.0 else 0))
    dt = 5  if tepat_waktu   else 0
    return min(max(dk, di) + dt, 100)

def status_stok(stok, stok_min):
    if stok == 0:            return "HABIS"
    if stok < stok_min:      return "RENDAH"
    if stok < stok_min * 2:  return "PERINGATAN"
    return "AMAN"


# ════════════════════════════════════════════════════════════════
#  (a) ALGORITMA RINGKASAN MAHASISWA
# ════════════════════════════════════════════════════════════════

def ringkasan_mahasiswa(data: list) -> dict:
    """
    Menghitung distribusi status mahasiswa dan statistik IPK/SKS.
    Returns dict dengan semua metrik.
    """
    total = len(data)
    hasil = []
    for m in data:
        st = status_mhs(m["ipk"], m["sks"])
        hasil.append({**m, "status": st})

    # Hitung per kategori
    aktif       = [m for m in hasil if m["status"] == "Aktif"]
    peringatan  = [m for m in hasil if m["status"] == "Peringatan"]
    tidak_aktif = [m for m in hasil if m["status"] == "Tidak Aktif"]

    # Statistik IPK
    ipk_list = [m["ipk"] for m in data]
    sks_list = [m["sks"] for m in data]

    return {
        "total"            : total,
        "aktif"            : len(aktif),
        "peringatan"       : len(peringatan),
        "tidak_aktif"      : len(tidak_aktif),
        "persen_aktif"     : len(aktif)       / total * 100,
        "persen_peringatan": len(peringatan)  / total * 100,
        "persen_tdk_aktif" : len(tidak_aktif) / total * 100,
        "ipk_rata"         : sum(ipk_list) / total,
        "ipk_max"          : max(ipk_list),
        "ipk_min"          : min(ipk_list),
        "sks_rata"         : sum(sks_list) / total,
        "detail"           : hasil,
    }


# ════════════════════════════════════════════════════════════════
#  (b) ALGORITMA RINGKASAN DISKON
# ════════════════════════════════════════════════════════════════

def ringkasan_diskon(data: list) -> dict:
    """
    Menghitung statistik diskon yang diberikan kepada setiap mahasiswa.
    Returns dict dengan semua metrik.
    """
    total = len(data)
    hasil = []
    for d in data:
        persen  = hitung_diskon_persen(d["anak_karyawan"], d["ipk"], d["tepat_waktu"])
        potongan = d["spp"] * persen / 100
        hasil.append({
            **d,
            "diskon_persen": persen,
            "potongan"     : potongan,
            "biaya_final"  : d["spp"] - potongan,
        })

    diskon_list   = [h["diskon_persen"] for h in hasil]
    potongan_list = [h["potongan"]      for h in hasil]
    spp_list      = [h["spp"]           for h in hasil]

    # Distribusi bracket diskon
    nol    = sum(1 for d in diskon_list if d == 0)
    rendah = sum(1 for d in diskon_list if 0 < d <= 15)
    tinggi = sum(1 for d in diskon_list if d > 15)

    return {
        "total"              : total,
        "diskon_rata"        : sum(diskon_list) / total,
        "diskon_max"         : max(diskon_list),
        "diskon_min"         : min(diskon_list),
        "total_potongan"     : sum(potongan_list),
        "total_spp_asli"     : sum(spp_list),
        "total_spp_final"    : sum(h["biaya_final"] for h in hasil),
        "persen_hemat"       : sum(potongan_list) / sum(spp_list) * 100,
        "bracket_nol"        : nol,
        "bracket_rendah"     : rendah,   # 1–15%
        "bracket_tinggi"     : tinggi,   # >15%
        "persen_dapat_diskon": (total - nol) / total * 100,
        "detail"             : hasil,
    }


# ════════════════════════════════════════════════════════════════
#  (c) ALGORITMA RINGKASAN STOK
# ════════════════════════════════════════════════════════════════

def ringkasan_stok(data: list) -> dict:
    """
    Menghitung statistik status stok dan kebutuhan restock.
    Returns dict dengan semua metrik.
    """
    total  = len(data)
    hasil  = []
    for item in data:
        st        = status_stok(item["stok"], item["stok_min"])
        restock   = max(0, item["stok_min"] - item["stok"])
        nilai     = item["stok"] * item["harga"]
        perlu     = st in ("HABIS", "RENDAH")
        hasil.append({**item, "status": st, "restock": restock,
                      "nilai": nilai, "perlu_restock": perlu})

    aman        = [h for h in hasil if h["status"] == "AMAN"]
    peringatan  = [h for h in hasil if h["status"] == "PERINGATAN"]
    rendah      = [h for h in hasil if h["status"] == "RENDAH"]
    habis       = [h for h in hasil if h["status"] == "HABIS"]
    restock_items = [h for h in hasil if h["perlu_restock"]]

    stok_list   = [h["stok"]  for h in hasil]
    nilai_list  = [h["nilai"] for h in hasil]

    return {
        "total"              : total,
        "jml_aman"           : len(aman),
        "jml_peringatan"     : len(peringatan),
        "jml_rendah"         : len(rendah),
        "jml_habis"          : len(habis),
        "jml_restock"        : len(restock_items),
        "persen_aman"        : len(aman)          / total * 100,
        "persen_peringatan"  : len(peringatan)    / total * 100,
        "persen_rendah"      : len(rendah)        / total * 100,
        "persen_habis"       : len(habis)         / total * 100,
        "persen_restock"     : len(restock_items) / total * 100,
        "total_restock_unit" : sum(h["restock"]   for h in restock_items),
        "total_nilai"        : sum(nilai_list),
        "stok_rata"          : sum(stok_list) / total,
        "stok_max"           : max(stok_list),
        "stok_min"           : min(stok_list),
        "detail"             : hasil,
    }


# ════════════════════════════════════════════════════════════════
#  TAMPILAN TABEL
# ════════════════════════════════════════════════════════════════

LEBAR = 70

def garis(kar="=", lebar=LEBAR): print(kar * lebar)

def baris_tabel(kolom1, kolom2, kolom3, w1=30, w2=18, w3=18):
    print(f"  {kolom1:<{w1}} {kolom2:>{w2}} {kolom3:>{w3}}")

def header_tabel(judul1, judul2, judul3):
    garis("-")
    baris_tabel(judul1, judul2, judul3)
    garis("-")

def tampilkan_tabel_mahasiswa(r: dict):
    garis()
    print("  (a) RINGKASAN STATUS MAHASISWA".center(LEBAR))
    garis()

    baris_tabel("Metrik", "Jumlah", "Persentase")
    header_tabel("Status", "Mahasiswa", "(%)")
    baris_tabel("Aktif",        f"{r['aktif']}",       f"{r['persen_aktif']:>7.1f}%")
    baris_tabel("Peringatan",   f"{r['peringatan']}",  f"{r['persen_peringatan']:>7.1f}%")
    baris_tabel("Tidak Aktif",  f"{r['tidak_aktif']}", f"{r['persen_tdk_aktif']:>7.1f}%")
    garis("-")
    baris_tabel("TOTAL", f"{r['total']}", "100.0%")
    garis()

    # Sub-tabel statistik IPK & SKS
    print(f"  {'Statistik':<30} {'IPK':>18} {'SKS':>18}")
    garis("-")
    print(f"  {'Rata-rata':<30} {r['ipk_rata']:>18.2f} {r['sks_rata']:>17.1f}")
    print(f"  {'Tertinggi':<30} {r['ipk_max']:>18.2f} {'-':>18}")
    print(f"  {'Terendah':<30}  {r['ipk_min']:>17.2f} {'-':>18}")
    garis()

    # Tabel detail
    print(f"\n  Detail Per Mahasiswa:")
    garis("-")
    print(f"  {'No':<4} {'Nama':<20} {'IPK':>6} {'SKS':>5}  {'Status'}")
    garis("-")
    for no, m in enumerate(r["detail"], 1):
        lbl = {"Aktif":"[OK]","Peringatan":"[!] ","Tidak Aktif":"[X] "}.get(m["status"],"")
        print(f"  {no:<4} {m['nama'][:19]:<20} {m['ipk']:>6.2f} {m['sks']:>5}  {lbl} {m['status']}")
    garis()


def tampilkan_tabel_diskon(r: dict):
    garis()
    print("  (b) RINGKASAN DISKON BIAYA KULIAH".center(LEBAR))
    garis()

    print(f"  {'Metrik Diskon':<38} {'Nilai':>28}")
    garis("-")
    print(f"  {'Total mahasiswa':<38} {r['total']:>28}")
    print(f"  {'Rata-rata diskon':<38} {r['diskon_rata']:>27.1f}%")
    print(f"  {'Diskon tertinggi diberikan':<38} {r['diskon_max']:>27}%")
    print(f"  {'Diskon terendah diberikan':<38} {r['diskon_min']:>27}%")
    print(f"  {'Mahasiswa mendapat diskon':<38} {r['persen_dapat_diskon']:>26.1f}%")
    garis("-")
    print(f"  {'Total SPP sebelum diskon':<38} Rp {r['total_spp_asli']:>22,.0f}")
    print(f"  {'Total potongan diskon':<38} Rp {r['total_potongan']:>22,.0f}")
    print(f"  {'Total SPP setelah diskon':<38} Rp {r['total_spp_final']:>22,.0f}")
    print(f"  {'Efisiensi biaya keseluruhan':<38} {r['persen_hemat']:>27.1f}%")
    garis()

    # Distribusi bracket
    print(f"  {'Distribusi Bracket Diskon':<30} {'Jumlah':>18} {'Persentase':>18}")
    garis("-")
    baris_tabel("Tanpa diskon (0%)",    f"{r['bracket_nol']}",    f"{r['bracket_nol']/r['total']*100:.1f}%")
    baris_tabel("Rendah (1–15%)",       f"{r['bracket_rendah']}", f"{r['bracket_rendah']/r['total']*100:.1f}%")
    baris_tabel("Tinggi (>15%)",        f"{r['bracket_tinggi']}", f"{r['bracket_tinggi']/r['total']*100:.1f}%")
    garis("-")
    baris_tabel("TOTAL", f"{r['total']}", "100.0%")
    garis()

    # Detail per mahasiswa
    print(f"\n  Detail Per Mahasiswa:")
    garis("-")
    print(f"  {'No':<4} {'Nama':<14} {'SPP Awal':>14} {'Diskon':>7} {'Potongan':>14} {'Final':>14}")
    garis("-")
    for no, d in enumerate(r["detail"], 1):
        print(f"  {no:<4} {d['nama'][:13]:<14} "
              f"Rp{d['spp']:>11,.0f} "
              f"{d['diskon_persen']:>6}% "
              f"Rp{d['potongan']:>11,.0f} "
              f"Rp{d['biaya_final']:>11,.0f}")
    garis()


def tampilkan_tabel_stok(r: dict):
    garis()
    print("  (c) RINGKASAN PERINGATAN STOK INVENTARIS".center(LEBAR))
    garis()

    print(f"  {'Status Stok':<30} {'Item':>18} {'Persentase':>18}")
    header_tabel("Status", "Jumlah Item", "(%)")
    baris_tabel("[AMAN]",        f"{r['jml_aman']}",        f"{r['persen_aman']:>7.1f}%")
    baris_tabel("[PERINGATAN]",  f"{r['jml_peringatan']}",  f"{r['persen_peringatan']:>7.1f}%")
    baris_tabel("[RENDAH]",      f"{r['jml_rendah']}",      f"{r['persen_rendah']:>7.1f}%")
    baris_tabel("[HABIS]",       f"{r['jml_habis']}",       f"{r['persen_habis']:>7.1f}%")
    garis("-")
    baris_tabel("Perlu Restock (Rendah+Habis)", f"{r['jml_restock']}", f"{r['persen_restock']:>7.1f}%")
    baris_tabel("TOTAL",         f"{r['total']}",           "100.0%")
    garis()

    print(f"  {'Statistik Stok':<38} {'Nilai':>28}")
    garis("-")
    print(f"  {'Total item perlu restock':<38} {r['jml_restock']:>28} item")
    print(f"  {'Total unit yang harus dipesan':<38} {r['total_restock_unit']:>28} unit")
    print(f"  {'Rata-rata stok per item':<38} {r['stok_rata']:>27.1f} unit")
    print(f"  {'Stok tertinggi':<38} {r['stok_max']:>28} unit")
    print(f"  {'Stok terendah':<38} {r['stok_min']:>28} unit")
    print(f"  {'Total nilai inventaris':<38} Rp {r['total_nilai']:>22,.0f}")
    garis()

    # Detail per item
    print(f"\n  Detail Per Item:")
    garis("-")
    print(f"  {'No':<4} {'Nama Item':<24} {'Stok':>5} {'Min':>4}  {'Status':<14} {'Nilai':>12}")
    garis("-")
    for no, item in enumerate(
        sorted(r["detail"], key=lambda x: ({"HABIS":1,"RENDAH":2,"PERINGATAN":3,"AMAN":4}[x["status"]], x["nama"])), 1
    ):
        lbl   = {"HABIS":"[HABIS]","RENDAH":"[RENDAH]","PERINGATAN":"[PERINGT]","AMAN":"[AMAN]"}.get(item["status"])
        stoks = "0(!)" if item["stok"] == 0 else str(item["stok"])
        print(f"  {no:<4} {item['nama'][:23]:<24} {stoks:>5} {item['stok_min']:>4}  "
              f"{lbl:<14} Rp{item['nilai']:>9,.0f}")
    garis()


# ════════════════════════════════════════════════════════════════
#  TABEL KOMPARASI ANTAR STUDI KASUS
# ════════════════════════════════════════════════════════════════

def tampilkan_komparasi(rm, rd, rs):
    garis("=")
    print("  KOMPARASI RINGKASAN — KETIGA STUDI KASUS".center(LEBAR))
    garis("=")
    print(f"  {'Indikator Kinerja':<36} {'Nilai':>18} {'Satuan':>11}")
    garis("-")

    baris = [
        # Studi kasus A
        ("(a) % Mahasiswa Aktif",            f"{rm['persen_aktif']:.1f}",       "%"),
        ("(a) % Mahasiswa Peringatan",        f"{rm['persen_peringatan']:.1f}",  "%"),
        ("(a) % Mahasiswa Tidak Aktif",       f"{rm['persen_tdk_aktif']:.1f}",   "%"),
        ("(a) Rata-rata IPK",                 f"{rm['ipk_rata']:.2f}",           "/ 4.00"),
        ("(a) Rata-rata SKS",                 f"{rm['sks_rata']:.1f}",           "SKS"),
        # Studi kasus B
        ("(b) Rata-rata Diskon",              f"{rd['diskon_rata']:.1f}",        "%"),
        ("(b) % Mahasiswa Dapat Diskon",      f"{rd['persen_dapat_diskon']:.1f}","%"),
        ("(b) Total Potongan Diskon",         f"Rp {rd['total_potongan']:,.0f}", ""),
        ("(b) Efisiensi Biaya Keseluruhan",   f"{rd['persen_hemat']:.1f}",       "%"),
        # Studi kasus C
        ("(c) % Item Aman",                   f"{rs['persen_aman']:.1f}",        "%"),
        ("(c) % Item Perlu Restock",          f"{rs['persen_restock']:.1f}",     "%"),
        ("(c) Total Unit Harus Dipesan",      f"{rs['total_restock_unit']}",     "unit"),
        ("(c) Total Nilai Inventaris",        f"Rp {rs['total_nilai']:,.0f}",    ""),
    ]

    for label, nilai, satuan in baris:
        print(f"  {label:<36} {nilai:>18} {satuan:>11}")

    garis("=")


# ════════════════════════════════════════════════════════════════
#  PROGRAM UTAMA
# ════════════════════════════════════════════════════════════════

def main():
    sekarang = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M")

    garis("=")
    print("     PROGRAM RINGKASAN ALGORITMA — TIGA STUDI KASUS".center(LEBAR))
    print(f"     Dijalankan pada: {sekarang}".center(LEBAR))
    garis("=")
    print(f"\n  Dataset:")
    print(f"    - Mahasiswa   : {len(DATA_MAHASISWA)} orang")
    print(f"    - Transaksi   : {len(DATA_DISKON)} mahasiswa")
    print(f"    - Inventaris  : {len(DATA_INVENTARIS)} item")
    garis("-")
    input("  [ Tekan Enter untuk mulai menghitung... ]")

    # ── Hitung ─────────────────────────────────────────────────
    rm = ringkasan_mahasiswa(DATA_MAHASISWA)
    rd = ringkasan_diskon(DATA_DISKON)
    rs = ringkasan_stok(DATA_INVENTARIS)

    # ── Tampilkan tiga tabel ────────────────────────────────────
    print()
    tampilkan_tabel_mahasiswa(rm)
    input("  [ Tekan Enter untuk studi kasus berikutnya... ]")

    print()
    tampilkan_tabel_diskon(rd)
    input("  [ Tekan Enter untuk studi kasus berikutnya... ]")

    print()
    tampilkan_tabel_stok(rs)
    input("  [ Tekan Enter untuk melihat komparasi akhir... ]")

    # ── Komparasi ───────────────────────────────────────────────
    print()
    tampilkan_komparasi(rm, rd, rs)
    print()


if __name__ == "__main__":
    main()
