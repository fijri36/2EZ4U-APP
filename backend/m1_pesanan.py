import time
import csv
import os

class ArrayPesanan:
    def __init__(self):
        self.data = []

    def tambah_depan(self, x):
        self.data.insert(0, x)

    def tambah_belakang(self, x):
        self.data.append(x)

    def tambah_tengah(self, x):
        posisi = len(self.data) // 2
        self.data.insert(posisi, x)

    def hapus(self, posisi):
        if posisi < 0 or posisi >= len(self.data):
            return None
        return self.data.pop(posisi)

    def ambil(self, posisi):
        if posisi < 0 or posisi >= len(self.data):
            return None
        return self.data[posisi]

    def jumlah(self):
        return len(self.data)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListPesanan:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def tambah_depan(self, x):
        node_baru = Node(x)
        node_baru.next = self.head
        self.head = node_baru
        if self.tail is None:
            self.tail = node_baru
        self.size += 1

    def tambah_belakang(self, x):
        node_baru = Node(x)
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru
        self.size += 1

    def tambah_tengah(self, x):
        posisi = self.size // 2
        if posisi == 0:
            self.tambah_depan(x)
            return

        node_baru = Node(x)
        sekarang = self.head
        for i in range(posisi - 1):
            sekarang = sekarang.next

        node_baru.next = sekarang.next
        sekarang.next = node_baru
        if node_baru.next is None:
            self.tail = node_baru
        self.size += 1

    def hapus(self, posisi):
        if posisi < 0 or posisi >= self.size:
            return None

        if posisi == 0:
            data = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        else:
            sekarang = self.head
            for i in range(posisi - 1):
                sekarang = sekarang.next
            data = sekarang.next.data
            sekarang.next = sekarang.next.next
            if sekarang.next is None:
                self.tail = sekarang

        self.size -= 1
        return data

    def ambil(self, posisi):
        if posisi < 0 or posisi >= self.size:
            return None
        sekarang = self.head
        for i in range(posisi):
            sekarang = sekarang.next
        return sekarang.data

    def jumlah(self):
        return self.size


