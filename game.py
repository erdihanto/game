import random
import time
import streamlit as st
import streamlit.components.v1 as components

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kuis Penjumlahan Interaktif", page_icon="🧮", layout="centered"
)

# --- INITIALIZATION SESSION STATE ---
if "screen" not in st.session_state:
    st.session_state.screen = "menu"  # Status: 'menu', 'quiz', 'result'
if "kategori" not in st.session_state:
    st.session_state.kategori = None
if "skor_benar" not in st.session_state:
    st.session_state.skor_benar = 0
if "skor_salah" not in st.session_state:
    st.session_state.skor_salah = 0
if "pilihan" not in st.session_state:
    st.session_state.pilihan = []
if "jawaban" not in st.session_state:
    st.session_state.jawaban = 0
if "soal_teks" not in st.session_state:
    st.session_state.soal_teks = ""
if "trigger_flash" not in st.session_state:
    st.session_state.trigger_flash = False
if "flash_count" not in st.session_state:
    st.session_state.flash_count = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# --- CSS STYLING & ANIMASI FLASH LATAR BELAKANG ---
flash_css = ""
if st.session_state.trigger_flash:
    flash_css = """
    @keyframes flashRed {
        0% { background-color: #FECACA; }
        100% { background-color: #F8FAFC; }
    }
    .stApp {
        animation: flashRed 0.4s ease-out forwards;
    }
    """

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    {flash_css}

    .main .block-container {{
        max-width: 520px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }}

    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Kartu Soal */
    .quiz-card {{
        background: #FFFFFF;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }}

    .question-text {{
        font-size: 3.5rem;
        font-weight: 800;
        color: #0F172A;
        margin: 10px 0;
        letter-spacing: -1px;
    }}

    /* Papan Skor Top Bar */
    .score-badge-container {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 16px;
    }}
    .score-badge {{
        flex: 1;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
    }}
    .score-correct {{ background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }}
    .score-wrong {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }}

    /* Timer Badge */
    .timer-badge {{
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-weight: 800;
        font-size: 1.2rem;
        margin-bottom: 16px;
    }}

    /* Tombol Pilihan Ganda */
    .option-btn > .stButton > button {{
        width: 100% !important;
        height: 65px !important;
        border-radius: 14px !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 2px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 10px !important;
    }}

    .secondary-btn > .stButton > button {{
        height: 50px !important;
        font-size: 1.05rem !important;
        border-radius: 12px !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)


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

    jawaban_benar = n1 + n2
    st.session_state.jawaban = jawaban_benar
    st.session_state.soal_teks = f"{n1} + {n2}"

    pilihan = {jawaban_benar}
    while len(pilihan) < 4:
        offset = random.choice([-3, -2, -1, 1, 2, 3])
        salah = jawaban_benar + offset
        if 2 <= salah <= 18:
            pilihan.add(salah)

    pilihan_list = list(pilihan)
    random.shuffle(pilihan_list)
    st.session_state.pilihan = pilihan_list
    st.session_state.start_time = time.time()


def cek_jawaban(jawaban_user):
    if jawaban_user == st.session_state.jawaban:
        st.session_state.skor_benar += 1
        st.session_state.trigger_flash = False
    else:
        st.session_state.skor_salah += 1
        st.session_state.trigger_flash = True
        st.session_state.flash_count += 1

    generate_soal(st.session_state.kategori)


# --- SUARA BUZZER AMAN UNTUK ANDROID TV ---
if st.session_state.trigger_flash:
    components.html(
        f"""
        <!-- trigger_audio_{st.session_state.flash_count} -->
        <script>
        setTimeout(function() {{
            try {{
                var targetWin = window.parent || window;
                var AudioCtx = targetWin.AudioContext || targetWin.webkitAudioContext;
                if (AudioCtx) {{
                    var ctx = new AudioCtx();
                    if (ctx.state === 'suspended') {{ ctx.resume(); }}
                    var osc = ctx.createOscillator();
                    var gain = ctx.createGain();
                    
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(160, ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(50, ctx.currentTime + 0.35);
                    
                    gain.gain.setValueAtTime(0.4, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
                    
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    
                    osc.start();
                    osc.stop(ctx.currentTime + 0.35);
                }}
            }} catch(e) {{
                console.log("Audio diblokir oleh TV:", e);
            }}
        }}, 50);
        </script>
    """,
        height=0,
        width=0,
    )
    st.session_state.trigger_flash = False


# --- ANTARMUKA APLIKASI (UI) ---

st.markdown(
    "<h2 style='text-align: center; color: #0F172A; font-weight: 800; margin-bottom: 20px;'>🧮 Kuis Penjumlahan</h2>",
    unsafe_allow_html=True,
)

# 1. SCREEN: MENU
if st.session_state.screen == "menu":
    st.markdown(
        """
        <div class="quiz-card">
            <h3 style="color: #334155; margin: 0 0 8px 0; font-weight: 700;">Pilih Modul Belajar</h3>
            <p style="color: #64748b; font-size: 1rem; margin: 0;">Pilih angka penjumlahan yang ingin kamu latih (10 Detik/Soal)</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(1, 10):
        if cols[(i - 1) % 3].button(f"Penjumlahan {i}", key=f"kat_{i}"):
            st.session_state.kategori = i
            st.session_state.skor_benar = 0
            st.session_state.skor_salah = 0
            generate_soal(i)
            st.session_state.screen = "quiz"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(
        "🎲 Penjumlahan Acak (Campuran)",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.kategori = 10
        st.session_state.skor_benar = 0
        st.session_state.skor_salah = 0
        generate_soal(10)
        st.session_state.screen = "quiz"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 2. SCREEN: KUIS AKTIF
elif st.session_state.screen == "quiz":
    st.markdown(
        f"""
        <div class="score-badge-container">
            <div class="score-badge score-correct">✓ Benar: {st.session_state.skor_benar}</div>
            <div class="score-badge score-wrong">✕ Salah: {st.session_state.skor_salah}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Hitung sisa waktu terlebih dahulu
    sisa_waktu = 10 - int(time.time() - st.session_state.start_time)

    # Cek apakah waktu sudah habis
    if sisa_waktu <= 0:
        cek_jawaban(-1)  # Anggap salah jika waktu habis
        st.rerun()

    # Tampilkan timer
    st.markdown(
        f'<div class="timer-badge">⏱️ Sisa Waktu: {sisa_waktu} detik</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="quiz-card">
            <div style="color: #64748B; font-weight: 700; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;">Berapakah Hasilnya?</div>
            <div class="question-text">{st.session_state.soal_teks} = ?</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="option-btn">', unsafe_allow_html=True)
    for idx, opsi in enumerate(st.session_state.pilihan):
        if st.button(
            str(opsi),
            key=f"opt_{idx}_{st.session_state.flash_count}",
            use_container_width=True,
        ):
            cek_jawaban(opsi)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button(
        "Selesai & Lihat Hasil", type="secondary", use_container_width=True
    ):
        st.session_state.screen = "result"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Refresh otomatis secara halus tiap 1 detik tanpa memblokir klik
    time.sleep(1)
    st.rerun()

# 3. SCREEN: HASIL AKHIR
elif st.session_state.screen == "result":
    total = st.session_state.skor_benar + st.session_state.skor_salah
    akurasi = (st.session_state.skor_benar / total * 100) if total > 0 else 0

    st.markdown(
        f"""
        <div class="quiz-card">
            <h2 style="color: #0F172A; margin-bottom: 15px; font-weight: 800;">🎉 Ringkasan Hasil</h2>
            <p style="font-size: 1.2rem; color: #475569; margin: 5px 0;">Total Soal Dijawab: <b>{total}</b></p>
            <p style="font-size: 1.2rem; color: #166534; font-weight: 700; margin: 5px 0;">Jawaban Benar: {st.session_state.skor_benar}</p>
            <p style="font-size: 1.2rem; color: #991B1B; font-weight: 700; margin: 5px 0;">Jawaban Salah: {st.session_state.skor_salah}</p>
            <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
            <h1 style="color: #2563EB; margin: 0; font-weight: 800;">Akurasi: {akurasi:.0f}%</h1>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Kembali ke Menu", type="primary", use_container_width=True):
        st.session_state.skor_benar = 0
        st.session_state.skor_salah = 0
        st.session_state.screen = "menu"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
