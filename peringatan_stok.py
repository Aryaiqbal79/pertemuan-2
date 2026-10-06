# ============================================================
#   SISTEM PERINGATAN STOK INVENTARIS
#   Status: Aman | Peringatan | Rendah | Habis
# ============================================================

# ── Data Inventaris ──────────────────────────────────────────
inventaris = [
    {"kode": "ITM-001", "nama": "Laptop Asus VivoBook",    "kategori": "Elektronik",   "stok": 42,  "stok_min": 10, "harga": 8_500_000},
    {"kode": "ITM-002", "nama": "Mouse Wireless Logitech", "kategori": "Aksesori",     "stok": 18,  "stok_min": 15, "harga":   250_000},
    {"kode": "ITM-003", "nama": "Keyboard Mechanical",     "kategori": "Aksesori",     "stok": 7,   "stok_min": 10, "harga":   750_000},
    {"kode": "ITM-004", "nama": "Monitor LED 24\"",        "kategori": "Elektronik",   "stok": 0,   "stok_min": 5,  "harga": 2_200_000},
    {"kode": "ITM-005", "nama": "Kertas HVS A4 (rim)",     "kategori": "ATK",          "stok": 3,   "stok_min": 20, "harga":    55_000},
    {"kode": "ITM-006", "nama": "Tinta Printer Canon",     "kategori": "ATK",          "stok": 12,  "stok_min": 15, "harga":    85_000},
    {"kode": "ITM-007", "nama": "Headset Gaming Rexus",    "kategori": "Aksesori",     "stok": 55,  "stok_min": 8,  "harga":   450_000},
    {"kode": "ITM-008", "nama": "Flash Disk 64GB",         "kategori": "Penyimpanan",  "stok": 0,   "stok_min": 10, "harga":    95_000},
    {"kode": "ITM-009", "nama": "SSD 256GB Samsung",       "kategori": "Penyimpanan",  "stok": 9,   "stok_min": 5,  "harga":   550_000},
    {"kode": "ITM-010", "nama": "Webcam HD Logitech",      "kategori": "Elektronik",   "stok": 30,  "stok_min": 5,  "harga":   480_000},
]

# ── Konfigurasi Status ───────────────────────────────────────
# Status ditentukan berdasarkan rasio: stok / stok_min
# Habis    : stok == 0
# Rendah   : 0 < stok < stok_min
# Peringatan: stok_min <= stok < stok_min * 2
# Aman     : stok >= stok_min * 2

PRIORITAS = {
    "HABIS"      : 1,
    "RENDAH"     : 2,
    "PERINGATAN" : 3,
    "AMAN"       : 4,
}

LABEL = {
    "HABIS"      : "[HABIS]",
    "RENDAH"     : "[RENDAH]",
    "PERINGATAN" : "[PERINGATAN]",
    "AMAN"       : "[AMAN]",
}

def tentukan_status(stok, stok_min):
    if stok == 0:
        return "HABIS"
    elif stok < stok_min:
        return "RENDAH"
    elif stok < stok_min * 2:
        return "PERINGATAN"
    else:
        return "AMAN"

def format_rupiah(nilai):
    return f"Rp {nilai:>15,.0f}"

def garis(karakter="=", lebar=80):
    print(karakter * lebar)

# ── Evaluasi & Tambah Data ───────────────────────────────────
for item in inventaris:
    item["status"]    = tentukan_status(item["stok"], item["stok_min"])
    item["prioritas"] = PRIORITAS[item["status"]]
    item["nilai"]     = item["stok"] * item["harga"]

# Urutkan berdasarkan prioritas (1 = paling mendesak)
inventaris_sorted = sorted(inventaris, key=lambda x: (x["prioritas"], x["nama"]))

# ── Header ───────────────────────────────────────────────────
garis()
print("              SISTEM PERINGATAN STOK INVENTARIS")
print("                 Laporan Per: 2026-10-06 | Rev. 1")
garis()

# ── Tabel Laporan Lengkap ────────────────────────────────────
print(f"\n{'LAPORAN INVENTARIS (Diurutkan berdasarkan Prioritas)'}")
garis("-", 80)
header = f"{'No':<4} {'Kode':<9} {'Nama Item':<26} {'Kategori':<13} {'Stok':>5} {'Min':>4} {'Status':<14} {'Nilai Stok':>17}"
print(header)
garis("-", 80)

for no, item in enumerate(inventaris_sorted, 1):
    label  = LABEL[item["status"]]
    nilai  = f"Rp {item['nilai']:>13,.0f}"
    stok_s = str(item["stok"]) if item["stok"] > 0 else "0 (!)"
    print(
        f"{no:<4} "
        f"{item['kode']:<9} "
        f"{item['nama'][:25]:<26} "
        f"{item['kategori']:<13} "
        f"{stok_s:>5} "
        f"{item['stok_min']:>4} "
        f"{label:<14} "
        f"{nilai}"
    )

garis("-", 80)

# ── Total Nilai Inventaris ───────────────────────────────────
total_nilai = sum(item["nilai"] for item in inventaris)
print(f"{'TOTAL NILAI INVENTARIS':>67} {format_rupiah(total_nilai)}")
garis("=", 80)

# ── Ringkasan Statistik ──────────────────────────────────────
print("\n" + " RINGKASAN STATISTIK ".center(80, "="))

# Hitung per status
per_status = {"HABIS": [], "RENDAH": [], "PERINGATAN": [], "AMAN": []}
for item in inventaris:
    per_status[item["status"]].append(item)

print(f"\n  {'Status':<14} {'Jumlah Item':>12}   Item")
garis("-", 80)
for status in ["HABIS", "RENDAH", "PERINGATAN", "AMAN"]:
    items = per_status[status]
    nama_items = ", ".join(i["nama"][:20] for i in items) if items else "-"
    print(f"  {LABEL[status]:<14} {len(items):>12}   {nama_items}")

garis("-", 80)
print(f"  {'Total Item':<14} {len(inventaris):>12}")

# Statistik stok
stok_list  = [i["stok"] for i in inventaris]
nilai_list = [i["nilai"] for i in inventaris]

print(f"\n  Stok tertinggi : {max(stok_list)} unit  ({next(i['nama'] for i in inventaris if i['stok'] == max(stok_list))})")
print(f"  Stok terendah  : {min(stok_list)} unit  ({next(i['nama'] for i in inventaris if i['stok'] == min(stok_list))})")
print(f"  Rata-rata stok : {sum(stok_list)/len(stok_list):.1f} unit")

print(f"\n  Item paling bernilai : {max(inventaris, key=lambda x: x['nilai'])['nama']}")
print(f"                         {format_rupiah(max(nilai_list))}")
print(f"  Total nilai inventaris : {format_rupiah(total_nilai)}")

# ── Daftar Tindakan Darurat ──────────────────────────────────
darurat = [i for i in inventaris if i["status"] in ("HABIS", "RENDAH")]
if darurat:
    print("\n" + " TINDAKAN SEGERA DIPERLUKAN ".center(80, "!"))
    print()
    for item in sorted(darurat, key=lambda x: x["prioritas"]):
        kekurangan = max(0, item["stok_min"] - item["stok"])
        print(f"  >> {item['kode']} | {item['nama']:<26} | "
              f"Stok: {item['stok']:>3} | Perlu restock: {kekurangan} unit")
    print()
    garis("!", 80)
else:
    print("\n  [OK] Semua item dalam kondisi aman.")
    garis()

print()
