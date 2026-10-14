import time
from backend.m1_pesanan import ArrayPesanan

class stack:
    def __init__(self):
        self.data = ArrayPesanan()
    def push(self, x):
        self.data.tambah_belakang(x)
    def pop(self):
        if self.kosong():
            return None
        return self.data.hapus(self.data.jumlah()-1)
    def peek(self):
        if self.kosong():
            return None
        return self.data.ambil(self.data.jumlah() - 1)
    def kosong(self):
        return self.data.jumlah()==0
    def jumlah(self):
        return self.data.jumlah()
    def bersihkan(self):
        self.data = ArrayPesanan()

def pecah_token(ekspresi):
    token=[]
    i = 0 
    while i < len (ekspresi):
        c = ekspresi[i]
        if c.isspace():
            i +=1
        elif c.isdigit():
            angka = ""
            while i < len(ekspresi) and ekspresi[i].isdigit():
                angka += ekspresi[i]
                i += 1
            token.append(angka)
        elif c in "+-*/()":
            token.append(c)
            i +=1
        else:
            raise ValueError("Karakter tidak dikenal: " + c)
    return token

def prioritas(operator):
    if operator == "*" or operator == "/":
        return 2
    if operator == "+" or operator == "-":
        return 1
    return 0 

def ke_postfix(ekspresi, catat=None):
    token = pecah_token(ekspresi)
    operator = stack()
    hasil = []
    no = 0
    for t in token:
        no += 1
        if t.isdigit():
            hasil.append(t)
            aksi = "operand, langsung ke output"
        elif t == "(":
            operator.push(t)
            aksi = "push ( ke stack"
        elif t == ")":
            while not operator.kosong() and operator.peek() != "(":
                hasil.append(operator.pop())
            if operator.kosong():
                raise ValueError("Kurung tutup tidak memiliki pasangan")
            operator.pop()
            aksi = "pop sampai ( , lalu buang ("
        else:
            aksi = "push " + t
            while (not operator.kosong() and operator.peek() != "("
                   and prioritas(operator.peek()) >= prioritas(t)):
                aksi = "pop " + operator.peek() + ", lalu push " + t
                hasil.append(operator.pop())
            operator.push(t)
        if catat is not None:
            catat.append(("1." + str(no), t, aksi, _isi(operator), " ".join(hasil) or "kosong"))

    while not operator.kosong():
        op = operator.pop()
        if op == "(":
            raise ValueError("Kurung buka tidak memiliki pasangan")
        hasil.append(op)
    if catat is not None:
        catat.append(("1.akhir", "-", "pop sisa stack ke output", "kosong", " ".join(hasil) or "kosong"))
    return " ".join(hasil)

def _isi(st):
    if st.kosong():
        return "kosong"
    s = ""
    for i in range(st.jumlah()):
        s += str(st.data.ambil(i)) + " "
    return s.strip()

def hitung(postfix, catat=None):
    angka = stack()
    no = 0
    for t in postfix.split():
        no += 1
        if t.isdigit():
            angka.push(int(t))
            aksi = "operand, push " + t
        elif t in ("+", "-", "*", "/"):
            b = angka.pop()
            a = angka.pop()
            if a is None or b is None:
                raise ValueError("Ekspresi postfix tidak lengkap")
            if t == "+":
                nilai = a + b
            elif t == "-":
                nilai = a - b
            elif t == "*":
                nilai = a * b
            else:
                if b == 0:
                    raise ZeroDivisionError("Tidak boleh membagi dengan nol")
                nilai = a / b
            angka.push(nilai)
            aksi = "pop %s dan %s, hitung %s, push %s" % (a, b, t, nilai)
        else:
            raise ValueError("Token postfix tidak valid: " + t)
        if catat is not None:
            catat.append(("2." + str(no), t, aksi, _isi(angka), "-"))
    if angka.jumlah() != 1:
        raise ValueError("Ekspresi postfix tidak valid")
    return angka.pop()

class AntreanNaif:
    def __init__(self):
        self.data = ArrayPesanan()
        self.total_geser = 0 
    def enqueue(self,x):
        self.data.tambah_belakang(x)
    def dequeue(self):
        if self.kosong():
            return None
        self.total_geser += self.data.jumlah() - 1
        return self.data.hapus(0)
    def tambah_depan(self, x):
        self.data.tambah_depan(x)
    def hapus_belakang(self):
        if self.kosong():
            return None
        return self.data.hapus(self.data.jumlah() - 1)
    def kosong(self):
        return self.data.jumlah() == 0
    def jumlah(self):
        return self.data.jumlah()
    def lihat(self, i):
        return self.data.ambil(i)

