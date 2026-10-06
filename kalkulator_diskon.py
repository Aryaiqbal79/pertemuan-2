# ================================================
#   KALKULATOR DISKON BIAYA KULIAH
# ================================================

def garis(karakter="=", panjang=55):
    print(karakter * panjang)

def tanya_yn(pertanyaan):
    """Meminta input y/n dan mengembalikan True/False."""
    while True:
        jawaban = input(pertanyaan).strip().lower()
        if jawaban in ("y", "n"):
            return jawaban == "y"
        print("  [!] Masukkan 'y' atau 'n'.\n")

def input_float_positif(label):
    """Meminta input angka positif."""
    while True:
        try:
            nilai = float(input(label))
            if nilai > 0:
                return nilai
            print("  [!] Nilai harus lebih dari 0.\n")
        except ValueError:
            print("  [!] Masukkan angka yang valid.\n")

def input_ipk():
    """Meminta input IPK dalam rentang 0.0 - 4.0."""
    while True:
        try:
            ipk = float(input("  IPK Anda          : "))
            if 0.0 <= ipk <= 4.0:
                return ipk
            print("  [!] IPK harus antara 0.00 - 4.00.\n")
        except ValueError:
            print("  [!] Masukkan angka yang valid.\n")

# ── Banner ───────────────────────────────────────
garis()
print("       KALKULATOR DISKON BIAYA KULIAH")
garis()

# ── Input ────────────────────────────────────────
print("\n[ DATA MAHASISWA ]\n")
spp           = input_float_positif("  Biaya SPP (Rp)    : ")
anak_karyawan = tanya_yn("  Anak karyawan?    (y/n) : ")
ipk           = input_ipk()
tepat_waktu   = tanya_yn("  Bayar tepat waktu? (y/n) : ")

# ── Hitung Diskon ────────────────────────────────
diskon_karyawan = 0
diskon_ipk      = 0
diskon_tepat    = 0
keterangan      = []

# 1. Diskon anak karyawan (tidak bisa digabung dengan diskon IPK,
#    ambil yang lebih besar — jika keduanya berlaku, tetap 25%)
if anak_karyawan:
    diskon_karyawan = 25
    keterangan.append("Anak Karyawan       : 25%")

# 2. Diskon IPK (bertingkat, ambil satu tertinggi)
if ipk >= 3.8:
    diskon_ipk = 20
    keterangan.append("IPK >= 3.8          : 20%")
elif ipk >= 3.5:
    diskon_ipk = 15
    keterangan.append("IPK >= 3.5          : 15%")
elif ipk >= 3.0:
    diskon_ipk = 10
    keterangan.append("IPK >= 3.0          : 10%")
else:
    keterangan.append("IPK < 3.0           :  0%  (tidak dapat diskon IPK)")

# 3. Diskon tepat waktu (tambahan, bisa digabung)
if tepat_waktu:
    diskon_tepat = 5
    keterangan.append("Tepat Waktu (tambahan):  5%")

# Diskon utama = max antara karyawan dan IPK (tidak ditumpuk)
diskon_utama  = max(diskon_karyawan, diskon_ipk)
diskon_total  = diskon_utama + diskon_tepat

# Batasi maksimum 100%
diskon_total  = min(diskon_total, 100)

potongan      = spp * diskon_total / 100
biaya_final   = spp - potongan

# ── Tampilkan Laporan ────────────────────────────
print()
garis()
print("               RINCIAN DISKON")
garis()

if keterangan:
    for ket in keterangan:
        print(f"  {ket}")
else:
    print("  Tidak ada diskon yang berlaku.")

garis("-")

if diskon_karyawan > 0 and diskon_ipk > 0:
    print(f"  * Diskon utama diambil nilai terbesar       : {diskon_utama}%")
    garis("-")
print(f"  Total Diskon           : {diskon_total}%")
garis()
print()
print(f"  Biaya SPP Awal         : Rp {spp:>15,.2f}")
print(f"  Potongan ({diskon_total:>3}%)          : Rp {potongan:>15,.2f}")
garis("-")
print(f"  BIAYA FINAL            : Rp {biaya_final:>15,.2f}")
garis()

# ── Pesan Tambahan ───────────────────────────────
if diskon_total == 0:
    print("\n  Info: Tidak ada diskon yang berlaku untuk data ini.")
elif diskon_total >= 30:
    print(f"\n  Selamat! Anda mendapatkan diskon besar ({diskon_total}%).")
else:
    print(f"\n  Diskon {diskon_total}% berhasil diterapkan.")

print()
