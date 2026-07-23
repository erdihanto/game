import streamlit as st
import streamlit.components.v1 as components
import random
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kuis Penjumlahan Interaktif",
    page_icon="🧮",
    layout="centered"
)

# --- CSS MODERN & STYLING TOMBOL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Membatasi lebar tampilan agar tetap rapi seperti aplikasi mobile */
    .main .block-container {
        max-width: 480px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Sembunyikan header/footer bawaan Streamlit */
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* Kartu Soal */
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

    /* Papan Skor Top Bar */
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

    /* TOMBOL PILIHAN GANDA PANJANG & UNIFORM */
    .option-btn > .stButton > button {
        width: 100% !important;
        height: 58px !important;
        border-radius: 14px !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 2px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 6px !important;
        transition: all 0.15s ease-in-out !important;
    }

    .option-btn > .stButton > button:hover {
        border-color: #3B82F6 !important;
        color: #2563EB !important;
        background-color: #EFF6FF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.15) !important;
    }

    .option-btn > .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Style Tombol Sekunder (Kategori / Navigasi) */
    .secondary-btn > .stButton > button {
        height: 48px !important;
        font-size: 0.95rem !important;
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
if 'trigger_flash' not in st.session_state:
    st.session_state.trigger_flash = False
if 'flash_count' not in st.session_state:
    st.session_state.flash_count = 0

# --- LOGIKA SOAL ---
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
        st.session_state.trigger_flash = False
    else:
        st.session_state.skor_salah += 1
        st.session_state.trigger_flash = True
        st.session_state.flash_count += 1
        
    generate_soal(st.session_state.kategori)

# --- INJEKSI FLASH MERAH & SUARA NOTIFIKASI (KONSISTEN SETIAP SALAH) ---
if st.session_state.trigger_flash:
    # Menggunakan iframe component agar JavaScript selalu dieksekusi ulang tanpa caching
    components.html(f"""
        <script>
        (function() {{
            // 1. Bunyikan Suara Error (Buzzer)
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(200, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.3);
                
                gain.gain.setValueAtTime(0.4, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                
                osc.start();
                osc.stop(ctx.currentTime + 0.3);
            }} catch(e) {{}}

            // 2. Tampilkan Flash Merah pada Layar Utama
            try {{
                const parentDoc = window.parent.document;
                const flashDiv = parentDoc.createElement('div');
                flashDiv.style.position = 'fixed';
                flashDiv.style.top = '0';
                flashDiv.style.left = '0';
                flashDiv.style.width = '100vw';
                flashDiv.style.height = '100vh';
                flashDiv.style.backgroundColor = 'rgba(239, 68, 68, 0.65)';
                flashDiv.style.zIndex = '999999';
                flashDiv.style.pointerEvents = 'none';
                flashDiv.style.transition = 'opacity 0.4s ease-out';
                flashDiv.style.opacity = '1';
                
                parentDoc.body.appendChild(flashDiv);
                
                setTimeout(() => {{
                    flashDiv.style.opacity = '0';
                    setTimeout(() => {{
                        if (flashDiv.parentNode) {{
                            flashDiv.parentNode.removeChild(flashDiv);
                        }}
                    }}, 400);
                }}, 50);
            }} catch(e) {{}}
        }})();
        </script>
    """, height=0, width=0)
    
    st.session_state.trigger_flash = False

# --- TAMPILAN ANTARMUKA (UI) ---

st.markdown("<h3 style='text-align: center; color: #0F172A; font-weight: 800; margin-bottom: 20px;'>🧮 Kuis Penjumlahan</h3>", unsafe_allow_html=True)

# 1. SCREEN: PILIH KATEGORI
if not st.session_state.soal_aktif:
    st.markdown("""
        <div class="quiz-card">
            <h4 style="color: #334155; margin: 0 0 8px 0; font-weight: 700;">Pilih Modul Belajar</h4>
            <p style="color: #64748b; font-size: 0.9rem; margin: 0;">Pilih angka penjumlahan yang ingin kamu latih</p>
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
    # Papan Skor
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

    # Pilihan Ganda Membujur Panjang (1 Kolom, Ukuran Sama & Rapi)
    st.markdown('<div class="option-btn">', unsafe_allow_html=True)
    for idx, opsi in enumerate(st.session_state.pilihan):
        if st.button(str(opsi), key=f"opt_{idx}_{st.session_state.flash_count}", use_container_width=True):
            cek_jawaban(opsi)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Selesai & Lihat Hasil", type="secondary", use_container_width=True):
        st.session_state.soal_aktif = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 3. SCREEN: HASIL AKHIR
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
