import streamlit as st
import random
import time

# --- Setup State (Menyimpan data agar tidak hilang saat halaman di-refresh) ---
if 'kategori' not in st.session_state:
    st.session_state.kategori = None
if 'skor_benar' not in st.session_state:
    st.session_state.skor_benar = 0
if 'skor_salah' not in st.session_state:
    st.session_state.skor_salah = 0
if 'soal_aktif' not in st.session_state:
    st.session_state.soal_aktif = False
if 'pilihan' not in st.session_state:
    st.session_state.pilihan = []
if 'jawaban' not in st.session_state:
    st.session_state.jawaban = 0

def generate_soal(kategori):
    if 1 <= kategori <= 9:
        n1 = kategori
        n2 = random.randint(1, 9)
        if random.choice([True, False]):
            n1, n2 = n2, n1
    else:
        n1 = random.randint(1, 9)
        n2 = random.randint(1, 9)
        
    st.session_state.jawaban = n1 + n2
    st.session_state.soal_teks = f"{n1} + {n2} = ?"
    
    pilihan = [st.session_state.jawaban]
    while len(pilihan) < 4:
        acak = random.randint(2, 18)
        if acak not in pilihan:
            pilihan.append(acak)
            
    random.shuffle(pilihan)
    st.session_state.pilihan = pilihan
    st.session_state.soal_aktif = True

def cek_jawaban(jawaban_user):
    if jawaban_user == st.session_state.jawaban:
        st.session_state.skor_benar += 1
        st.success("Benar!")
    else:
        st.session_state.skor_salah += 1
        st.error("Salah!")
    time.sleep(0.5) # Jeda sebentar sebelum lanjut
    generate_soal(st.session_state.kategori)

# --- TAMPILAN UI ---
st.title("Kuis Penjumlahan Interaktif")

# Halaman 1: Pilih Kategori
if not st.session_state.soal_aktif:
    st.write("### Pilih Kategori")
    cols = st.columns(3)
    for i in range(1, 10):
        if cols[(i-1)%3].button(f"Penjumlahan {i}", use_container_width=True):
            st.session_state.kategori = i
            generate_soal(i)
            st.rerun()
            
    if st.button("Penjumlahan 10 (Acak)", use_container_width=True):
        st.session_state.kategori = 10
        generate_soal(10)
        st.rerun()

# Halaman 2: Kuis
else:
    col1, col2 = st.columns(2)
    col1.metric("Benar", st.session_state.skor_benar)
    col2.metric("Salah", st.session_state.skor_salah)
    
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.soal_teks}</h1>", unsafe_allow_html=True)
    
    st.write("### Pilih Jawaban:")
    cols = st.columns(2)
    for idx, opsi in enumerate(st.session_state.pilihan):
        if cols[idx % 2].button(str(opsi), use_container_width=True, key=f"btn_{idx}"):
            cek_jawaban(opsi)
            st.rerun()
            
    st.divider()
    if st.button("Selesai & Lihat Hasil", type="primary"):
        st.session_state.soal_aktif = False
        st.session_state.skor_benar = 0
        st.session_state.skor_salah = 0
        st.rerun()