def baca_pesanan():
    lokasi_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "pesanan.csv"
    )
    data_pesanan = []

    with open(lokasi_file, "r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.reader(file)
        judul_kolom = next(pembaca)
        for baris in pembaca:
            if baris:
                data_pesanan.append(baris)
    return judul_kolom, data_pesanan


def buat_pesanan(judul_kolom, id_baru, jenis):
    baris = [""] * len(judul_kolom)
    for i in range(len(judul_kolom)):
        nama_kolom = judul_kolom[i].strip().lower()
        if nama_kolom == "oid":
            baris[i] = id_baru
        elif nama_kolom == "prioritas":
            if jenis == "VIP":
                baris[i] = "1"
            elif jenis == "PRIORITAS":
                baris[i] = "2"
            else:
                baris[i] = "3"
        elif nama_kolom == "status":
            baris[i] = "ANTRE"
        elif nama_kolom == "pelanggan":
            baris[i] = "Pelanggan Test"
        elif nama_kolom == "resto":
            baris[i] = "Restoran Test"
        elif nama_kolom == "menu":
            baris[i] = "Menu Test"
        elif nama_kolom == "harga":
            baris[i] = "10000"
    return baris


def ukur_tambah(objek, nama_fungsi, data):
    mulai = time.perf_counter()
    if nama_fungsi == "depan":
        objek.tambah_depan(data)
    elif nama_fungsi == "tengah":
        objek.tambah_tengah(data)
    else:
        objek.tambah_belakang(data)
    return (time.perf_counter() - mulai)*1000


def tampilkan_waktu(waktu_array, waktu_linked):
    print("Array :", format(waktu_array, ".6f"), "ms")
    print("Linked List :", format(waktu_linked, ".6f"), "ms")


def demo():
    judul_kolom, pesanan = baca_pesanan()
    print("Jumlah pesanan CSV:", len(pesanan))

    array_besar = ArrayPesanan()
    linked_besar = LinkedListPesanan()

    for data in pesanan:
        array_besar.tambah_belakang(data)
        linked_besar.tambah_belakang(data)

    print("\n=== PERBANDINGAN PERFORMA M1 ===")
    print("Jumlah data awal:", len(pesanan))

    vip = buat_pesanan(judul_kolom, "TEST-VIP", "VIP")
    waktu_array = ukur_tambah(array_besar, "depan", vip)
    waktu_linked = ukur_tambah(linked_besar, "depan", vip)
    print("\n1. TAMBAH VIP (DEPAN)")
    tampilkan_waktu(waktu_array, waktu_linked)
    print("Data sama:", array_besar.ambil(0) == linked_besar.ambil(0))

    prioritas = buat_pesanan(judul_kolom, "TEST-PRIORITAS", "PRIORITAS")
    waktu_array = ukur_tambah(array_besar, "tengah", prioritas)
    waktu_linked = ukur_tambah(linked_besar, "tengah", prioritas)
    posisi_tengah = (array_besar.jumlah() - 1) // 2
    print("\n2. TAMBAH PRIORITAS (TENGAH)")
    tampilkan_waktu(waktu_array, waktu_linked)
    print("Data sama:", array_besar.ambil(posisi_tengah) == linked_besar.ambil(posisi_tengah))

    reguler = buat_pesanan(judul_kolom, "TEST-REGULER", "REGULER")
    waktu_array = ukur_tambah(array_besar, "belakang", reguler)
    waktu_linked = ukur_tambah(linked_besar, "belakang", reguler)
    posisi_akhir = array_besar.jumlah() - 1
    print("\n3. TAMBAH REGULER (BELAKANG)")
    tampilkan_waktu(waktu_array, waktu_linked)
    print("Data sama:", array_besar.ambil(posisi_akhir) == linked_besar.ambil(posisi_akhir))

    posisi = array_besar.jumlah() // 2
    mulai = time.perf_counter()
    hasil_array = array_besar.ambil(posisi)
    waktu_array = (time.perf_counter() - mulai) * 1000
    mulai = time.perf_counter()
    hasil_linked = linked_besar.ambil(posisi)
    waktu_linked = (time.perf_counter() - mulai) * 1000
    print("\n4. LIHAT PESANAN PADA INDEKS", posisi)
    tampilkan_waktu(waktu_array, waktu_linked)
    print("Data sama:", hasil_array == hasil_linked)
    print("ID pesanan:", hasil_array[0] 
          if hasil_array 
          else "Tidak ada")

    mulai = time.perf_counter()
    hapus_array = array_besar.hapus(posisi)
    waktu_array = (time.perf_counter() - mulai) * 1000
    mulai = time.perf_counter()
    hapus_linked = linked_besar.hapus(posisi)
    waktu_linked = (time.perf_counter() - mulai) * 1000
    print("\n5. HAPUS PESANAN PADA INDEKS", posisi)
    tampilkan_waktu(waktu_array, waktu_linked)
    print("Data yang dihapus sama:", hapus_array == hapus_linked)

    print("\n=== JUMLAH PESANAN AKHIR ===")
    print("Array       :", array_besar.jumlah())
    print("Linked List :", linked_besar.jumlah())
    print("Jumlah sama :", array_besar.jumlah() == linked_besar.jumlah())

def cek_m1():
    print("\n=== PENGUJIAN OTOMATIS M1 ===")

    array = ArrayPesanan()
    linked = LinkedListPesanan()

    for x in ["A", "B", "C", "D"]:
        array.tambah_belakang(x)
        linked.tambah_belakang(x)

    array.tambah_depan("VIP")
    linked.tambah_depan("VIP")

    assert array.ambil(0) == "VIP"
    assert linked.ambil(0) == "VIP"
    print("1. VIP masuk depan: BERHASIL")

    array.tambah_tengah("PRIORITAS")
    linked.tambah_tengah("PRIORITAS")

    assert array.ambil(2) == "PRIORITAS"
    assert linked.ambil(2) == "PRIORITAS"
    print("2. PRIORITAS masuk tengah: BERHASIL")

    array.tambah_belakang("REGULER")
    linked.tambah_belakang("REGULER")

    assert array.ambil(array.jumlah() - 1) == "REGULER"
    assert linked.ambil(linked.jumlah() - 1) == "REGULER"
    print("3. REGULER masuk belakang: BERHASIL")

    assert array.jumlah() == linked.jumlah()

    for i in range(array.jumlah()):
        assert array.ambil(i) == linked.ambil(i)

    print("4. Semua isi Array dan Linked List sama: BERHASIL")

    assert array.ambil(2) == linked.ambil(2)
    assert array.ambil(-1) is None
    assert linked.ambil(-1) is None
    print("5. Lihat pesanan: BERHASIL")

    hasil_array = array.hapus(2)
    hasil_linked = linked.hapus(2)

    assert hasil_array == "PRIORITAS"
    assert hasil_linked == "PRIORITAS"
    print("6. Hapus pesanan tengah: BERHASIL")

    assert linked.head.data == "VIP"
    assert linked.tail.data == "REGULER"
    assert linked.tail.next is None
    assert linked.size == array.jumlah()
    print("7. Head, tail, dan size: BERHASIL")

    while array.jumlah() > 0:
        assert array.hapus(0) == linked.hapus(0)

    assert linked.head is None
    assert linked.tail is None
    assert linked.jumlah() == 0
    print("8. Hapus hingga kosong: BERHASIL")

    array.tambah_belakang("BARU")
    linked.tambah_belakang("BARU")

    assert linked.head.data == "BARU"
    assert linked.tail.data == "BARU"
    assert array.ambil(0) == linked.ambil(0)
    print("9. Tambah data setelah kosong: BERHASIL")

    print("\nSEMUA PENGUJIAN M1 BERHASIL!")

if __name__ == "__main__":
    cek_m1()
    demo()
