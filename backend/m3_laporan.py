import csv
import os
import time

def baca_pesanan():
    lokasi = os.path.join(os.path.dirname(__file__), "..", "data", "pesanan.csv")
    with open(lokasi, "r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.reader(file)
        judul = next(pembaca)
        data = []
        for baris in pembaca:
            if baris:
                data.append(baris)
    return judul, data

def indeks_kolom(judul, nama):
    """Mencari posisi kolom; mendukung nama singkat dari README."""
    nama = nama.strip().lower()
    for i in range(len(judul)):
        kolom = judul[i].strip().lower().replace(" ", "_")
        if kolom == nama:
            return i
        if nama == "selesai" and kolom in ("t_selesai", "t_selesai_detik", "selesai_detik"):
            return i
    raise ValueError("Kolom '" + nama + "' tidak ditemukan dalam CSV: " + str(judul))


def nilai_kunci(baris, indeks, nama):
    nilai = baris[indeks].strip()
    if nama == "harga" or nama == "selesai":
        if nilai == "":
            return (1, 0)
        try:
            return (0, float(nilai))
        except ValueError:
            raise ValueError("Nilai angka tidak valid pada kolom " + nama + ": " + nilai)
    return (0, nilai)

def insertion_sort(data, indeks, nama="harga"):
    if len(data) > 20000:
        raise ValueError("Insertion sort dibatasi maksimal 20.000 baris. Gunakan merge sort.")
    a = data[:]  
    perbandingan = 0
    pemindahan = 0
    for i in range(1, len(a)):
        item = a[i]
        kunci_item = nilai_kunci(item, indeks, nama)
        j = i - 1
        while j >= 0:
            perbandingan += 1
            if nilai_kunci(a[j], indeks, nama) > kunci_item:
                a[j + 1] = a[j]
                pemindahan += 1
                j -= 1
            else:
                break
        a[j + 1] = item
        pemindahan += 1
    return a, perbandingan, pemindahan

def merge_sort(data, indeks, nama="harga"):
    a = data[:]
    n = len(a)
    bantu = [None] * n
    perbandingan = 0
    pemindahan = 0

    lebar = 1
    while lebar < n:
        kiri = 0
        while kiri < n:
            tengah = min(kiri + lebar, n)
            kanan = min(kiri + 2 * lebar, n)
            i = kiri
            j = tengah
            k = kiri
            while i < tengah and j < kanan:
                perbandingan += 1
                if nilai_kunci(a[i], indeks, nama) <= nilai_kunci(a[j], indeks, nama):
                    bantu[k] = a[i]
                    i += 1
                else:
                    bantu[k] = a[j]
                    j += 1
                k += 1
                pemindahan += 1
            while i < tengah:
                bantu[k] = a[i]
                i += 1
                k += 1
                pemindahan += 1
            while j < kanan:
                bantu[k] = a[j]
                j += 1
                k += 1
                pemindahan += 1
            kiri += 2 * lebar
        a, bantu = bantu, a
        lebar *= 2
    return a, perbandingan, pemindahan

def linear_search(data, indeks, target):
    perbandingan = 0
    for i in range(len(data)):
        perbandingan += 1
        if data[i][indeks] == target:
            return i, perbandingan
    return -1, perbandingan

def binary_search(data_terurut, indeks, target):
    """Hanya gunakan pada daftar yang SUDAH diurutkan berdasarkan oid."""
    kiri = 0
    kanan = len(data_terurut) - 1
    perbandingan = 0
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        perbandingan += 1
        oid = data_terurut[tengah][indeks]
        if oid == target:
            return tengah, perbandingan
        if oid < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1, perbandingan


def data_sama(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def cek_m3():
    """Tes fungsi tanpa membuka CSV asli."""
    contoh = [["X", "100"], ["Z", "50"], ["Y", "100"], ["A", "20"]]
    ins, _, _ = insertion_sort(contoh, 1, "harga")
    mer, _, _ = merge_sort(contoh, 1, "harga")
    assert data_sama(ins, mer)
    assert ins[0][0] == "A" and ins[1][0] == "Z"
    assert ins[2][0] == "X" and ins[3][0] == "Y"
    assert contoh[0][0] == "X" 

    indeks, banding = linear_search(contoh, 0, "Y")
    assert indeks == 2 and banding == 3
    urut_oid, _, _ = merge_sort(contoh, 0, "oid")
    indeks, banding = binary_search(urut_oid, 0, "Y")
    assert indeks >= 0 and urut_oid[indeks][0] == "Y"
    indeks, _ = binary_search(urut_oid, 0, "TIDAK-ADA")
    assert indeks == -1
    assert binary_search([], 0, "X")[0] == -1
    assert insertion_sort([], 1, "harga")[0] == []
    assert merge_sort([], 1, "harga")[0] == []
    print("Tes M3: LULUS (stabilitas, urutan, pencarian, data kosong)")

def demo():
    cek_m3()
    judul, pesanan = baca_pesanan()
    print("\n=== M3: SORT & SEARCH ===")
    print("Jumlah pesanan CSV:", len(pesanan))
    if not pesanan:
        print("CSV kosong; tidak ada data untuk diuji.")
        return

    idx_harga = indeks_kolom(judul, "harga")
    idx_oid = indeks_kolom(judul, "oid")

    jumlah = min(2000, len(pesanan))
    contoh = pesanan[:jumlah]
    mulai = time.perf_counter()
    hasil_ins, banding_ins, pindah_ins = insertion_sort(contoh, idx_harga, "harga")
    waktu_ins = (time.perf_counter() - mulai) * 1000
    mulai = time.perf_counter()
    hasil_merge, banding_merge, pindah_merge = merge_sort(contoh, idx_harga, "harga")
    waktu_merge = (time.perf_counter() - mulai) * 1000

    print("\n1. INSERTION SORT | harga |", jumlah, "baris")
    print("Waktu (ms):", round(waktu_ins, 4))
    print("Perbandingan:", banding_ins, "Pemindahan:", pindah_ins)
    print("\n2. MERGE SORT | harga |", jumlah, "baris")
    print("Waktu (ms):", round(waktu_merge, 4))
    print("Perbandingan:", banding_merge, "Pemindahan:", pindah_merge)
    print("Hasil sama:", data_sama(hasil_ins, hasil_merge))

    target = pesanan[len(pesanan) // 2][idx_oid]
    mulai = time.perf_counter()
    posisi_linear, banding_linear = linear_search(pesanan, idx_oid, target)
    waktu_linear = (time.perf_counter() - mulai) * 1000

    mulai = time.perf_counter()
    terurut_oid, banding_urut, _ = merge_sort(pesanan, idx_oid, "oid")
    waktu_persiapan = (time.perf_counter() - mulai) * 1000
    mulai = time.perf_counter()
    posisi_binary, banding_binary = binary_search(terurut_oid, idx_oid, target)
    waktu_binary = (time.perf_counter() - mulai) * 1000

    print("\n3. LINEAR SEARCH | oid:", target)
    print("Ditemukan pada indeks:", posisi_linear)
    print("Perbandingan:", banding_linear, "Waktu (ms):", round(waktu_linear, 4))
    print("\n4. BINARY SEARCH | oid:", target)
    print("Persiapan urut oid (ms):", round(waktu_persiapan, 4))
    print("Perbandingan untuk mengurutkan:", banding_urut)
    print("Ditemukan pada indeks daftar terurut:", posisi_binary)
    print("Perbandingan pencarian:", banding_binary)
    print("Waktu pencarian saja (ms):", round(waktu_binary, 4))
    print("OID sama:", posisi_binary >= 0 and
          pesanan[posisi_linear][idx_oid] == terurut_oid[posisi_binary][idx_oid])

if __name__ == "__main__":
    demo()
