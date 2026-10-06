# ============================================
#   Program Status Mahasiswa
#   Menentukan status berdasarkan IPK & SKS
# ============================================

print("=" * 50)
print("       SISTEM INFORMASI STATUS MAHASISWA")
print("=" * 50)

mahasiswa = []

# Input data 5 mahasiswa menggunakan loop
for i in range(1, 6):
    print(f"\n--- Input Data Mahasiswa ke-{i} ---")

    nim  = input("  NIM   : ")
    nama = input("  Nama  : ")

    while True:
        try:
            ipk = float(input("  IPK   : "))
            if 0.0 <= ipk <= 4.0:
                break
            else:
                print("  [!] IPK harus antara 0.0 - 4.0. Coba lagi.")
        except ValueError:
            print("  [!] IPK harus berupa angka. Coba lagi.")

    while True:
        try:
            sks = int(input("  SKS   : "))
            if sks >= 0:
                break
            else:
                print("  [!] SKS tidak boleh negatif. Coba lagi.")
        except ValueError:
            print("  [!] SKS harus berupa bilangan bulat. Coba lagi.")

    mahasiswa.append({
        "nim" : nim,
        "nama": nama,
        "ipk" : ipk,
        "sks" : sks
    })

# Fungsi penentu status
def tentukan_status(ipk, sks):
    if ipk < 1.5:
        return "Tidak Aktif"
    elif 1.5 <= ipk < 2.0:
        return "Peringatan"
    else:  # ipk >= 2.0
        if sks >= 18:
            return "Aktif"
        else:
            return "Peringatan"  # IPK cukup tapi SKS kurang

# Tampilkan laporan
print("\n")
print("=" * 70)
print("                       LAPORAN STATUS MAHASISWA")
print("=" * 70)
print(f"{'No':<4} {'NIM':<12} {'Nama':<20} {'IPK':<8} {'SKS':<8} {'Status'}")
print("-" * 70)

for idx, mhs in enumerate(mahasiswa, start=1):
    status = tentukan_status(mhs["ipk"], mhs["sks"])

    # Tambahkan label agar lebih informatif
    simbol = {"Aktif": "[OK]", "Peringatan": "[!] ", "Tidak Aktif": "[X] "}
    ket    = f"{simbol.get(status, '')} {status}"

    print(f"{idx:<4} {mhs['nim']:<12} {mhs['nama']:<20} {mhs['ipk']:<8.2f} {mhs['sks']:<8} {ket}")

print("=" * 70)

# Ringkasan
aktif       = sum(1 for m in mahasiswa if tentukan_status(m["ipk"], m["sks"]) == "Aktif")
peringatan  = sum(1 for m in mahasiswa if tentukan_status(m["ipk"], m["sks"]) == "Peringatan")
tidak_aktif = sum(1 for m in mahasiswa if tentukan_status(m["ipk"], m["sks"]) == "Tidak Aktif")

print(f"\n  Ringkasan  :")
print(f"  [OK] Aktif       : {aktif} mahasiswa")
print(f"  [!]  Peringatan  : {peringatan} mahasiswa")
print(f"  [X]  Tidak Aktif : {tidak_aktif} mahasiswa")
print("\n" + "=" * 70)