class AntreanMelingkar:
    def __init__(self, kapasitas=4):
        if kapasitas < 1:
            raise ValueError("Kapasitas minimal 1")
        self.data = [None] * kapasitas
        self.kapasitas = kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0
    def _tumbuh(self):
        baru = [None] * (self.kapasitas * 2)
        for i in range(self.count):
            baru[i] = self.lihat(i)
        self.data = baru
        self.kapasitas *= 2
        self.front = 0
        self.rear = self.count

    def enqueue(self, x):
        if self.count == self.kapasitas:
            self._tumbuh()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.kapasitas
        self.count += 1

    def dequeue(self):
        if self.kosong():
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self.count -= 1
        return x

    def tambah_depan(self, x):
        if self.count == self.kapasitas:
            self._tumbuh()
        self.front = (self.front - 1) % self.kapasitas
        self.data[self.front] = x
        self.count += 1

    def hapus_belakang(self):
        if self.kosong():
            return None
        self.rear = (self.rear - 1) % self.kapasitas
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x

    def kosong(self):
        return self.count == 0

    def jumlah(self):
        return self.count

    def lihat(self, i):
        if i < 0 or i >= self.count:
            return None
        return self.data[(self.front + i) % self.kapasitas]


class MesinAntrean:
    def __init__(self, kapasitas=4):
        self.naif = AntreanNaif()
        self.circular = AntreanMelingkar(kapasitas)
        self.undo = stack()
        self.redo = stack()
        self.waktu_naif = 0.0
        self.waktu_circular = 0.0
        self.geser_terakhir = 0
        self.waktu_enqueue_naif = 0.0
        self.waktu_enqueue_circular = 0.0

    def enqueue(self, x):
        awal = time.perf_counter()
        self.naif.enqueue(x)
        self.waktu_enqueue_naif = (
            time.perf_counter() - awal
        ) * 1000

        awal = time.perf_counter()
        self.circular.enqueue(x)
        self.waktu_enqueue_circular = (
            time.perf_counter() - awal
        ) * 1000

        self.undo.push(("ENQUEUE", [x]))
        self.redo.bersihkan()
        return x

    def dequeue(self, banyak=1):
        keluar = []
        self.waktu_naif = 0.0
        self.waktu_circular = 0.0
        geser_awal = self.naif.total_geser
        for i in range(banyak):
            if self.naif.kosong():
                break
            t = time.perf_counter()
            a = self.naif.dequeue()
            self.waktu_naif += time.perf_counter() - t
            t = time.perf_counter()
            b = self.circular.dequeue()
            self.waktu_circular += time.perf_counter() - t
            if a != b:
                raise RuntimeError("Isi kedua antrean tidak sama")
            keluar.append(a)
        self.geser_terakhir = self.naif.total_geser - geser_awal
        if len(keluar) > 0:
            self.undo.push(("DEQUEUE", keluar))
            self.redo.bersihkan()
            return keluar

    def undo_last(self):
        aksi = self.undo.pop()
        if aksi is None:
            return None
        jenis, data = aksi
        if jenis == "ENQUEUE":
            a = self.naif.hapus_belakang()
            b = self.circular.hapus_belakang()
            if a != data[0] or b != data[0]:
                raise RuntimeError("Data undo enqueue tidak cocok")
        else:
            for i in range(len(data) - 1, -1, -1):
                self.naif.tambah_depan(data[i])
                self.circular.tambah_depan(data[i])
        self.redo.push(aksi)
        return aksi

    def redo_last(self):
        aksi = self.redo.pop()
        if aksi is None:
            return None
        jenis, data = aksi
        if jenis == "ENQUEUE":
            self.naif.enqueue(data[0])
            self.circular.enqueue(data[0])
        else:
            for x in data:
                a = self.naif.dequeue()
                b = self.circular.dequeue()
                if a != x or b != x:
                    raise RuntimeError("Data redo dequeue tidak cocok")
        self.undo.push(aksi)
        return aksi

def demo():
    ekspresi = "(3*12000) + (2*8500) - 5000"
    postfix = ke_postfix(ekspresi)
    print("=== M2: KASIR STACK ===")
    print("Infix:", ekspresi)
    print("Postfix:", postfix)
    print("Total: Rp", format(hitung(postfix), ",.0f").replace(",", "."))

    antrean = MesinAntrean(4)
    print("\n=== M2: QUEUE DAN UNDO / REDO ===")
    for x in ("P1", "P2", "P3", "P4", "P5"):
        antrean.enqueue(x)
    print("Jumlah awal:", antrean.naif.jumlah())
    print("Dequeue 2:", antrean.dequeue(2))
    print("Undo:", antrean.undo_last())
    print("Redo:", antrean.redo_last())

    biasa = AntreanNaif()
    lingkar = AntreanMelingkar(4)
    for i in range(20000):
        biasa.enqueue(i)
        lingkar.enqueue(i)
    awal = time.perf_counter()
    for i in range(100):
        biasa.dequeue()
    waktu_naif = (time.perf_counter() - awal) * 1000
    awal = time.perf_counter()
    for i in range(100):
        lingkar.dequeue()
    waktu_circular = (time.perf_counter() - awal) * 1000
    print("\n=== PERBANDINGAN DEQUEUE 100 DARI 20.000 ===")
    print("Naif (ms):", round(waktu_naif, 4), "geseran:", biasa.total_geser)
    print("Circular (ms):", round(waktu_circular, 4), "geseran: 0")

if __name__ == "__main__":
    demo()
