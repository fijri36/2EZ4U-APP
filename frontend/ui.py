import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
from backend.m1_pesanan import ArrayPesanan, LinkedListPesanan, baca_pesanan, buat_pesanan
from backend.m2_antrean import MesinAntrean, ke_postfix, hitung
from backend.m3_laporan import insertion_sort, merge_sort, linear_search, binary_search, indeks_kolom

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Aplikasi2EZ4U(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('2EZ4U Food Delivery')
        self.geometry('1200x760')
        self.minsize(970, 620)
        self.configure(bg='#d9d9d9')
        self.header = []
        self.array = ArrayPesanan()
        self.linked = LinkedListPesanan()
        self.antrean = MesinAntrean(4)
        self.key = 'load'
        self.fields = {}
        self.waktu_m3 = 0.0
        self.oid_berikut = 1
        self._layout()
        self._menu('load', 'Load / Muat ulang')

    def _layout(self):
        tk.Label(self, text='✳  2EZ4U Food Delivery', bg='#473472', fg='#D6F4ED', font=('Segoe UI', 15, 'bold'), anchor='w', padx=16).pack(fill='x', padx=10, pady=(10, 0), ipady=10)
        self.status = tk.StringVar(value='siap')
        tk.Label(self,textvariable=self.status,bg='#473472',fg='white',anchor='w',padx=8).pack(fill='x',padx=10,pady=(2,8))
        body = tk.Frame(self, bg='#D6F4ED')
        body.pack(fill='both', expand=True, padx=10)
        side = tk.Frame(body, bg='#dddddd', width=290)
        side.pack(side='left', fill='y')
        side.pack_propagate(False)
        canvas = tk.Canvas(side, bg='#D6F4ED', highlightthickness=0)
        bar = ttk.Scrollbar(side, orient='vertical', command=canvas.yview)
        bar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.configure(yscrollcommand=bar.set)
        self.side_inner = tk.Frame(canvas, bg='#D6F4ED')
        canvas.create_window((0, 0), window=self.side_inner, anchor='nw')
        self.side_inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        self._side_section('DATA')
        self._side_item('Muat Ulang', 'load')

        self._side_section('M1 - DATA PESANAN')
        for prefix, nama in [('array','Array'), ('linked','Linked List')]:
            for op, label in [('lihat','Lihat Pesanan'),('reguler','Tambah Reguler'),('prioritas','Tambah Prioritas'),('vip','Tambah VIP'),('hapus','Hapus Pesanan')]:
                self._side_item(f'{nama} - {label}', f'm1_{prefix}_{op}')

        self._side_section('M2 - STACK & QUEUE')
        for key, label in [('postfix','Stack - Postfix (Mesin Kasir)'),
                           ('undo','Stack - Undo'),
                           ('redo','Stack - Redo'),
                           ('enqueue','Queue - Enqueue'),
                           ('dequeue_naif','Queue - Dequeue Naif'),
                           ('dequeue_circular','Queue - Dequeue Circular')]:
            self._side_item(label, 'm2_'+key)

        self._side_section('M3 - SORT & SEARCH')
        for key, label in [('insertion','Sort - Insertion Sort'),('merge','Sort - Merge Sort'),('linear','Search - Linear Search'),('binary','Search - Binary Search')]:
            self._side_item(label, 'm3_'+key)
        right = tk.Frame(body, bg='#D6F4ED', padx=12, pady=12)
        right.pack(side='left', fill='both', expand=True)
        self.title_label = tk.Label(right, bg='#D6F4ED', font=('Segoe UI',13,'bold'), anchor='w')
        self.title_label.pack(fill='x')
        self.desc_label = tk.Label(right, bg='#eeeeee', fg='#87BAC3', anchor='w', justify='left', wraplength=800)
        self.desc_label.pack(fill='x', pady=(6,12))
        self.hint_frame = tk.Frame(right, bg='#e4e7eb', padx=10, pady=8)
        self.hint_frame.pack(fill='x', pady=(4, 8))
        self.hint = tk.Label(self.hint_frame, bg='#e4e7eb', fg='#4b5563', font=('Segoe UI', 9), justify='left', wraplength=750)
        self.hint.pack(anchor='w')
        self.form = tk.Frame(right, bg='#eeeeee')
        self.form.pack(fill='x', pady=(0,8))
        self.action = tk.Button(right, text='JALANKAN', bg='#53629E', fg='white', width=18, command=self._run)
        self.action.pack(anchor='w', pady=(0,10))

        self.tabel_frame = tk.Frame(right, bg='#eeeeee')
        kolom = ('langkah', 'token', 'tindakan', 'stack', 'output')
        self.tabel = ttk.Treeview(self.tabel_frame, columns=kolom, show='headings', height=9)
        for k, w in zip(kolom, (70, 60, 330, 150, 250)):
            self.tabel.heading(k, text=k)
            self.tabel.column(k, width=w, anchor='w')
        sb = ttk.Scrollbar(self.tabel_frame,orient='vertical',command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=sb.set)
        self.tabel.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        self.log = tk.Text(right, height=4, font=('Consolas',9))
        self.log.pack(side='bottom', fill='x')
        tk.Label(right, text='COMMAND / RIWAYAT AKSI', bg='#eeeeee', anchor='w', font=('Segoe UI',8,'bold')).pack(side='bottom', fill='x', pady=(8,2))
        self.resultframe = tk.Frame(right)
        self.resultframe.pack(fill='both', expand=True)
        self.result = tk.Text(self.resultframe, font=('Consolas',10), wrap='none')
        ybar = ttk.Scrollbar(self.resultframe, command=self.result.yview)
        xbar = ttk.Scrollbar(self.resultframe, orient='horizontal', command=self.result.xview)
        self.result.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        self.result.pack(side='left', fill='both', expand=True)
        ybar.pack(side='right',fill='y')
        xbar.pack(side='bottom',fill='x')

    def _side_section(self, label):
        tk.Label(self.side_inner,text=label,bg='#dddddd',fg='#536172',font=('Segoe UI',9,'bold'),anchor='w').pack(fill='x',padx=8,pady=(12,3))

    def _side_item(self,label,key):
        tk.Button(self.side_inner,text=label,anchor='w',font=('Segoe UI',9),relief='groove', command=lambda: self._menu(key,label)).pack(fill='x',padx=8,pady=1)

    def _menu(self, key, label):
        self.key = key
        self.title_label.config(text=label)

        self.result.delete('1.0', 'end')
        for r in self.tabel.get_children():
            self.tabel.delete(r)
        self.tabel_frame.pack_forget()
        if key in ('m2_postfix', 'm2_undo', 'm2_redo', 'm2_dequeue_naif',
                   'm2_dequeue_circular', 'm3_insertion', 'm3_merge','m3_linear_search', 'm3_binary_search' ):
            self.resultframe.pack_configure(fill='x', expand=False)
            self.result.config(height=5)
        else:
            self.resultframe.pack_configure(fill='both', expand=True)
            self.result.config(height=15)
        self.status.set('siap')
        self.hint.config(text='')

        for widget in self.form.winfo_children():
            widget.destroy()
        self.fields = {}

        if key == 'load':
            desc = 'Muat 200.000 pesanan CSV ke Array & Linked List. Tampilkan seluruh isi di panel hasil.'
            fields = []
            action = 'LOAD'

        elif key.startswith('m1_'):
            op = key.rsplit('_', 1)[-1]
            desc = 'Operasi M1 berdasarkan ' + ('Array' if '_array_' in key else 'Linked List')
            if op in ('lihat', 'hapus'):
                fields = [('Pencarian berdasarkan', 'Indeks', ('Indeks', 'OID', 'Restoran')),
                          ('Nilai pencarian', '0')]
            else:
                fields = [('Nama pelanggan', ''), ('Nama restoran', ''),
                          ('Nama menu', ''), ('Harga', '')]
            action = {'lihat': 'LIHAT', 'hapus': 'HAPUS', 'vip': 'TAMBAH VIP',
                      'prioritas': 'TAMBAH PRIORITAS', 'reguler': 'TAMBAH REGULER'}[op]

        elif key.startswith('m2_'):
            op = key[3:]
            if op == 'postfix':
                desc = 'Struk ditulis infix, lalu dihitung dua tahap dengan stack: tahap 1 infix menjadi postfix, tahap 2 postfix dievaluasi.'
                fields = [('Struk belanja (infix)', '')]
                action = 'HITUNG'
                self._set_kolom(('langkah', 'token', 'tindakan', 'stack', 'output'), (70, 60, 330, 150, 250))
                self.tabel_frame.pack(fill='x', pady=(0, 8), before=self.resultframe)
            elif op == 'enqueue':
                desc = 'Queue: pesanan baru masuk ke belakang. Pesanan ditambahkan ke queue naif dan circular.'
                fields = [('Nama pelanggan', '')]
                action = 'ENQUEUE'
            elif op in ('dequeue_naif', 'dequeue_circular'):
                if op == 'dequeue_naif':
                    self.title_label.config(text='Queue naif: ambil dari depan dengan menggeser isi')
                    desc = 'Mengambil indeks 0 lalu menggeser seluruh sisa isi satu petak ke kiri. Biayanya O(n) setiap kali.'
                else:
                    self.title_label.config(text='Queue circular: ambil dari depan dengan memajukan pointer')
                    desc = 'Mengambil elemen di front lalu hanya memajukan pointer front. Biayanya O(1) setiap kali.'
                fields = [('Berapa kali dequeue', '1')]
                action = 'DEQUEUE'
                self._set_kolom(('#', 'oid', 'pelanggan', 'resto', 'menu', 'masuk'), (50, 110, 220, 150, 150, 100))
                self.tabel_frame.pack(fill='both', expand=True, pady=(0, 8), before=self.resultframe)
            elif op == 'undo':
                desc = 'Mengambil catatan teratas tumpukan undo, lalu menjalankan kebalikannya. Aksi terakhirlah yang dibatalkan lebih dulu.'
                fields = []
                action = 'UNDO'
                self._set_kolom(('#', 'oid', 'pelanggan', 'resto', 'menu'), (50, 110, 220, 150, 150))
                self.tabel_frame.pack(fill='x', pady=(0, 8), before=self.resultframe)
            else:
                desc = 'Mengambil catatan teratas tumpukan redo, lalu mengerjakan ulang aksi aslinya. Aksi baru apa pun mengosongkan tumpukan ini.'
                fields = []
                action = 'REDO'
                self._set_kolom(('#', 'oid', 'pelanggan', 'resto', 'menu'), (50, 110, 220, 150, 150))
                self.tabel_frame.pack(fill='x', pady=(0, 8), before=self.resultframe)

        elif key.startswith('m3_'):
            op = key[3:]
            if op in ('insertion', 'merge'):
                if op == 'insertion':
                    self.title_label.config(text='Sort: insertion sort, O(n²)')
                    desc = 'Setiap elemen digeser mundur sampai menemukan tempatnya. Sederhana, tetapi kerjanya tumbuh kuadratik.'
                else:
                    self.title_label.config(text='Sort: merge sort, O(n log n)')
                    desc = 'Larik dibelah dua terus-menerus, lalu potongan yang sudah terurut disatukan kembali.'
                fields = [('Jumlah baris diurutkan', '10'),
                          ('Diurutkan menurut', 'harga', ('oid', 'harga', 'selesai'))]
                action = 'URUTKAN'
                self._set_kolom(('#', 'oid', 'harga', 'selesai', 'resto', 'menu'), (50, 110, 110, 110, 160, 160))
                self.tabel_frame.pack(fill='both', expand=True, pady=(0, 8), before=self.resultframe)
            else:
                desc = 'Sorting / Searching M3 dengan algoritma buatan sendiri'
                fields = [('OID yang dicari', '')]
                action = 'CARI'

        self.desc_label.config(text=desc)
        self.action.config(text=action)
        for r, item in enumerate(fields):
            name, default = item[:2]
            tk.Label(self.form, text=name, bg='#eeeeee', anchor='w', width=22).grid(row=r, column=0, sticky='w', pady=3)
            var = tk.StringVar(value=default)
            if len(item) == 3:
                ttk.Combobox(self.form, textvariable=var, values=item[2], state='readonly', width=31).grid(row=r, column=1, sticky='w')
            else:
                tk.Entry(self.form, textvariable=var, width=35).grid(row=r, column=1, sticky='w')
            self.fields[name] = var

        petunjuk = {
            'm2_dequeue_naif': 'Sampai panjang antrean; coba 1 lalu 100 untuk melihat bedanya',
            'm2_dequeue_circular': 'Sampai panjang antrean; coba 1 lalu 100 untuk melihat bedanya',
            'm3_insertion': 'diambil dari awal data; coba 1.000 lalu 2.000 lalu 4.000 (maks 20.000)',
            'm3_merge': 'diambil dari awal data; coba 1.000 lalu 2.000 lalu 4.000\noid (teks), harga (angka), selesai (waktu selesai)',
        }.get(key)
        if petunjuk:
            tk.Label(self.form, text=petunjuk, bg='#eeeeee', fg='#6b7a90',
                     font=('Segoe UI', 8)).grid(row=len(fields), column=1, sticky='w')

    def _get(self,key): return self.fields[key].get().strip()
    def _output(self,msg):
        self.result.delete('1.0','end'); self.result.insert('end',str(msg))
    def _log(self,label,elapsed):
        self.log.insert('end',time.strftime('%H:%M:%S')+f'  {label}   {elapsed:.4f} ms\n'); self.log.see('end')
    def _oid_index(self):
        for i, name in enumerate(self.header):
            if name.strip().lower()=='oid': return i
        raise ValueError('Kolom oid tidak ditemukan')
    def _row_text(self,row):
        return '\n'.join(f'{name}: {row[i] if i < len(row) else ""}' for i,name in enumerate(self.header))
    def _load(self):
        path = os.path.join(ROOT, 'data', 'pesanan.csv')
        if not os.path.isfile(path):
            raise FileNotFoundError('Letakkan pesanan.csv di ' + os.path.dirname(path))
        self.header, data = baca_pesanan()
        self.array = ArrayPesanan()
        self.linked = LinkedListPesanan()
        self.antrean = MesinAntrean(4)
        idx_status = self._kolom('status')
        idx_oid = self._oid_index()
        jumlah_antre = 0
        
        for row in data:
            self.array.tambah_belakang(row)
            self.linked.tambah_belakang(row)

            if row[idx_status].strip().upper() == 'ANTRE':
                oid = row[idx_oid]
                self.antrean.naif.enqueue(oid)
                self.antrean.circular.enqueue(oid)
                jumlah_antre += 1

        nomor_terbesar = 0

        for row in data:
            oid = row[idx_oid].strip()

            if oid.startswith('O-') and oid[2:].isdigit():
                nomor = int(oid[2:])
                if nomor > nomor_terbesar:
                    nomor_terbesar = nomor

        self.oid_berikut = nomor_terbesar + 1
        tampil = min(100, len(data))
        baris = [' | '.join(self.header), '=' * 90]
        for i in range(tampil):
            baris.append(' | '.join(data[i]))
        self._output('Total: %d pesanan (menampilkan %d pertama)\n\n' % (len(data), tampil) + '\n'.join(baris))
        self.status.set('%d pesanan dimuat | %d pesanan ANTRE masuk kedua queue' 
            % (len(data), jumlah_antre)
        )

    def _kolom(self, nama):
        for i, h in enumerate(self.header):
            if h.strip().lower() == nama:
                return i
        raise ValueError('Kolom ' + nama + ' tidak ditemukan')

    def _cari(self, obj, struktur, kolom, query, berhenti_pertama, batas=20):
        """Return (daftar posisi, total cocok). Tanpa dict/set."""
        q = query.strip().lower()
        posisi = []
        total = 0
        if struktur == 'array':
            for i in range(obj.jumlah()):
                if obj.ambil(i)[kolom].strip().lower() == q:
                    total += 1
                    if len(posisi) < batas:
                        posisi.append(i)
                    if berhenti_pertama:
                        break
        else:
            node = obj.head
            i = 0
            while node is not None:
                if node.data[kolom].strip().lower() == q:
                    total += 1
                    if len(posisi) < batas:
                        posisi.append(i)
                    if berhenti_pertama:
                        break
                node = node.next
                i += 1
        return posisi, total

    def _m1(self, key):
        _, struktur, op = key.split('_')
        obj = self.array if struktur == 'array' else self.linked
        other = self.linked if struktur == 'array' else self.array
        if obj.jumlah() == 0:
            raise ValueError('Klik DATA → Load terlebih dahulu.')

        if op in ('lihat', 'hapus'):
            kind = self._get('Pencarian berdasarkan')
            query = self._get('Nilai pencarian')
            if not query:
                raise ValueError('Nilai pencarian harus diisi')

            t0 = time.perf_counter()
            if kind == 'Indeks':
                try:
                    pos = int(query)
                except ValueError:
                    raise ValueError('Indeks harus bilangan bulat')
                if not 0 <= pos < obj.jumlah():
                    raise ValueError('Indeks di luar jangkauan (0 - %d)' % (obj.jumlah() - 1))
                daftar, total = [pos], 1
            else:
                kolom = self._kolom('oid' if kind == 'OID' else 'resto')
                berhenti = (kind == 'OID') or (op == 'hapus')
                daftar, total = self._cari(obj, struktur, kolom, query, berhenti)
                if not daftar:
                    return '%s tidak ditemukan: %s' % (kind, query)
            ms_cari = (time.perf_counter() - t0) * 1000

            t0 = time.perf_counter()
            if op == 'lihat':
                hasil = [obj.ambil(p) for p in daftar]
            else:
                hasil = [obj.hapus(daftar[0])]
            ms_op = (time.perf_counter() - t0) * 1000

            if op == 'hapus':
                if other.hapus(daftar[0]) != hasil[0]:
                    raise RuntimeError('Array dan Linked List tidak sinkron')

            teks = '%s | %s | cari berdasarkan %s: %s\n' % (op.upper(), struktur.upper(), kind, query)
            if kind == 'Restoran' and op == 'lihat':
                teks += 'Total cocok: %d pesanan, menampilkan %d pertama\n' % (total, len(daftar))
            elif kind == 'Restoran' and op == 'hapus':
                teks += '(menghapus pesanan pertama yang cocok)\n'
            teks += '\nindeks | ' + ' | '.join(self.header) + '\n' + '-' * 90 + '\n'
            posisi_tampil = daftar if op == 'lihat' else [daftar[0]]
            for p, row in zip(posisi_tampil, hasil):
                teks += '%6d | %s\n' % (p, ' | '.join(row))
            teks += '\nWaktu pencarian: %.5f ms\nWaktu %s: %.5f ms' % (ms_cari, op, ms_op)
            return teks

        jenis = op.upper()
        oid = 'O-%06d' % self.oid_berikut
        row = buat_pesanan(self.header, oid, jenis)
        for i, name in enumerate(self.header):
            field = {'pelanggan': 'Nama pelanggan', 'resto': 'Nama restoran',
                     'menu': 'Nama menu', 'harga': 'Harga'}.get(name.strip().lower())
            if field:
                val = self._get(field)
                if not val:
                    raise ValueError(field + ' harus diisi')
                if field == 'Harga' and not val.isdigit():
                    raise ValueError('Harga harus berupa angka')
                row[i] = val
        method = {'vip': 'tambah_depan', 'prioritas': 'tambah_tengah',
                  'reguler': 'tambah_belakang'}[op]
        t0 = time.perf_counter()
        getattr(obj, method)(row)
        elapsed = (time.perf_counter() - t0) * 1000
        getattr(other, method)(row)
        self.oid_berikut += 1
        return ('Pesanan %s berhasil ditambahkan\n\n' % jenis + self._row_text(row)
                + '\n\nWaktu %s: %.5f ms\nJumlah total: %d' % (struktur, elapsed, obj.jumlah()))
    
    def _isi_antrean(self):
        q = self.antrean.circular
        return ' <- '.join(str(q.lihat(i)) for i in range(q.jumlah())) or 'kosong'

    def _tampil_detail(self, pesanan):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        self._set_kolom(
            ('kolom', 'isi'),
            (180, 400)
        )

        for i, nama_kolom in enumerate(self.header):
            nilai = pesanan[i]

            if nama_kolom.strip().lower() == 'harga':
                try:
                    nilai = format(int(float(nilai)), ',').replace(',', '.')
                except ValueError:
                    pass

            self.tabel.insert(
                '',
                'end',
                values=(nama_kolom, nilai)
            )

        self.tabel_frame.pack(
            fill='both',
            expand=True,
            pady=(4, 8),
            before=self.resultframe
        )

    def _set_kolom(self, kolom, lebar):
        self.tabel.config(columns=kolom)
        for k, w in zip(kolom, lebar):
            self.tabel.heading(k, text=k)
            self.tabel.column(k, width=w, anchor='w')

    def _rb(self, n):
        return format(n, ',').replace(',', '.')

    def _baris_oid(self, oid):
        """Cari baris lengkap di data berdasarkan OID. Return (pelanggan, resto, menu)."""
        try:
            pos, _ = self._cari(self.array, 'array', self._oid_index(), oid, True)
            if not pos:
                return ('-', '-', '-')
            row = self.array.ambil(pos[0])
            return (row[self._kolom('pelanggan')], row[self._kolom('resto')], row[self._kolom('menu')])
        except ValueError:
            return ('-', '-', '-')
    def _fmt_jam(self, detik):
        try:
            d = int(float(detik))
        except ValueError:
            return '-'
        return '%02d:%02d:%02d' % (d // 3600, d % 3600 // 60, d % 60)
    
    def _isi_tabel_sort(self, rows, batas=100):
        for r in self.tabel.get_children():
            self.tabel.delete(r)
        i_oid = self._oid_index()
        i_harga = self._kolom('harga')
        i_selesai = indeks_kolom(self.header, 'selesai')
        i_resto = self._kolom('resto')
        i_menu = self._kolom('menu')
        for no, row in enumerate(rows[:batas], 1):
            try:
                harga = self._rb(int(float(row[i_harga])))
            except ValueError:
                harga = '-'
            self.tabel.insert('', 'end', values=(no, row[i_oid], harga,
                              self._fmt_jam(row[i_selesai]), row[i_resto], row[i_menu]))

    def _masuk_oid(self, oid):
        pos, _ = self._cari(self.array, 'array', self._oid_index(), oid, True)
        if not pos:
            return '-'
        return self._fmt_jam(self.array.ambil(pos[0])[self._kolom('t_masuk_detik')])
            
    def _info_antrean(self):
            q = self.antrean.circular
            return ('\nIsi antrean : %s\nJumlah      : %d | kapasitas circular: %d | front: %d | rear: %d'
                    '\nStack undo  : %d | stack redo: %d'
                    % (self._isi_antrean(), q.jumlah(), q.kapasitas, q.front, q.rear,
                    self.antrean.undo.jumlah(), self.antrean.redo.jumlah()))

    def _m2(self, key):
        op = key[3:]
        if op == 'postfix':
            exp = self._get('Struk belanja (infix)')
            if not exp:
                raise ValueError('Struk belanja harus diisi')
            catat = []
            post = ke_postfix(exp, catat)
            total = hitung(post, catat)
            for r in self.tabel.get_children():
                self.tabel.delete(r)
            for baris in catat:
                self.tabel.insert('', 'end', values=baris)
            rp = format(total, ',.0f').replace(',', '.')
            return f'Struk  : {exp}\nPostfix: {post}\nTOTAL  : Rp {rp}'

        if op == 'enqueue':
            nama = self._get('Nama pelanggan')

            if not nama:
                raise ValueError('Nama pelanggan harus diisi')

            if not self.header:
                raise ValueError('Klik DATA -> LOAD terlebih dahulu.')
            oid = 'O-%06d' % self.oid_berikut
            pesanan = buat_pesanan(self.header, oid, 'REGULER')

            for i, kolom in enumerate(self.header):
                kolom = kolom.strip().lower()

                if kolom == 'oid':
                    pesanan[i] = oid
                elif kolom == 'pelanggan':
                    pesanan[i] = nama
                elif kolom == 'resto':
                    pesanan[i] = 'kafe-teknik'
                elif kolom == 'menu':
                    pesanan[i] = 'roti-bakar'
                elif kolom == 'harga':
                    pesanan[i] = '12000'
                elif kolom == 'prioritas':
                    pesanan[i] = '3'
                elif kolom == 't_masuk_detik':
                    sekarang = time.localtime()
                    detik = (
                        sekarang.tm_hour * 3600
                        + sekarang.tm_min * 60
                        + sekarang.tm_sec
                    )
                    pesanan[i] = str(detik)
                elif kolom == 't_selesai_detik':
                    pesanan[i] = ''
                elif kolom == 'status':
                    pesanan[i] = 'ANTRE'

            self.array.tambah_belakang(pesanan)
            self.linked.tambah_belakang(pesanan)

            self.antrean.enqueue(oid)
            self.oid_berikut += 1

            self._log(
                'queue_enqueue_naif -> M2 - queue',
                self.antrean.waktu_enqueue_naif
            )
            self._log(
                'queue_enqueue_circular -> M2 - queue',
                self.antrean.waktu_enqueue_circular
            )

            hasil = (
                f'{oid} masuk ke barisan paling belakang '
                f'pada KEDUA antrean.\n'
                f'Panjang sekarang: '
                f'naif {self._rb(self.antrean.naif.jumlah())}, '
                f'circular {self._rb(self.antrean.circular.jumlah())}.'
            )

            self._tampil_detail(pesanan)

            return hasil

        if op in ('dequeue_naif', 'dequeue_circular'):
            try:
                n = int(self._get('Berapa kali dequeue'))
            except ValueError:
                raise ValueError('Jumlah harus bilangan bulat')
            if n < 1:
                raise ValueError('Jumlah minimal 1')
            panjang_awal = self.antrean.naif.jumlah()
            front_awal = self.antrean.circular.front
            keluar = self.antrean.dequeue(n)
            for r in self.tabel.get_children():
                self.tabel.delete(r)
            if not keluar:
                self.hint.config(text='')
                return 'Antrean kosong, tidak ada yang dilayani.'
            for no, oid in enumerate(keluar, 1):
                pelanggan, resto, menu = self._baris_oid(str(oid))
                self.tabel.insert('', 'end', values=(no, oid, pelanggan, resto, menu, self._masuk_oid(str(oid))))
            k = len(keluar)
            if op == 'dequeue_naif':
                geser = self.antrean.geser_terakhir
                self.hint.config(text='Mengambil indeks 0 memaksa seluruh sisa isi satu petak ke kiri, jadi O(n) per dequeue. '
                                    'Panjang antrean saat itu %s, dan segitu pula kira-kira geseran yang terjadi. '
                                    'Bandingkan waktunya dengan menu DEQUEUE CIRCULAR.' % self._rb(panjang_awal))
                return ('%d pesanan keluar dari depan antrean naif.\nTotal %s elemen digeser, rata-rata %s geseran per dequeue.\n'
                        'Sisa antrean naif %s.' % (k, self._rb(geser), self._rb(geser // k), self._rb(self.antrean.naif.jumlah())))
            self.hint.config(text='Circular hanya memajukan pointer front, jadi O(1) per dequeue tanpa menggeser elemen. '
                                'Panjang antrean saat itu %s. Bandingkan waktunya dengan menu DEQUEUE NAIF.' % self._rb(panjang_awal))
            return ('%d pesanan keluar dari depan antrean circular.\n'
            'Total 0 elemen digeser, pointer front maju %d kali (indeks %d -> %d, kapasitas %s).\n'
            'Sisa antrean circular %s.' % (k, k, front_awal, self.antrean.circular.front,
                                           self._rb(self.antrean.circular.kapasitas),
                                           self._rb(self.antrean.circular.jumlah())))
        if op == 'undo':
            for r in self.tabel.get_children():
                self.tabel.delete(r)
            aksi = self.antrean.undo_last()
            if aksi is None:
                return 'Tumpukan undo kosong, tidak ada aksi yang bisa dibatalkan.' + self._info_antrean()
            jenis, data = aksi
            if jenis == 'ENQUEUE':
                kalimat = 'Pembatalan enqueue: %s dikeluarkan lagi dari belakang.' % data[0]
                catatan = 'Kebalikan dari enqueue adalah membuang elemen paling belakang, dan itu murah pada kedua antrean.'
            else:
                kalimat = 'Pembatalan dequeue: %d pesanan dikembalikan ke depan antrean.' % len(data)
                catatan = ('Kebalikan dari dequeue adalah menaruh elemen kembali di depan: antrean naif harus '
                           'menggeser semua elemen, circular cukup memundurkan pointer front.')
            for no, oid in enumerate(data, 1):
                pelanggan, resto, menu = self._baris_oid(str(oid))
                self.tabel.insert('', 'end', values=(no, oid, pelanggan, resto, menu))
            return ('%s\nPanjang antrean sekarang: naif %s, circular %s. Tumpukan undo tersisa %d catatan.\n\n%s'
                    % (kalimat, self._rb(self.antrean.naif.jumlah()),
                       self._rb(self.antrean.circular.jumlah()),
                       self.antrean.undo.jumlah(), catatan))

        if op == 'redo':
            for r in self.tabel.get_children():
                self.tabel.delete(r)
            aksi = self.antrean.redo_last()
            if aksi is None:
                return 'Tumpukan redo kosong, tidak ada aksi yang bisa dikerjakan ulang.' + self._info_antrean()
            jenis, data = aksi
            if jenis == 'ENQUEUE':
                kalimat = 'Enqueue dikerjakan lagi: %s masuk kembali ke belakang.' % data[0]
            else:
                kalimat = 'Dequeue dikerjakan lagi: %d pesanan dilayani lagi dari depan.' % len(data)
            for no, oid in enumerate(data, 1):
                pelanggan, resto, menu = self._baris_oid(str(oid))
                self.tabel.insert('', 'end', values=(no, oid, pelanggan, resto, menu))
            return ('%s\nPanjang antrean sekarang: naif %s, circular %s. Tumpukan undo %d, redo %d.\n\n'
                    'Redo mengerjakan ULANG aksi aslinya, bukan kebalikannya, lalu mengembalikan '
                    'catatannya ke tumpukan undo supaya bisa dibatalkan lagi.'
                    % (kalimat, self._rb(self.antrean.naif.jumlah()),
                       self._rb(self.antrean.circular.jumlah()),
                       self.antrean.undo.jumlah(), self.antrean.redo.jumlah()))
        if op in ('insertion', 'merge'):
            try:
                n = int(self._get('Jumlah baris diurutkan').replace('.', ''))
            except ValueError:
                raise ValueError('Jumlah baris harus bilangan bulat')
            if n < 1:
                raise ValueError('Jumlah baris minimal 1')
            if op == 'insertion' and n > 20000:
                raise ValueError('Insertion sort dibatasi maksimal 20.000 baris. Gunakan merge sort.')
            n = min(n, len(data))
            nama = self._get('Diurutkan menurut')
            index = indeks_kolom(self.header, nama)

            t0 = time.perf_counter()
            if op == 'insertion':
                rows, banding, pindah = insertion_sort(data[:n], index, nama)
            else:
                rows, banding, pindah = merge_sort(data[:n], index, nama)
            self.waktu_m3 = (time.perf_counter() - t0) * 1000

            self._isi_tabel_sort(rows)
            if op == 'insertion':
                self.hint.config(text='Setiap elemen digeser mundur sampai menemukan tempatnya, jadi biayanya tumbuh kuadratik: '
                                      'melipatduakan jumlah baris membuat kerjanya kira-kira empat kali lipat. '
                                      'Jalankan SORT - MERGE SORT pada jumlah dan kunci yang sama, lalu bandingkan angka perbandingannya.')
            else:
                self.hint.config(text='Larik dibelah dua terus-menerus lalu potongan yang sudah terurut disatukan kembali. '
                                      'Kedalaman belahannya log n dan tiap lapis menyentuh n elemen, jadi O(n log n). '
                                      'Hasilnya sama persis dengan insertion sort karena keduanya stabil.')
            teks = '%s pesanan diurutkan menurut %s.\n%s perbandingan, %s pemindahan.' % (
                self._rb(len(rows)), nama, self._rb(banding), self._rb(pindah))
            if len(rows) > 100:
                teks += '\nTabel menampilkan 100 baris teratas.'
            return teks

    def _m3(self, key):
        if self.array.jumlah() == 0:
            raise ValueError('Klik DATA → Load terlebih dahulu')
        op = key[3:]
        idxoid = self._oid_index()
        data = [self.array.ambil(i) for i in range(self.array.jumlah())]

        if op in ('insertion', 'merge'):
            try:
                n = int(self._get('Jumlah baris diurutkan').replace('.', ''))
            except ValueError:
                raise ValueError('Jumlah baris harus bilangan bulat')
            if n < 1:
                raise ValueError('Jumlah baris minimal 1')
            if op == 'insertion' and n > 20000:
                raise ValueError('Insertion sort dibatasi maksimal 20.000 baris. Gunakan merge sort.')
            n = min(n, len(data))
            nama = self._get('Diurutkan menurut')
            index = indeks_kolom(self.header, nama)

            t0 = time.perf_counter()
            if op == 'insertion':
                rows, banding, pindah = insertion_sort(data[:n], index, nama)
            else:
                rows, banding, pindah = merge_sort(data[:n], index, nama)
            self.waktu_m3 = (time.perf_counter() - t0) * 1000

            self._isi_tabel_sort(rows)
            if op == 'insertion':
                self.hint.config(text='Setiap elemen digeser mundur sampai menemukan tempatnya, jadi biayanya tumbuh kuadratik: '
                                      'melipatduakan jumlah baris membuat kerjanya kira-kira empat kali lipat. '
                                      'Jalankan SORT - MERGE SORT pada jumlah dan kunci yang sama, lalu bandingkan angka perbandingannya.')
            else:
                self.hint.config(text='Larik dibelah dua terus-menerus lalu potongan yang sudah terurut disatukan kembali. '
                                      'Kedalaman belahannya log n dan tiap lapis menyentuh n elemen, jadi O(n log n). '
                                      'Hasilnya sama persis dengan insertion sort karena keduanya stabil.')
            teks = '%s pesanan diurutkan menurut %s.\n%s perbandingan, %s pemindahan.' % (
                self._rb(len(rows)), nama, self._rb(banding), self._rb(pindah))
            if len(rows) > 100:
                teks += '\nTabel menampilkan 100 baris teratas.'
            return teks

        target = self._get('OID yang dicari')
        if op == 'linear':
            start = time.perf_counter()
            pos, comparisons = linear_search(data, idxoid, target)
            prep = 0
            duration = (time.perf_counter() - start) * 1000
            item = data[pos] if pos >= 0 else None
        else:
            start = time.perf_counter()
            ordered, _, _ = merge_sort(data, idxoid, 'oid')
            prep = (time.perf_counter() - start) * 1000
            start = time.perf_counter()
            pos, comparisons = binary_search(ordered, idxoid, target)
            duration = (time.perf_counter() - start) * 1000
            item = ordered[pos] if pos >= 0 else None
        self.waktu_m3 = duration 
        return (f'{op.upper()} SEARCH\nOID: {target}\nIndeks: {pos}\nPerbandingan: {comparisons}\n'
                f'Persiapan sorting: {prep:.4f} ms\nPencarian: {duration:.4f} ms\n\n'
                + (self._row_text(item) if item else 'Tidak ditemukan'))
    
    def _run(self):
        key = self.key
        start = time.perf_counter()
        try:
            if key == 'load':
                self._load()
                self._log('LOAD CSV', (time.perf_counter() - start) * 1000)
                return
            if key.startswith('m1_'):
                result = self._m1(key)
            elif key.startswith('m2_'):
                result = self._m2(key)
            elif key.startswith('m3_'):
                result = self._m3(key)
            else:
                result = 'Modul belum diimplementasikan.'
            elapsed = (time.perf_counter() - start) * 1000
            self._output(result)

            if key.startswith('m2_dequeue'):
                jenis = 'queue naif' if key.endswith('naif') else 'queue circular'
                ms = (self.antrean.waktu_naif if key.endswith('naif') else self.antrean.waktu_circular) * 1000
                self._log(f'{key} -> M2 – {jenis}', ms)
                self.status.set(f'[M2 – {jenis}]  {ms:.2f} ms')
            elif key in ('m3_insertion', 'm3_merge', 'm3_linear', 'm3_binary'):
                nama = {'m3_insertion': 'insertion sort', 'm3_merge': 'merge sort',
                        'm3_linear': 'linear search', 'm3_binary': 'binary search'}[key]
                self._log(f'{nama.replace(" ", "_")} -> M3 – {nama}', self.waktu_m3)
                self.status.set(f'[M3 – {nama}]  {self.waktu_m3:.2f} ms')
            else:
                self._log(key, elapsed)
                self.status.set(f'{key} berhasil | {elapsed:.4f} ms | M1: {self.array.jumlah()} pesanan')
        except Exception as error:
            messagebox.showerror('Operasi gagal', str(error))
            self.status.set('Gagal: ' + str(error))
      
        except Exception as error:
            messagebox.showerror('Operasi gagal',str(error))
            self.status.set('Gagal: '+str(error))

if __name__=='__main__':
    Aplikasi2EZ4U().mainloop()