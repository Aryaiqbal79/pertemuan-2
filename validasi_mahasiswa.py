# ================================================================
#   VALIDASI DATA MAHASISWA
#   Mencakup: NIM, IPK, SKS, Semester
# ================================================================
#
#   Format NIM  : 10 digit angka
#                 4 digit pertama = tahun masuk (2000–2037)
#                 Contoh valid   : 2024050001
#                 Contoh invalid : 199905001 (9 digit), ABCD050001
#
# ================================================================

# ────────────────────────────────────────────────────────────────
#  FUNGSI-FUNGSI VALIDASI
# ────────────────────────────────────────────────────────────────

def validasi_nim(nim: str) -> list[str]:
    """
    Memvalidasi NIM mahasiswa.
    Aturan:
      - Harus tepat 10 karakter
      - Seluruh karakter harus digit (0-9)
      - 4 digit pertama merupakan tahun masuk: 2000–2037

    Returns:
        List string berisi pesan error. Kosong berarti valid.
    """
    errors = []

    # 1. Pastikan sudah diisi
    if not nim or nim.strip() == "":
        errors.append("NIM tidak boleh kosong.")
        return errors  # berhenti, tidak perlu cek lanjut

    nim = nim.strip()

    # 2. Hanya boleh digit
    if not nim.isdigit():
        errors.append(
            f"NIM hanya boleh berisi angka (ditemukan karakter bukan digit: "
            f"'{[c for c in nim if not c.isdigit()][:3]}')."
        )

    # 3. Harus tepat 10 digit
    if len(nim) != 10:
        errors.append(
            f"NIM harus tepat 10 digit (sekarang {len(nim)} digit)."
        )

    # 4. Cek tahun masuk (hanya jika sudah 10 digit dan semua angka)
    if nim.isdigit() and len(nim) == 10:
        tahun_masuk = int(nim[:4])
        if not (2000 <= tahun_masuk <= 2037):
            errors.append(
                f"Tahun masuk pada NIM ({tahun_masuk}) tidak valid. "
                f"Harus antara 2000–2037."
            )

    return errors


def validasi_ipk(ipk_input) -> list[str]:
    """
    Memvalidasi IPK mahasiswa.
    Aturan:
      - Harus berupa angka (int atau float)
      - Rentang: 0.0 – 4.0

    Returns:
        List string berisi pesan error. Kosong berarti valid.
    """
    errors = []

    try:
        ipk = float(ipk_input)
    except (ValueError, TypeError):
        errors.append(
            f"IPK harus berupa angka desimal (diterima: '{ipk_input}')."
        )
        return errors

    if ipk < 0.0 or ipk > 4.0:
        errors.append(
            f"IPK harus antara 0.00 – 4.00 (diterima: {ipk:.2f})."
        )

    return errors


def validasi_sks(sks_input) -> list[str]:
    """
    Memvalidasi jumlah SKS yang diambil per semester.
    Aturan:
      - Harus bilangan bulat
      - Rentang: 0 – 24

    Returns:
        List string berisi pesan error. Kosong berarti valid.
    """
    errors = []

    # Cek apakah bisa dikonversi ke int
    try:
        sks_f = float(sks_input)          # coba float dulu
        if sks_f != int(sks_f):           # pastikan tidak ada desimal
            raise ValueError
        sks = int(sks_f)
    except (ValueError, TypeError):
        errors.append(
            f"SKS harus bilangan bulat (diterima: '{sks_input}')."
        )
        return errors

    if sks < 0 or sks > 24:
        errors.append(
            f"SKS harus antara 0 – 24 (diterima: {sks})."
        )

    return errors


def validasi_semester(semester_input) -> list[str]:
    """
    Memvalidasi semester aktif mahasiswa.
    Aturan:
      - Harus bilangan bulat
      - Rentang: 1 – 14

    Returns:
        List string berisi pesan error. Kosong berarti valid.
    """
    errors = []

    try:
        sem_f = float(semester_input)
        if sem_f != int(sem_f):
            raise ValueError
        sem = int(sem_f)
    except (ValueError, TypeError):
        errors.append(
            f"Semester harus bilangan bulat (diterima: '{semester_input}')."
        )
        return errors

    if sem < 1 or sem > 14:
        errors.append(
            f"Semester harus antara 1 – 14 (diterima: {sem})."
        )

    return errors


