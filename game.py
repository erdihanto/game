import random
import tkinter as tk

# Mencoba mengimpor winsound untuk suara di Windows
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

class KuisPenjumlahanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kuis Penjumlahan Interaktif")
        self.root.geometry("400x550")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(False, False)

        # Variabel Game
        self.kategori = 1
        self.benar = 0
        self.salah = 0
        self.jawaban_benar = 0
        self.waktu_maksimal = 60  # Waktu dalam detik
        self.waktu_tersisa = 0
        self.timer_id = None

        # Frame Utama
        self.main_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tampilkan Menu Kategori Utama
        self.show_category_screen()

    # --- SUARA NOTIFIKASI SALAH ---
    def play_wrong_sound(self):
        if HAS_WINSOUND:
            winsound.Beep(300, 300)
        else:
            self.root.bell()

    # --- HALAMAN 1: PILIHAN KATEGORI ---
    def show_category_screen(self):
        self.clear_frame()

        lbl_title = tk.Label(self.main_frame, text="Pilih Kategori", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#2c3e50")
        lbl_title.pack(pady=10)

        grid_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        grid_frame.pack(pady=10)

        # Tombol Kategori 1 - 9
        for i in range(1, 10):
            row = (i - 1) // 2
            col = (i - 1) % 2
            btn = tk.Button(grid_frame, text=f"Penjumlahan {i}", font=("Arial", 11, "bold"), bg="#3498db", fg="white",
                            width=15, height=2, relief="flat", command=lambda k=i: self.start_quiz(k))
            btn.grid(row=row, column=col, padx=5, pady=5)

        # Tombol Kategori 10 (Campuran)
        btn_10 = tk.Button(grid_frame, text="Penjumlahan 10 (Acak)", font=("Arial", 11, "bold"), bg="#8e44ad", fg="white",
                           width=32, height=2, relief="flat", command=lambda: self.start_quiz(10))
        btn_10.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # --- HALAMAN 2: SOAL PILIHAN GANDA ---
    def start_quiz(self, kat):
        self.kategori = kat
        self.benar = 0
        self.salah = 0
        self.waktu_tersisa = self.waktu_maksimal
        self.clear_frame()

        # Teks Timer
        self.lbl_timer = tk.Label(self.main_frame, text=f"Waktu: {self.waktu_tersisa}s", font=("Arial", 14, "bold"), fg="#e74c3c", bg="#f0f8ff")
        self.lbl_timer.pack(pady=5)

        # Baris Skor
        self.score_frame = tk.Frame(self.main_frame, bg="#ecf0f1", relief="groove", bd=1)
        self.score_frame.pack(fill="x", pady=5)

        self.lbl_benar = tk.Label(self.score_frame, text="Benar: 0", font=("Arial", 11, "bold"), fg="#27ae60", bg="#ecf0f1")
        self.lbl_benar.pack(side="left", padx=15, pady=5)

        self.lbl_salah = tk.Label(self.score_frame, text="Salah: 0", font=("Arial", 11, "bold"), fg="#c0392b", bg="#ecf0f1")
        self.lbl_salah.pack(side="right", padx=15, pady=5)

        # Teks Soal
        self.lbl_soal = tk.Label(self.main_frame, text="", font=("Arial", 28, "bold"), bg="#f0f8ff", fg="#2c3e50")
        self.lbl_soal.pack(pady=20)

        # Grid Tombol Pilihan Ganda
        self.opt_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        self.opt_frame.pack(pady=10)

        self.buttons = []
        for i in range(4):
            row = i // 2
            col = i % 2
            btn = tk.Button(self.opt_frame, text="", font=("Arial", 16, "bold"), bg="#f39c12", fg="white",
                            width=10, height=2, relief="flat", command=lambda idx=i: self.check_answer(idx))
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.buttons.append(btn)

        # Tombol Berhenti (Selesai Lebih Awal)
        btn_selesai = tk.Button(self.main_frame, text="Selesai Sekarang", font=("Arial", 12, "bold"), bg="#7f8c8d", fg="white",
                                width=25, height=1, relief="flat", command=self.finish_quiz)
        btn_selesai.pack(pady=20)

        # Mulai Timer dan Soal Pertama
        self.update_timer()
        self.generate_question()

    # --- LOGIKA TIMER ---
    def update_timer(self):
        if self.waktu_tersisa > 0:
            self.lbl_timer.config(text=f"Waktu: {self.waktu_tersisa}s")
            self.waktu_tersisa -= 1
            # Memanggil fungsi ini lagi setiap 1000 milidetik (1 detik)
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.lbl_timer.config(text="Waktu Habis!")
            self.finish_quiz()

    # --- GENERATE SOAL & PILIHAN GANDA ---
    def generate_question(self):
        if 1 <= self.kategori <= 9:
            n1 = self.kategori
            n2 = random.randint(1, 9)
            if random.choice([True, False]):
                n1, n2 = n2, n1
        else:
            n1 = random.randint(1, 9)
            n2 = random.randint(1, 9)

        self.jawaban_benar = n1 + n2
        self.lbl_soal.config(text=f"{n1} + {n2} = ?")

        # Membuat 4 Pilihan Ganda Unik
        pilihan = [self.jawaban_benar]
        while len(pilihan) < 4:
            acak = random.randint(2, 18)
            if acak not in pilihan:
                pilihan.append(acak)

        random.shuffle(pilihan)

        for i in range(4):
            self.buttons[i].config(text=str(pilihan[i]))

    # --- PROSES CEK JAWABAN ---
    def check_answer(self, idx):
        opsi_dipilih = int(self.buttons[idx].cget("text"))

        if opsi_dipilih == self.jawaban_benar:
            self.benar += 1
            self.lbl_benar.config(text=f"Benar: {self.benar}")
        else:
            self.salah += 1
            self.lbl_salah.config(text=f"Salah: {self.salah}")
            self.play_wrong_sound() 

        # Lanjut ke soal berikutnya langsung
        self.generate_question()

    # --- HALAMAN 3: REKAP HASIL AKHIR ---
    def finish_quiz(self):
        # Batalkan timer jika tombol "Selesai" ditekan sebelum waktu habis
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        total = self.benar + self.salah
        akurasi = (self.benar / total * 100) if total > 0 else 0
        self.clear_frame()

        lbl_title = tk.Label(self.main_frame, text="Hasil Akhir", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#2c3e50")
        lbl_title.pack(pady=15)

        lbl_total = tk.Label(self.main_frame, text=f"Total Dijawab: {total}", font=("Arial", 14), bg="#f0f8ff")
        lbl_total.pack(pady=5)

        lbl_benar = tk.Label(self.main_frame, text=f"Jawaban Benar: {self.benar}", font=("Arial", 14, "bold"), fg="#27ae60", bg="#f0f8ff")
        lbl_benar.pack(pady=5)

        lbl_salah = tk.Label(self.main_frame, text=f"Jawaban Salah: {self.salah}", font=("Arial", 14, "bold"), fg="#c0392b", bg="#f0f8ff")
        lbl_salah.pack(pady=5)
        
        lbl_akurasi = tk.Label(self.main_frame, text=f"Akurasi: {akurasi:.0f}%", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#f0f8ff")
        lbl_akurasi.pack(pady=10)

        btn_ulang = tk.Button(self.main_frame, text="Main Lagi", font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                              width=20, height=2, relief="flat", command=self.show_category_screen)
        btn_ulang.pack(pady=30)

    # Helper untuk membersihkan layar
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# --- RUNNING PROGRAM ---
if __name__ == "__main__":
    root = tk.Tk()
    app = KuisPenjumlahanApp(root)
    root.mainloop()