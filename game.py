import streamlit as st
import random

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Kuis Penjumlahan Modern",
    page_icon="🧮",
    layout="centered"
)

# --- INJEKSI CSS MODERN & ANIMASI FLASH ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Background Utama */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Container Kartu Modern (Glassmorphism) */
    .main-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.06);
        border: 1px solid rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 25px;
    }

    /* Teks Soal */
    .question-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #0f172a;
        margin: 15px 0;
        letter-spacing: -1px;
    }

    /* Flash Merah Saat Jawaban Salah */
    @keyframes redFlash {
        0% { background-color: rgba(239, 68, 68, 0.4); }
        100% { background-color: transparent; }
    }

    .flash-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 99999;
        animation: redFlash 0.5s ease-out forwards;
    }

    /* Kustomisasi Tombol Streamlit */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        color: #1e293b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
        color: #2563eb;
    }

    /* Papan Skor Modern */
    .score-container {
        display: flex;
        justify-content: space-around;
        background: #f1f5f9;
        padding: 12px 20px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .score-text-true { color: #10b981; font-weight: 800; font-size: 1.1rem; }
    .score-text-false { color: #ef4444; font-weight: 800; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION SESSION STATE ---
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
if 'flash_salah' not in st.session_state:
    st.session_state.flash_salah = False

# --- FUNGSI LOGIKA SOAL ---
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
        st.session_state.flash_salah = False
    else:
        st.session_state.skor_salah += 1
        st.session_state.flash_salah = True
        
    generate_soal(st.session_state.kategori)

# --- TRIGGER FLASH & SUARA KETIKA JAWABAN SALAH ---
if st.session_state.flash_salah:
    st.markdown("""
        <div class="flash-overlay"></div>
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(220, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(110, ctx.currentTime + 0.3);
                
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                
                osc.start();
                osc.stop(ctx.currentTime + 0.3);
            } catch(e) {}
        })();
        </script>
    """, unsafe_allow_html=True)
    st.session_state.flash_salah = False

# --- TAMPILAN TINGKAT ATAS (UI) ---

# HEADER APLIKASI
st.markdown("<h2 style='text-align: center; color: #0f172a; font-weight: 800; margin-bottom: 20px;'>🧮 Kuis Penjumlahan Interaktif</h2>", unsafe_allow_html=True)

# 1. SCREEN: PILIH KATEGORI
if not st.session_state.soal_aktif:
    st.markdown("""
        <div class="main-card">
            <h3 style="color: #334155; margin-bottom: 10px;">Pilih Modul Penjumlahan</h3>
            <p style="color: #64748b; font-size: 0.95rem;">Pilih angka yang ingin kamu latih hari ini</p>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i in range(1, 10):
        if cols[(i-1)%3].button(f"Penjumlahan {i}", key=f"kat_{i}"):
            st.session_state.kategori = i
            generate_soal(i)
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 Penjumlahan 10 (Acak Campuran)", use_container_width=True, type="primary"):
        st.session_state.kategori = 10
        generate_soal(10)
        st.rerun()

# 2. SCREEN: KUIS AKTIF
else:
    # Papan Skor
    st.markdown(f"""
        <div class="score-container">
            <span class="score-text-true">✓ Benar: {st.session_state.skor_benar}</span>
            <span class="score-text-false">✕ Salah: {st.session_state.skor_salah}</span>
        </div>
    """, unsafe_allow_html=True)

    # Tampilan Kartu Soal
    st.markdown(f"""
        <div class="main-card">
            <div style="color: #64748b; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Soal Penjumlahan</div>
            <div class="question-title">{st.session_state.soal_teks}</div>
        </div>
    """, unsafe_allow_html=True)

    # Grid Pilihan Jawaban
    cols = st.columns(2)
    for idx, opsi in enumerate(st.session_state.pilihan):
        if cols[idx % 2].button(str(opsi), key=f"btn_opsi_{idx}"):
            cek_jawaban(opsi)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Selesai & Lihat Hasil", type="secondary"):
        st.session_state.soal_aktif = False
        st.rerun()

# 3. SCREEN HASIL (Jika Selesai)
if not st.session_state.soal_aktif and (st.session_state.skor_benar > 0 or st.session_state.skor_salah > 0):
    total = st.session_state.skor_benar + st.session_state.skor_salah
    akurasi = (st.session_state.skor_benar / total * 100) if total > 0 else 0
    
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: #0f172a; margin-bottom: 20px;">🎉 Hasil Akhir</h2>
            <p style="font-size: 1.1rem; color: #475569;">Total Dijawab: <b>{total}</b></p>
            <p style="font-size: 1.2rem; color: #10b981; font-weight: 700;">Jawaban Benar: {st.session_state.skor_benar}</p>
            <p style="font-size: 1.2rem; color: #ef4444; font-weight: 700;">Jawaban Salah: {st.session_state.skor_salah}</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <h3 style="color: #2563eb;">Akurasi: {akurasi:.0f}%</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reset Skor & Main Lagi", type="primary"):
        st.session_state.skor_benar = 0
        st.session_state.skor_salah = 0
        st.rerun()