def validasi_mahasiswa(nim: str, ipk, sks, semester) -> dict:
    """
    Menjalankan semua validasi untuk satu data mahasiswa.

    Args:
        nim      : NIM sebagai string
        ipk      : Nilai IPK (bisa str/float)
        sks      : Jumlah SKS (bisa str/int)
        semester : Semester aktif (bisa str/int)

    Returns:
        dict dengan key:
          'valid'    -> bool, True jika semua field valid
          'errors'   -> dict field -> list error per field
          'semua_error' -> list semua pesan error (flat)
    """
    hasil = {
        "NIM"      : validasi_nim(nim),
        "IPK"      : validasi_ipk(ipk),
        "SKS"      : validasi_sks(sks),
        "Semester" : validasi_semester(semester),
    }
    semua = [f"[{field}] {pesan}"
             for field, errors in hasil.items()
             for pesan in errors]

    return {
        "valid"      : len(semua) == 0,
        "errors"     : hasil,
        "semua_error": semua,
    }


# ────────────────────────────────────────────────────────────────
#  UTILITAS TAMPILAN
# ────────────────────────────────────────────────────────────────

LEBAR = 60

def garis(kar="=", lebar=LEBAR):
    print(kar * lebar)

def tampilkan_hasil_validasi(nama: str, hasil: dict):
    """Mencetak laporan hasil validasi satu mahasiswa."""
    garis()
    status = "[VALID]" if hasil["valid"] else "[TIDAK VALID]"
    print(f"  Mahasiswa : {nama}")
    print(f"  Status    : {status}")
    garis("-")

    fields = ["NIM", "IPK", "SKS", "Semester"]
    for field in fields:
        errors = hasil["errors"][field]
        if errors:
            print(f"  {field:<10} : [X] GAGAL")
            for e in errors:
                print(f"              -> {e}")
        else:
            print(f"  {field:<10} : [OK] Valid")

    if hasil["semua_error"]:
        garis("-")
        print(f"  Total error: {len(hasil['semua_error'])} ditemukan")

    garis()


# ────────────────────────────────────────────────────────────────
#  INPUT INTERAKTIF
# ────────────────────────────────────────────────────────────────

def input_raw(label: str) -> str:
    """Input bebas tanpa validasi (validasi dilakukan terpisah)."""
    return input(label).strip()


def jalankan_program():
    garis()
    print("       PROGRAM VALIDASI DATA MAHASISWA".center(LEBAR))
    garis()
    print("  Catatan: Input diterima apa adanya untuk divalidasi.")
    print("  NIM format: 10 digit, 4 digit awal = tahun (2000-2037)")
    garis()

    while True:
        try:
            n = int(input("\n  Jumlah mahasiswa yang akan divalidasi (1-10): "))
            if 1 <= n <= 10:
                break
            print("  [!] Masukkan angka antara 1 dan 10.")
        except ValueError:
            print("  [!] Masukkan bilangan bulat.")

    print()
    data_mahasiswa = []

    for i in range(1, n + 1):
        garis("-")
        print(f"  Input Data Mahasiswa ke-{i}")
        garis("-")
        nama     = input_raw("  Nama     : ") or f"Mahasiswa {i}"
        nim      = input_raw("  NIM      : ")
        ipk      = input_raw("  IPK      : ")
        sks      = input_raw("  SKS      : ")
        semester = input_raw("  Semester : ")
        data_mahasiswa.append((nama, nim, ipk, sks, semester))

    # ── Laporan Hasil Validasi ───────────────────────────────
    print()
    garis()
    print("         HASIL VALIDASI DATA MAHASISWA".center(LEBAR))
    garis()

    total_valid    = 0
    total_invalid  = 0

    for nama, nim, ipk, sks, semester in data_mahasiswa:
        hasil = validasi_mahasiswa(nim, ipk, sks, semester)
        tampilkan_hasil_validasi(nama, hasil)
        if hasil["valid"]:
            total_valid += 1
        else:
            total_invalid += 1

    # ── Ringkasan Akhir ──────────────────────────────────────
    print()
    garis()
    print("  RINGKASAN VALIDASI".center(LEBAR))
    garis("-")
    print(f"  Total mahasiswa diperiksa : {n}")
    print(f"  [OK]  Data valid          : {total_valid}")
    print(f"  [X]   Data tidak valid    : {total_invalid}")
    garis()

    if total_invalid == 0:
        print("  Semua data mahasiswa lolos validasi.")
    else:
        print(f"  {total_invalid} data perlu diperbaiki sebelum disimpan.")
    garis()
    print()


# ────────────────────────────────────────────────────────────────
#  TITIK MASUK PROGRAM
# ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    jalankan_program()
