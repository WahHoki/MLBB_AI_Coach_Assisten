import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load Environment & API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_ID = "gemini-1.5-flash" # BENAR
# 2. Setup Tampilan & Anti-Translate Fix
st.set_page_config(page_title="Asisten Taktik MLBB", page_icon="🎮", layout="wide")

# Mencegah error 'removeChild' akibat Google Translate
st.markdown("<html lang='en' class='notranslate'>", unsafe_allow_html=True)

# 3. Sidebar untuk Pengaturan
with st.sidebar:
    st.header("⚙️ Coach Settings")
    st.info("Status API: " + ("✅ Aktif" if API_KEY else "❌ Belum Terisi"))
    
    model_choice = st.selectbox(
        "Pilih Otak Coach:",
        ["gemini-2.5-flash", "gemini-2.0-flash"],
        help="Gunakan 1.5-flash jika kuota 2.0 sedang penuh."
    )
    
    st.divider()
    st.write("Dibuat oleh Hoki @ STIKOM Bali")

# 4. Inisialisasi Client
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    st.error("Waduh bro, API Key belum ada di .env! Isi dulu ya.")
    st.stop()

# 5. UI Utama
st.title("🎮 MLBB Tactic Assistant")
st.caption("Analisis draft, counter pick, dan build item ala Pro Player.")

# Menggunakan Container agar UI lebih rapi
container = st.container(border=True)
with container:
    user_input = st.text_input("Input Kondisi Draft:", placeholder="Lawan pick Ling dan Angela, counternya apa?")
    analyze_button = st.button("Analisis Sekarang! 🚀", use_container_width=True)

# 6. Logika Pemrosesan
if analyze_button:
    if user_input:
        with st.spinner("Coach lagi liat replay musuh..."):
            try:
                system_instruction = """
                Kamu adalah mantan pelatih Esports profesional Mobile Legends. 
                Tugasmu: Analisis draft, beri counter hero, dan saran build item meta.
                Gaya bicara: Santai, ala gamer Indonesia (pake gue-lo/bro), tapi tajam dan analitis.
                """
                
                response = client.models.generate_content(
                    model=model_choice,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7
                    ),
                    contents=user_input
                )
                
                st.subheader("📋 Hasil Analisis Coach:")
                st.markdown(response.text)
                
            except Exception as e:
                if "429" in str(e):
                    st.error("🚨 Kuota Habis! Coba ganti model di sidebar atau tunggu 1 menit.")
                else:
                    st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Input-nya jangan kosong dong, Coach mau analisis apa? 😂")