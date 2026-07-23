import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kuis Penjumlahan Interaktif",
    page_icon="🧮",
    layout="centered"
)

# --- CSS MODERN & PRESISI (RESPONSIF & RAPI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

    /* Tampilan Dasar */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Batasi Lebar Kontainer Utama Agar Rapi Seperti Aplikasi Mobile */
    .main .block-container {
        max-width: 480px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Hilangkan Header Bawaan Streamlit */
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* Flash Merah Layar Penuh Saat Jawaban Salah */
    @keyframes redFlashAnim {
        0% { background-color: rgba(239, 68, 68, 0.75); }
        100% { background-color: transparent; }
    }
    .flash-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 999999;
        animation: redFlashAnim 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }

    /* Kartu Soal / Header Card */
    .quiz-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }

    .question-text {
        font-size: 3.2rem;
        font-weight: 800;
        color: #0F172A;
        margin: 10px 0;
        letter-spacing: -1px;
    }

    /* Papan Skor Modern */
    .score-badge-container {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 16px;
    }
    .score-badge {
        flex: 1;
        padding: 10px;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .score-correct { background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
    .score-wrong { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }

    /* PENATAAN TOMBOL PILIHAN GANDA (SAMA RATA & RAPI) */
    .stButton > button {
        width: 100% !important;
        height: 70px !important;
        border-radius: 16px !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 2px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.15s ease-in-out !important;
    }

    .stButton > button:hover {
        border-color: #3B82F6 !important;
        color: #2563EB !important;
        background-color: #EFF6FF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px -3px rgba(59, 130, 246, 0.15) !important;
    }

    .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Kustomisasi Tombol Sekunder (Kategori & Selesai) */
    .secondary-btn > .stButton > button {
        height: 50px !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
    }
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

# --- LOGIKA KUIS ---
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
    st.session_state.soal_teks = f"{n1} + {n2}"
    
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

# --- EFEK FLASH MERAH & SUARA BUZZER JIKA JAWABAN SALAH ---
if st.session_state.flash_salah:
    # Audio Beep Base64 (Suara Error Pendek)
    BEEP_AUDIO = "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFb2x3e4SGi4yPj5CakZWWmJmZm5ycnpyampmYmZaVlJOMi4qIhoaEg4KBf318fXx8fX19fHx8fX1+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+"
    
    st.markdown(f"""
        <div class="flash-overlay"></div>
        <audio autoplay style="display:none;">
            <source src="{BEEP_AUDIO}" type="audio/wav">
        </audio>
        <script>
            // Fallback Web Audio API
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.35);
                
                gain.gain.setValueAtTime(0.5, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                
                osc.start();
                osc.stop(ctx.currentTime + 0.35);
            }} catch(e) {{}}
        </script>
    """, unsafe_allow_html=True)
    st.session_state.flash_salah = False

# --- TAMPILAN ANTARMUKA (UI) ---

st.markdown("<h3 style='text-align: center; color: #0F172A; font-weight: 800; margin-bottom: 20px;'>🧮 Kuis Penjumlahan</h3>", unsafe_allow_html=True)

# 1. SCREEN: PILIH KATEGORI
if not st.session_state.soal_aktif:
    st.markdown("""
        <div class="quiz-card">
            <h4 style="color: #334155; margin: 0 0 8px 0; font-weight: 700;">Pilih Modul Belajar</h4>
            <p style="color: #64748b; font-size: 0.9rem; margin: 0;">Pilih angka penjumlahan yang ingin dilatih</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(1, 10):
        if cols[(i-1)%3].button(f"Penjumlahan {i}", key=f"kat_{i}"):
            st.session_state.kategori = i
            generate_soal(i)
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 Penjumlahan Acak (Campuran)", use_container_width=True, type="primary"):
        st.session_state.kategori = 10
        generate_soal(10)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 2. SCREEN: KUIS AKTIF
else:
    # Papan Skor Top Bar
    st.markdown(f"""
        <div class="score-badge-container">
            <div class="score-badge score-correct">✓ Benar: {st.session_state.skor_benar}</div>
            <div class="score-badge score-wrong">✕ Salah: {st.session_state.skor_salah}</div>
        </div>
    """, unsafe_allow_html=True)

    # Kartu Soal
    st.markdown(f"""
        <div class="quiz-card">
            <div style="color: #64748B; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Berapakah Hasilnya?</div>
            <div class="question-text">{st.session_state.soal_teks} = ?</div>
        </div>
    """, unsafe_allow_html=True)

    # Grid 2x2 Tombol Pilihan Ganda Rapi & Simetris
    c1, c2 = st.columns(2)
    with c1:
        if st.button(str(st.session_state.pilihan[0]), key="opt_0"):
            cek_jawaban(st.session_state.pilihan[0])
            st.rerun()
        if st.button(str(st.session_state.pilihan[2]), key="opt_2"):
            cek_jawaban(st.session_state.pilihan[2])
            st.rerun()
            
    with c2:
        if st.button(str(st.session_state.pilihan[1]), key="opt_1"):
            cek_jawaban(st.session_state.pilihan[1])
            st.rerun()
        if st.button(str(st.session_state.pilihan[3]), key="opt_3"):
            cek_jawaban(st.session_state.pilihan[3])
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Selesai & Lihat Hasil", type="secondary", use_container_width=True):
        st.session_state.soal_aktif = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 3. SCREEN: HASIL AKHIR (Pilihan Selesai)
if not st.session_state.soal_aktif and (st.session_state.skor_benar > 0 or st.session_state.skor_salah > 0):
    total = st.session_state.skor_benar + st.session_state.skor_salah
    akurasi = (st.session_state.skor_benar / total * 100) if total > 0 else 0
    
    st.markdown(f"""
        <div class="quiz-card">
            <h3 style="color: #0F172A; margin-bottom: 15px; font-weight: 800;">🎉 Ringkasan Hasil</h3>
            <p style="font-size: 1.05rem; color: #475569; margin: 5px 0;">Total Soal Dijawab: <b>{total}</b></p>
            <p style="font-size: 1.1rem; color: #166534; font-weight: 700; margin: 5px 0;">Jawaban Benar: {st.session_state.skor_benar}</p>
            <p style="font-size: 1.1rem; color: #991B1B; font-weight: 700; margin: 5px 0;">Jawaban Salah: {st.session_state.skor_salah}</p>
            <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
            <h2 style="color: #2563EB; margin: 0; font-weight: 800;">Akurasi: {akurasi:.0f}%</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Ulangi Kuis", type="primary", use_container_width=True):
        st.session_state.skor_benar = 0
        st.session_state.skor_salah = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
