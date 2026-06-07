# test_ai.py - Test koneksi ke Google Gemini API (FIXED)
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key dari .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 50)
print("TEST KONEKSI GOOGLE GEMINI API")
print("=" * 50)

# Cek apakah API Key ada
if not GEMINI_API_KEY:
    print("❌ API Key TIDAK DITEMUKAN!")
    print("   Silakan buat file .env dengan isi: GEMINI_API_KEY=your_key_here")
    exit()

print(f"✅ API Key ditemukan: {GEMINI_API_KEY[:15]}...")

# Coba konfigurasi
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Konfigurasi API berhasil")
except Exception as e:
    print(f"❌ Konfigurasi gagal: {e}")
    exit()

# Coba list model yang tersedia
try:
    print("\n📋 Mencari model yang tersedia...")
    models = genai.list_models()
    available_models = []
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"   - {m.name}")
    
    if not available_models:
        print("❌ Tidak ada model generateContent yang tersedia!")
        exit()
    
    # Gunakan model pertama yang tersedia
    model_name = available_models[0]
    print(f"\n✅ Menggunakan model: {model_name}")
    
    model = genai.GenerativeModel(model_name)
    
    # Test dengan pertanyaan sederhana
    response = model.generate_content("Sebutkan 3 hal tentang analisis data HR dalam bahasa Indonesia")
    print("\n" + "=" * 50)
    print("RESPONSE DARI AI:")
    print("=" * 50)
    print(response.text)
    print("=" * 50)
    print("\n✅✅✅ API BEKERJA DENGAN BAIK! ✅✅✅")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Kemungkinan masalah:")
    print("   1. API Key tidak valid (format harus AIzaSy...)")
    print("   2. Kuota API habis")
    print("   3. API Key belum di-enable di Google AI Studio")