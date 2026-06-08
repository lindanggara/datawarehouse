# dashboard.py - FULL FONT AWESOME - SEMUA CARD UNGU + LANDING PAGE (UPDATED)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime
import numpy as np

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# ============================================================
# CONFIGURE AI - DINONAKTIFKAN
# ============================================================
AI_AVAILABLE = False

def get_ai_insight(prompt):
    return "AI Insight tidak tersedia."

# ============================================================
# LANDING PAGE STATE
# ============================================================
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ============================================================
# LANDING PAGE - PREMIUM MODERN DESIGN (FINAL)
# ============================================================
if not st.session_state.show_dashboard:
    st.set_page_config(
        page_title="HR Analytics | Landing",
        page_icon="📊",
        layout="wide"
    )

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
            scroll-behavior: smooth;
        }
        
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        .stApp {
            background: linear-gradient(135deg, #faf9ff 0%, #f0ecff 100%) !important;
        }
        
        /* NAVBAR - GLASS */
        .lp-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.8rem 2rem;
            margin: 1rem 6%;
            background: rgba(255,255,255,0.85);
            backdrop-filter: blur(12px);
            border-radius: 80px;
            box-shadow: 0 8px 32px rgba(108,92,231,0.12);
            border: 1px solid rgba(108,92,231,0.15);
        }
        .lp-nav-logo {
            font-size: 22px;
            font-weight: 800;
            background: linear-gradient(135deg, #6C5CE7, #A594FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-decoration: none;
        }
        .lp-nav-links {
            display: flex;
            gap: 2.5rem;
        }
        .lp-nav-links a {
            font-size: 14px;
            font-weight: 500;
            color: #4a4a6a;
            text-decoration: none;
            transition: all 0.3s;
            position: relative;
        }
        .lp-nav-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(135deg, #6C5CE7, #A594FF);
            transition: width 0.3s;
            border-radius: 2px;
        }
        .lp-nav-links a:hover::after {
            width: 100%;
        }
        .lp-nav-links a:hover {
            color: #6C5CE7;
        }
        .lp-nav-chip {
            background: linear-gradient(135deg, #6C5CE7, #8B74FF);
            color: white;
            border-radius: 40px;
            padding: 6px 20px;
            font-size: 12px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(108,92,231,0.3);
        }
        
        /* Anchor */
        .anchor {
            display: block;
            position: relative;
            top: -90px;
            visibility: hidden;
        }
        
        /* HERO - GRADIENT MEWAH */
        .lp-hero {
            background: linear-gradient(135deg, #6C5CE7, #8B74FF, #A594FF);
            margin: 1.5rem 6%;
            border-radius: 48px;
            padding: 4rem 3rem;
            color: white;
            text-align: center;
            box-shadow: 0 25px 50px rgba(108,92,231,0.3);
            position: relative;
            overflow: hidden;
        }
        .lp-hero::before {
            content: '';
            position: absolute;
            top: -30%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        }
        .lp-hero::after {
            content: '';
            position: absolute;
            bottom: -30%;
            left: -20%;
            width: 250px;
            height: 250px;
            background: rgba(255,255,255,0.08);
            border-radius: 50%;
        }
        .lp-hero h1 {
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 1rem;
            position: relative;
            z-index: 1;
        }
        .lp-hero p {
            font-size: 18px;
            opacity: 0.95;
            max-width: 600px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
            line-height: 1.6;
        }
        
        /* STATS - DENGAN GLOW */
        .lp-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.2rem;
            margin: 2rem 6%;
        }
        .lp-stat-card {
            background: white;
            border-radius: 28px;
            padding: 1.8rem 1rem;
            text-align: center;
            border: 1px solid rgba(108,92,231,0.1);
            box-shadow: 0 8px 25px rgba(108,92,231,0.08);
            transition: all 0.3s;
        }
        .lp-stat-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 35px rgba(108,92,231,0.15);
            border-color: rgba(108,92,231,0.2);
        }
        .lp-stat-number {
            font-size: 40px;
            font-weight: 800;
            background: linear-gradient(135deg, #6C5CE7, #8B74FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .lp-stat-label {
            font-size: 14px;
            color: #8B74FF;
            margin-top: 8px;
            font-weight: 500;
        }
        
        /* PREVIEW */
        .lp-preview {
            background: white;
            margin: 2rem 6%;
            border-radius: 36px;
            padding: 2rem;
            border: 1px solid rgba(108,92,231,0.1);
            box-shadow: 0 8px 30px rgba(108,92,231,0.06);
        }
        .lp-preview-title {
            font-size: 22px;
            font-weight: 700;
            color: #6C5CE7;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .lp-preview-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }
        .lp-preview-card {
            background: #faf9ff;
            border-radius: 24px;
            padding: 1rem;
            border: 1px solid #f0ecff;
        }
        .lp-preview-bar {
            margin-bottom: 0.8rem;
        }
        .lp-preview-bar-meta {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 4px;
        }
        .lp-preview-bar-track {
            height: 8px;
            background: #ede9fe;
            border-radius: 99px;
            overflow: hidden;
        }
        .lp-preview-bar-fill {
            height: 100%;
            border-radius: 99px;
            background: linear-gradient(90deg, #6C5CE7, #8B74FF);
        }
        .lp-preview-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f0ecff;
        }
        .lp-preview-row:last-child {
            border-bottom: none;
        }
        .lp-preview-row-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .lp-preview-avatar {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #ede9fe, #f0ecff);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }
        
        /* SECTION HEADER */
        .lp-section-header {
            text-align: center;
            margin: 5rem 6% 2.5rem;
        }
        .lp-section-header h2 {
            font-size: 38px;
            font-weight: 800;
            color: #1a1a2e;
            margin-bottom: 0.75rem;
        }
        .lp-section-header h2 span {
            background: linear-gradient(135deg, #6C5CE7, #8B74FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .lp-section-header p {
            font-size: 16px;
            color: #6b7280;
            max-width: 550px;
            margin: 0 auto;
        }
        
        /* FEATURES */
        .lp-features {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.8rem;
            margin: 2rem 6%;
        }
        .lp-feature-card {
            background: white;
            border-radius: 28px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(108,92,231,0.08);
            box-shadow: 0 8px 20px rgba(108,92,231,0.05);
            transition: all 0.3s;
        }
        .lp-feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 40px rgba(108,92,231,0.12);
            border-color: rgba(108,92,231,0.2);
        }
        .lp-feature-icon {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #f0ecff, #e8e0ff);
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            margin: 0 auto 1rem;
        }
        .lp-feature-title {
            font-size: 18px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 0.5rem;
        }
        .lp-feature-desc {
            font-size: 14px;
            color: #6b7280;
            line-height: 1.6;
        }
        
        /* STEPS */
        .lp-steps {
            display: flex;
            gap: 2rem;
            margin: 2rem 6%;
        }
        .lp-step {
            flex: 1;
            background: white;
            border-radius: 28px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(108,92,231,0.08);
            box-shadow: 0 8px 20px rgba(108,92,231,0.05);
            transition: all 0.3s;
        }
        .lp-step:hover {
            transform: translateY(-5px);
        }
        .lp-step-num {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #6C5CE7, #8B74FF);
            border-radius: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            font-weight: 800;
            color: white;
            margin: 0 auto 1rem;
            box-shadow: 0 8px 20px rgba(108,92,231,0.3);
        }
        
        /* FOOTER */
        .lp-footer {
            background: white;
            margin: 0 6% 2rem 6%;
            border-radius: 28px;
            padding: 1.8rem 2rem;
            border: 1px solid rgba(108,92,231,0.1);
            box-shadow: 0 4px 20px rgba(108,92,231,0.04);
        }
        .lp-footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .lp-footer-logo {
            font-size: 18px;
            font-weight: 800;
            background: linear-gradient(135deg, #6C5CE7, #8B74FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .lp-footer-links {
            display: flex;
            gap: 1.8rem;
        }
        .lp-footer-links a {
            font-size: 13px;
            color: #9ca3af;
            text-decoration: none;
            transition: color 0.3s;
        }
        .lp-footer-links a:hover {
            color: #6C5CE7;
        }
        .lp-footer-copy {
            font-size: 12px;
            color: #c4b5fd;
            text-align: center;
            margin-top: 1.2rem;
            padding-top: 1.2rem;
            border-top: 1px solid #f0ecff;
        }
        
        /* BUTTON */
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #6C5CE7, #8B74FF) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 14px 36px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            box-shadow: 0 8px 25px rgba(108,92,231,0.4) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 35px rgba(108,92,231,0.5) !important;
        }
        
        @media (max-width: 900px) {
            .lp-stats, .lp-features, .lp-steps, .lp-preview-grid {
                grid-template-columns: 1fr;
                flex-direction: column;
            }
            .lp-stats {
                grid-template-columns: repeat(2, 1fr);
            }
            .lp-hero h1 {
                font-size: 32px;
            }
            .lp-section-header h2 {
                font-size: 28px;
            }
            .lp-nav-links {
                display: none;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # NAVBAR
    st.markdown("""
    <div class="lp-nav">
        <a href="#hero" class="lp-nav-logo" style="text-decoration:none;">📊 HR Analytics</a>
        <div class="lp-nav-links">
            <a href="#hero">Beranda</a>
            <a href="#features">Fitur</a>
            <a href="#steps">Cara Kerja</a>
            <a href="#about">Tentang</a>
        </div>
        <div class="lp-nav-chip">✨ Data Warehouse 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # HERO
    st.markdown('<span id="hero" class="anchor"></span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lp-hero">
        <h1>📊 HR Analytics<br>Performance Intelligence</h1>
        <p>Pantau KPI, kelompokkan karyawan, prediksi tren, dan buat keputusan strategis berbasis data — semua dalam satu dashboard yang mudah digunakan.</p>
    </div>
    """, unsafe_allow_html=True)

    # STATS (UPDATE DENGAN DATA REAL)
    st.markdown("""
    <div class="lp-stats">
        <div class="lp-stat-card"><div class="lp-stat-number">200</div><div class="lp-stat-label">Total Karyawan</div></div>
        <div class="lp-stat-card"><div class="lp-stat-number">40</div><div class="lp-stat-label">Proyek Aktif</div></div>
        <div class="lp-stat-card"><div class="lp-stat-number">2</div><div class="lp-stat-label">Cluster Karyawan</div></div>
        <div class="lp-stat-card"><div class="lp-stat-number">15</div><div class="lp-stat-label">Departemen</div></div>
    </div>
    """, unsafe_allow_html=True)

    # PREVIEW
    st.markdown("""
    <div class="lp-preview">
        <div class="lp-preview-title">📈 Preview Dashboard</div>
        <div class="lp-preview-grid">
            <div class="lp-preview-card">
                <div class="lp-preview-bar"><div class="lp-preview-bar-meta"><span>Engineering</span><span>92%</span></div><div class="lp-preview-bar-track"><div class="lp-preview-bar-fill" style="width:92%"></div></div></div>
                <div class="lp-preview-bar"><div class="lp-preview-bar-meta"><span>Marketing</span><span>78%</span></div><div class="lp-preview-bar-track"><div class="lp-preview-bar-fill" style="width:78%"></div></div></div>
                <div class="lp-preview-bar"><div class="lp-preview-bar-meta"><span>Finance</span><span>85%</span></div><div class="lp-preview-bar-track"><div class="lp-preview-bar-fill" style="width:85%"></div></div></div>
            </div>
            <div class="lp-preview-card">
                <div class="lp-preview-row"><div class="lp-preview-row-left"><div class="lp-preview-avatar">👤</div><div><span style="font-weight:700;">Budi S.</span><br><span style="font-size:10px;color:#b8a9ff;">Engineering</span></div></div><div class="lp-preview-score">96</div></div>
                <div class="lp-preview-row"><div class="lp-preview-row-left"><div class="lp-preview-avatar">👤</div><div><span style="font-weight:700;">Sari A.</span><br><span style="font-size:10px;color:#b8a9ff;">Marketing</span></div></div><div class="lp-preview-score">88</div></div>
                <div class="lp-preview-row"><div class="lp-preview-row-left"><div class="lp-preview-avatar">👤</div><div><span style="font-weight:700;">Eka R.</span><br><span style="font-size:10px;color:#b8a9ff;">Finance</span></div></div><div class="lp-preview-score">91</div></div>
            </div>
            <div class="lp-preview-card">
                <div class="lp-preview-row"><div class="lp-preview-row-left"><div class="lp-preview-avatar">⭐</div><div><span style="font-weight:700;">Rata-rata KPI</span><br><span style="font-size:10px;color:#b8a9ff;">Semua Departemen</span></div></div><div class="lp-preview-score">85%</div></div>
                <div class="lp-preview-row"><div class="lp-preview-row-left"><div class="lp-preview-avatar">🎯</div><div><span style="font-weight:700;">Target Tercapai</span><br><span style="font-size:10px;color:#b8a9ff;">7 dari 10 dept</span></div></div><div class="lp-preview-score">70%</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # FEATURES
    st.markdown('<span id="features" class="anchor"></span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lp-section-header">
        <h2>Comprehensive <span>Feature Set</span></h2>
        <p>Semua yang Anda butuhkan untuk mengelola dan menganalisis performa karyawan secara menyeluruh.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lp-features">
        <div class="lp-feature-card"><div class="lp-feature-icon">📊</div><div class="lp-feature-title">Monitoring KPI</div><div class="lp-feature-desc">Pantau performa setiap departemen secara real-time dengan visualisasi interaktif.</div></div>
        <div class="lp-feature-card"><div class="lp-feature-icon">👥</div><div class="lp-feature-title">Clustering Karyawan</div><div class="lp-feature-desc">Kelompokkan karyawan berdasarkan karakteristik untuk strategi pengembangan.</div></div>
        <div class="lp-feature-card"><div class="lp-feature-icon">📈</div><div class="lp-feature-title">Forecasting</div><div class="lp-feature-desc">Prediksi performa departemen ke depan untuk perencanaan strategis.</div></div>
        <div class="lp-feature-card"><div class="lp-feature-icon">🤖</div><div class="lp-feature-title">AI Insights</div><div class="lp-feature-desc">Wawasan cerdas dari data HR menggunakan Gemini AI.</div></div>
        <div class="lp-feature-card"><div class="lp-feature-icon">🎯</div><div class="lp-feature-title">Feature Importance</div><div class="lp-feature-desc">Identifikasi faktor terpenting yang mempengaruhi performa karyawan.</div></div>
        <div class="lp-feature-card"><div class="lp-feature-icon">📋</div><div class="lp-feature-title">Ekspor Data</div><div class="lp-feature-desc">Ekspor data mentah untuk analisis lebih lanjut.</div></div>
    </div>
    """, unsafe_allow_html=True)

    # STEPS
    st.markdown('<span id="steps" class="anchor"></span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lp-section-header">
        <h2>Cara <span>Menggunakannya</span></h2>
        <p>Mulai analisis HR Anda dalam 3 langkah mudah.</p>
    </div>
    <div class="lp-steps">
        <div class="lp-step"><div class="lp-step-num">1</div><div class="lp-step-title">Masuk ke Dashboard</div><div class="lp-step-desc">Akses seluruh fitur analitik HR tanpa konfigurasi rumit.</div></div>
        <div class="lp-step"><div class="lp-step-num">2</div><div class="lp-step-title">Pilih Menu Analisis</div><div class="lp-step-desc">Navigasi ke fitur KPI, clustering, forecasting, atau AI insights.</div></div>
        <div class="lp-step"><div class="lp-step-num">3</div><div class="lp-step-title">Ambil Keputusan</div><div class="lp-step-desc">Gunakan insight untuk membuat keputusan HR berbasis data.</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ABOUT
    st.markdown('<span id="about" class="anchor"></span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lp-section-header">
        <h2>Tentang <span>Proyek</span></h2>
        <p>Proyek akhir mata kuliah Data Warehouse yang mengintegrasikan data HR untuk analisis performa karyawan.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e0e7ff, #ede9fe, #fae8ff); margin: 3rem 6%; border-radius: 32px; padding: 3rem; text-align: center; box-shadow: 0 15px 40px rgba(108,92,231,0.15); border: 1px solid rgba(108,92,231,0.1);">
        <div style="display: inline-block; background: linear-gradient(135deg, #6C5CE7, #8B74FF); border-radius: 60px; padding: 8px 24px; margin-bottom: 1.5rem;">
            <span style="font-size: 14px; font-weight: 600; color: white;">✨ Mulai Sekarang</span>
        </div>
        <h3 style="font-size: 34px; font-weight: 800; color: #1e1b4b; margin-bottom: 0.75rem;">Siap Memulai? <span style="background: linear-gradient(135deg, #6C5CE7, #8B74FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Masuk & Rasakan</span></h3>
        <p style="font-size: 16px; color: #4a4a6a; max-width: 500px; margin: 0 auto; line-height: 1.6;">Jelajahi data karyawan Anda, temukan insight tersembunyi, dan buat keputusan HR yang lebih baik.</p>
    </div>
    """, unsafe_allow_html=True)

    # TOMBOL MASUK
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Masuk ke Dashboard", use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()

    # FOOTER
    st.markdown("""
    <div class="lp-footer">
        <div class="lp-footer-content">
            <div class="lp-footer-logo">📊 HR Analytics</div>
            <div class="lp-footer-links">
                <a href="#hero">Beranda</a>
                <a href="#features">Fitur</a>
                <a href="#steps">Cara Kerja</a>
                <a href="#about">Tentang</a>
                <a href="#hero">Kontak</a>
            </div>
        </div>
        <div class="lp-footer-copy">© 2026 HR Analytics Dashboard · Data Warehouse Project</div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ============================================================
# PAGE CONFIG UNTUK DASHBOARD
# ============================================================
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================
if 'menu' not in st.session_state:
    st.session_state.menu = "Dashboard"

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data(ttl=3600)
def load_data():
    files = {
        'cluster_summary': 'data/clustering/cluster_summary.csv',
        'dept_performance': 'data/clustering/dept_performance.csv',
        'forecast_data': 'data/forecasting/forecast_data.csv',
        'dashboard_summary': 'data/dashboard_summary.csv',
        'feature_importance': 'data/clustering/feature_importance.csv',
        'feature_importance_reg': 'data/regression/feature_importance_regression.csv',
        'forecast_metrics': 'data/forecasting/forecasting_metrics.csv'
    }
    
    data = {}
    for name, path in files.items():
        if os.path.exists(path):
            data[name] = pd.read_csv(path)
        else:
            data[name] = None
    return data

data = load_data()

# ============================================================
# HITUNG TOTAL KARYAWAN
# ============================================================
total_employees = 0
if data['dept_performance'] is not None:
    total_employees = int(data['dept_performance']['jumlah_karyawan'].sum())

# ============================================================
# FUNGSI LABEL CLUSTER (HURUF) - UNTUK INTERPRETASI
# ============================================================
def get_cluster_label(kpi_value):
    if kpi_value >= 85:
        return "High Performer"
    elif kpi_value >= 70:
        return "Solid Performer"
    elif kpi_value >= 55:
        return "Average Performer"
    else:
        return "Needs Improvement"

def get_cluster_color(kpi_value):
    if kpi_value >= 85:
        return "#20C997"
    elif kpi_value >= 70:
        return "#6C5CE7"
    elif kpi_value >= 55:
        return "#FD7E14"
    else:
        return "#DC3545"

# ============================================================
# FUNGSI INSIGHT MANUAL DARI DATA (TANPA AI)
# ============================================================
def get_manual_insights():
    insights = []
    
    # Insight 1: Best and worst department
    if data['dept_performance'] is not None:
        df = data['dept_performance']
        best = df.loc[df['avg_kpi'].idxmax()]
        worst = df.loc[df['avg_kpi'].idxmin()]
        insights.append(f"🏆 Departemen dengan performa terbaik adalah {best['departemen']} dengan rata-rata KPI {best['avg_kpi']:.1f} dan achievement {best['pencapaian_%']:.1f}%")
        insights.append(f"⚠️ Departemen yang perlu perhatian khusus adalah {worst['departemen']} dengan rata-rata KPI {worst['avg_kpi']:.1f}")
    
    # Insight 2: Cluster distribution
    if data['cluster_summary'] is not None:
        df_c = data['cluster_summary']
        high = df_c[df_c['avg_kpi'] >= 85]['jumlah_karyawan'].sum() if len(df_c) > 0 else 0
        solid = df_c[(df_c['avg_kpi'] >= 70) & (df_c['avg_kpi'] < 85)]['jumlah_karyawan'].sum() if len(df_c) > 0 else 0
        avg = df_c[(df_c['avg_kpi'] >= 55) & (df_c['avg_kpi'] < 70)]['jumlah_karyawan'].sum() if len(df_c) > 0 else 0
        low = df_c[df_c['avg_kpi'] < 55]['jumlah_karyawan'].sum() if len(df_c) > 0 else 0
        insights.append(f"👥 Distribusi karyawan: {high} High Performer, {solid} Solid Performer, {avg} Average Performer, {low} Needs Improvement")
    
    # Insight 3: Feature importance
    if data['feature_importance'] is not None and len(data['feature_importance']) > 0:
        top = data['feature_importance'].iloc[0]['feature']
        insights.append(f"🎯 Faktor paling berpengaruh terhadap performa karyawan adalah {top}")
    
    # Insight 4: Forecasting accuracy
    if data['forecast_metrics'] is not None and len(data['forecast_metrics']) > 0:
        best_f = data['forecast_metrics'].loc[data['forecast_metrics']['MAPE'].idxmin()]
        insights.append(f"📈 Departemen dengan prediksi paling akurat adalah {best_f['departemen']} (MAPE: {best_f['MAPE']:.1f}%)")
    
    # Insight 5: Overall average
    if data['dept_performance'] is not None:
        avg_kpi = data['dept_performance']['avg_kpi'].mean()
        avg_ach = data['dept_performance']['pencapaian_%'].mean()
        insights.append(f"📊 Rata-rata KPI seluruh departemen: {avg_kpi:.1f} dengan achievement {avg_ach:.1f}%")
    
    return insights

# ============================================================
# CUSTOM CSS - DIPERBESAR
# ============================================================
st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    
    .stApp {
        background: linear-gradient(135deg, #f5f0ff 0%, #e8e0ff 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6C5CE7 0%, #5B4BCF 100%);
        border-radius: 0 20px 20px 0;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-logo-icon {
        font-size: 48px;
        color: white;
        margin-bottom: 12px;
    }
    
    .sidebar-title {
        font-size: 22px;
        font-weight: 800;
        color: white;
        margin-top: 8px;
    }
    
    .sidebar-subtitle {
        font-size: 13px;
        color: rgba(255,255,255,0.6);
    }
    
    /* METRIC CARDS */
    .metric-card {
        background: white;
        border-radius: 28px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        min-height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(108,92,231,0.15);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(108,92,231,0.15);
    }
    
    .metric-icon {
        font-size: 38px;
        color: #6C5CE7;
        margin-bottom: 10px;
    }
    
    .metric-value {
        font-size: 38px;
        font-weight: 800;
        color: #1a1a2e;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 14px;
        color: #6c5ce7;
        margin-top: 8px;
        font-weight: 600;
    }
    
    /* CHART CARDS - SEMUA UNGU */
    .chart-card {
        background: linear-gradient(135deg, #6C5CE7 0%, #8B74FF 100%);
        border-radius: 28px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: none;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .chart-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(108,92,231,0.3);
    }
    
    /* HEADER CARD */
    .chart-header {
        background: rgba(255,255,255,0.08);
        padding: 16px 24px;
        border-bottom: 1px solid rgba(255,255,255,0.15);
    }
    
    .chart-title {
        font-size: 18px;
        font-weight: 700;
        color: white !important;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .chart-title i {
        color: white;
        font-size: 20px;
    }
    
    /* BODY CARD */
    .chart-body {
        padding: 1.5rem;
        background: transparent;
    }
    
    /* WELCOME HEADER */
    .welcome-header {
        background: linear-gradient(135deg, #6C5CE7 0%, #8B74FF 100%);
        border-radius: 28px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.8rem;
        color: white;
    }
    
    .welcome-title {
        font-size: 32px !important;
        font-weight: 800 !important;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .welcome-title i {
        font-size: 36px !important;
    }
    
    .welcome-subtitle {
        font-size: 18px !important;
        opacity: 0.95;
        margin-top: 10px;
    }
    
    .welcome-date {
        font-size: 15px !important;
        opacity: 0.8;
        margin-top: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .welcome-date i {
        font-size: 15px !important;
    }
    
    /* INSIGHT CARD */
    .insight-card {
        background: linear-gradient(135deg, #f0ecff 0%, #e8e0ff 100%);
        border-radius: 24px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        border-left: 5px solid #6C5CE7;
        font-size: 14px;
        color: #2d2d3f;
    }
    
    .insight-card i {
        color: #6C5CE7;
        margin-right: 10px;
        font-size: 16px;
    }
    
    /* PAGE INFO BOX */
    .page-info {
        background: white;
        border-radius: 24px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.8rem;
        border-left: 5px solid #6C5CE7;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .page-info-title {
        font-size: 20px;
        font-weight: 700;
        color: #6C5CE7;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .page-info-title i {
        color: #6C5CE7;
        font-size: 24px;
    }
    
    .page-info-desc {
        font-size: 16px;
        color: #4a4a6a;
        line-height: 1.6;
    }
    
    /* INTERPRETASI BOX */
    .interpretasi-box {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #6C5CE7;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .interpretasi-box h4 {
        color: #6C5CE7;
        margin: 0 0 12px 0;
        font-size: 18px;
    }
    
    .interpretasi-box p {
        color: #4a4a6a;
        font-size: 15px;
        line-height: 1.6;
        margin: 0;
    }
    
    /* PLOTLY CHARTS */
    .js-plotly-plot, .plotly, .plot-container {
        border-radius: 20px !important;
        overflow: hidden !important;
        background: white !important;
    }
    
    /* DATAFRAME */
    .stDataFrame, .stDataFrame > div, .dataframe {
        border-radius: 20px !important;
        overflow: hidden !important;
        background: white !important;
    }
    
    /* EXPANDER */
    .stExpander, .stExpander > div, .streamlit-expanderHeader {
        border-radius: 20px !important;
        overflow: hidden !important;
        background: rgba(108,92,231,0.08) !important;
        color: #1a1a2e !important;
    }
    
    /* TABS */
    .stTabs, .stTabs [data-baseweb="tab-list"] {
        border-radius: 40px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 32px !important;
        color: #4a4a6a !important;
        font-size: 14px !important;
        padding: 8px 24px !important;
        background: rgba(108,92,231,0.1) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #6C5CE7 !important;
        color: white !important;
    }
    
    /* SELECTBOX */
    .stSelectbox > div > div, .stSelectbox input {
        border-radius: 16px !important;
        font-size: 14px !important;
    }
    
    /* BUTTONS */
    .stButton button {
        border-radius: 40px !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
    }
    
    /* FOOTER */
    .footer {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        color: rgba(0,0,0,0.35);
        font-size: 12px;
        border-top: 1px solid rgba(108,92,231,0.15);
        margin-top: 1.5rem;
    }
    
    /* SIDEBAR TEXT COLOR */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox label {
        color: white !important;
        font-size: 14px !important;
    }
    
    [data-testid="stSidebar"] .stCaption {
        color: rgba(255,255,255,0.6) !important;
        font-size: 12px !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2) !important;
    }
    
    /* DATAFRAME FIX */
    .dataframe {
        width: 100% !important;
    }
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* SIDEBAR MENU BUTTON - RATA KIRI (FINAL) */
    [data-testid="stSidebar"] .stButton button {
        text-align: left !important;
        justify-content: flex-start !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        width: 100% !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        background: rgba(255,255,255,0.12) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.25) !important;
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .stButton button:active,
    [data-testid="stSidebar"] .stButton button:focus {
        background: rgba(255,255,255,0.3) !important;
        outline: none !important;
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: rgba(255,255,255,0.3) !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo-icon">
            <i class="fas fa-chart-line"></i>
        </div>
        <div class="sidebar-title">HR Analytics</div>
        <div class="sidebar-subtitle">Performance Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    menu_items = [
        {"emoji": "📊", "name": "Dashboard"},
        {"emoji": "👥", "name": "Clustering"},
        {"emoji": "📈", "name": "Forecasting"},
        {"emoji": "🎯", "name": "Feature Importance"},
        {"emoji": "📋", "name": "Data Tables"},
        {"emoji": "📚", "name": "Knowledge Base"}
    ]
    
    for item in menu_items:
        is_active = st.session_state.menu == item["name"]
        
        if st.button(
            f"{item['emoji']}  {item['name']}",
            key=f"menu_{item['name']}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.menu = item["name"]
            st.rerun()
    
    st.markdown("---")
    
    show_ai = False
    st.markdown('<div style="color: white; background: rgba(255,255,255,0.15); padding: 10px 14px; border-radius: 10px; font-size: 14px;">⚙️ Insight berbasis data</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2026 HR Analytics")
    st.caption("Data Warehouse Project")

menu = st.session_state.menu

# ============================================================
# FUNCTION TO SHOW PAGE INFO
# ============================================================
def show_page_info(title, description, icon):
    st.markdown(f"""
    <div class="page-info">
        <div class="page-info-title">
            <i class="fas {icon}"></i>
            <span>Apa itu halaman {title}?</span>
        </div>
        <div class="page-info-desc">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD PAGE
# ============================================================
if menu == "Dashboard":
    now = datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")
    
    st.markdown(f"""
    <div class="welcome-header">
        <div class="welcome-title">
            <i class="fas fa-user-circle"></i>
            <span>Halo, Admin!</span>
        </div>
        <div class="welcome-subtitle">
            Selamat datang di HR Analytics Dashboard
        </div>
        <div class="welcome-date">
            <i class="fas fa-calendar-day"></i>
            <span>{formatted_date}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if data['dashboard_summary'] is not None:
        summary = data['dashboard_summary'].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon"><i class="fas fa-users"></i></div>
                <div class="metric-value">{int(summary['total_employees'])}</div>
                <div class="metric-label">Total Employees</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon"><i class="fas fa-folder-open"></i></div>
                <div class="metric-value">{int(summary['total_projects'])}</div>
                <div class="metric-label">Total Projects</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon"><i class="fas fa-chart-pie"></i></div>
                <div class="metric-value">{int(summary['clusters_used'])}</div>
                <div class="metric-label">Clusters</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon"><i class="fas fa-chart-line"></i></div>
                <div class="metric-value">{summary['regression_r2']:.1%}</div>
                <div class="metric-label">R² Score</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================================
    # MANUAL INSIGHTS - GABUNGAN DALAM SATU CARD RAPI
    # ============================================================
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <i class="fas fa-chart-line"></i>
                <span>Insights & Rekomendasi</span>
            </div>
        </div>
        <div class="chart-body">
    """, unsafe_allow_html=True)
    
    if data['dept_performance'] is not None:
        df = data['dept_performance']
        best = df.loc[df['avg_kpi'].idxmax()]
        worst = df.loc[df['avg_kpi'].idxmin()]
        
        # Hitung distribusi cluster
        high_count = 0
        solid_count = 0
        avg_count = 0
        low_count = 0
        
        if data['cluster_summary'] is not None:
            df_c = data['cluster_summary']
            high_count = int(df_c[df_c['avg_kpi'] >= 85]['jumlah_karyawan'].sum()) if len(df_c) > 0 else 0
            solid_count = int(df_c[(df_c['avg_kpi'] >= 70) & (df_c['avg_kpi'] < 85)]['jumlah_karyawan'].sum()) if len(df_c) > 0 else 0
            avg_count = int(df_c[(df_c['avg_kpi'] >= 55) & (df_c['avg_kpi'] < 70)]['jumlah_karyawan'].sum()) if len(df_c) > 0 else 0
            low_count = int(df_c[df_c['avg_kpi'] < 55]['jumlah_karyawan'].sum()) if len(df_c) > 0 else 0
        
        # Dapatkan feature importance top
        top_feature = "level_jabatan"
        if data['feature_importance'] is not None and len(data['feature_importance']) > 0:
            top_feature = data['feature_importance'].iloc[0]['feature']
        
        # Dapatkan best forecast
        best_forecast = "-"
        best_mape = "-"
        if data['forecast_metrics'] is not None and len(data['forecast_metrics']) > 0:
            best_f = data['forecast_metrics'].loc[data['forecast_metrics']['MAPE'].idxmin()]
            best_forecast = best_f['departemen']
            best_mape = f"{best_f['MAPE']:.1f}%"
        
        # Rata-rata
        avg_kpi = df['avg_kpi'].mean()
        avg_ach = df['pencapaian_%'].mean()
        
        # Tampilkan dalam grid 2 kolom
        col1_insight, col2_insight = st.columns(2)
        
        with col1_insight:
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #20C997;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <i class="fas fa-trophy" style="color: #20C997; font-size: 20px;"></i>
                    <span style="font-weight: 700; color: #333;">Departemen Terbaik</span>
                </div>
                <div style="font-size: 18px; font-weight: 800; color: #20C997;">{best['departemen']}</div>
                <div style="font-size: 13px; color: #666;">KPI: {best['avg_kpi']:.1f} | Achievement: {best['pencapaian_%']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #DC3545;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <i class="fas fa-exclamation-triangle" style="color: #DC3545; font-size: 20px;"></i>
                    <span style="font-weight: 700; color: #333;">Perlu Perhatian</span>
                </div>
                <div style="font-size: 18px; font-weight: 800; color: #DC3545;">{worst['departemen']}</div>
                <div style="font-size: 13px; color: #666;">KPI: {worst['avg_kpi']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #FD7E14;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <i class="fas fa-chart-line" style="color: #FD7E14; font-size: 20px;"></i>
                    <span style="font-weight: 700; color: #333;">Rata-rata Keseluruhan</span>
                </div>
                <div style="font-size: 14px; color: #333;">KPI: <strong>{avg_kpi:.1f}</strong> | Achievement: <strong>{avg_ach:.1f}%</strong></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2_insight:
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #6C5CE7;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <i class="fas fa-users" style="color: #6C5CE7; font-size: 20px;"></i>
                    <span style="font-weight: 700; color: #333;">Distribusi Karyawan</span>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px;">
                    <div><span style="color: #20C997;">●</span> High: <strong>{high_count}</strong></div>
                    <div><span style="color: #6C5CE7;">●</span> Solid: <strong>{solid_count}</strong></div>
                    <div><span style="color: #FD7E14;">●</span> Average: <strong>{avg_count}</strong></div>
                    <div><span style="color: #DC3545;">●</span> Needs: <strong>{low_count}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #6C5CE7;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <i class="fas fa-chart-bar" style="color: #6C5CE7; font-size: 20px;"></i>
                    <span style="font-weight: 700; color: #333;">Faktor Paling Berpengaruh</span>
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #6C5CE7;">{top_feature}</div>
                <div style="font-size: 12px; color: #666;">Fitur ini paling menentukan performa karyawan</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #20C997;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <i class="fas fa-chart-line" style="color: #20C997; font-size: 20px;"></i>
                    <span style="font-weight: 700; color: #333;">Forecast Paling Akurat</span>
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #20C997;">{best_forecast}</div>
                <div style="font-size: 12px; color: #666;">MAPE: {best_mape} (sangat akurat)</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

        # ============================================================
    # BUBBLE CHART & PIE CHART - SIDE BY SIDE
    # ============================================================
    
    col1, col2 = st.columns(2)
    
    # ========== KOLOM KIRI - BUBBLE CHART ==========
    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-chart-line"></i>
                    <span>Department Performance</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)
        
        if data['dept_performance'] is not None:
            df = data['dept_performance'].copy().sort_values('avg_kpi', ascending=False)
            
            fig = px.scatter(
                df, 
                x='avg_kpi', 
                y='pencapaian_%', 
                size='jumlah_karyawan',
                size_max=50,
                color='departemen',
                hover_name='departemen',
                labels={
                    'avg_kpi': 'Rata-rata KPI',
                    'pencapaian_%': 'Pencapaian Target (%)',
                }
            )
            
            fig.update_traces(
                textposition=None,
                marker=dict(line=dict(width=1, color='white')),
                showlegend=False
            )
            
            fig.update_layout(
                height=400,
                xaxis=dict(title="Rata-rata KPI", range=[40, 100]),
                yaxis=dict(title="Pencapaian Target (%)", range=[40, 130]),
                margin=dict(l=10, r=10, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(245,245,245,0.5)'
            )
            
            fig.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
            st.caption("💡 Hover ke bubble untuk lihat nama departemen | Ukuran bubble = jumlah karyawan")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ========== KOLOM KANAN - PIE CHART ==========
    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-chart-pie"></i>
                    <span>Employee Distribution</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)
        
        if data['cluster_summary'] is not None:
            df_c = data['cluster_summary'].copy()
            df_c['Kategori'] = df_c['avg_kpi'].apply(get_cluster_label)
            df_c = df_c[df_c['jumlah_karyawan'] > 0]
            
            if len(df_c) > 0:
                fig = px.pie(
                    df_c, 
                    values='jumlah_karyawan', 
                    names='Kategori',
                    hole=0.4, 
                    color='Kategori',
                    color_discrete_map={
                        'High Performer': '#10B981',
                        'Solid Performer': '#8B5CF6',
                        'Average Performer': '#F59E0B',
                        'Needs Improvement': '#EF4444'
                    }
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(255,255,255,0.9)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("💡 Kategori berdasarkan rata-rata KPI karyawan")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ============================================================
    # FORECASTING CHART - Actual vs Predicted (DIPERBAIKI)
    # ============================================================
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <i class="fas fa-chart-line"></i>
                <span>KPI Forecast: Actual vs Predicted</span>
            </div>
        </div>
        <div class="chart-body">
    """, unsafe_allow_html=True)
    
    if data['forecast_data'] is not None:
        df_fore = data['forecast_data'].copy()
        depts = df_fore['department_name'].unique().tolist()
        selected_dept = st.selectbox("Pilih Departemen untuk Forecast Detail", depts)
        
        df_dept = df_fore[df_fore['department_name'] == selected_dept].copy()
        df_dept['periode'] = pd.to_datetime(df_dept['periode'])
        df_dept = df_dept.sort_values('periode').reset_index(drop=True)
        
        # Split data: actual (historical) dan forecast (future)
        n = len(df_dept)
        n_train = max(6, n - 6) if n > 10 else n
        
        df_actual = df_dept.iloc[:n_train].copy()
        df_forecast = df_dept.iloc[n_train:].copy() if n_train < n else pd.DataFrame()
        
        fig = go.Figure()
        
        # Actual data (hijau)
        fig.add_trace(go.Scatter(
            x=df_actual['periode'],
            y=df_actual['avg_kpi'],
            mode='lines+markers',
            name='Aktual (Data Historis)',
            line=dict(color='#20C997', width=3),
            marker=dict(size=8, color='#20C997', symbol='circle', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x|%b %Y}</b><br>KPI Aktual: %{y:.1f}<extra></extra>'
        ))
        
        # Forecast data (oranye)
        if len(df_forecast) > 0:
            fig.add_trace(go.Scatter(
                x=df_forecast['periode'],
                y=df_forecast['avg_kpi'],
                mode='lines+markers',
                name='Forecast (Prediksi)',
                line=dict(color='#FD7E14', width=3, dash='dot'),
                marker=dict(size=8, color='#FD7E14', symbol='diamond', line=dict(width=2, color='white')),
                hovertemplate='<b>%{x|%b %Y}</b><br>KPI Prediksi: %{y:.1f}<extra></extra>'
            ))
            
            # Garis pemisah antara aktual dan forecast
            sep_date = df_actual['periode'].iloc[-1]
            fig.add_shape(
                type='line', x0=sep_date, x1=sep_date, y0=40, y1=100,
                line=dict(color='#667eea', width=2, dash='dash')
            )
            fig.add_annotation(
                x=sep_date, y=100, text="⏰ Forecast Mulai", showarrow=False,
                font=dict(size=11, color='#667eea'), bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#667eea', borderwidth=1, borderpad=4
            )
        
        # Tambahkan metrik MAPE jika tersedia
        if data['forecast_metrics'] is not None:
            dept_metrics = data['forecast_metrics'][data['forecast_metrics']['departemen'] == selected_dept]
            if len(dept_metrics) > 0:
                fig.add_annotation(
                    x=0.02, y=0.98, xref="paper", yref="paper",
                    text=f"📊 MAPE: {dept_metrics.iloc[0]['MAPE']:.1f}% | MAE: {dept_metrics.iloc[0]['MAE']:.1f}",
                    showarrow=False, font=dict(size=11, color='#666'),
                    bgcolor='rgba(255,255,255,0.9)', bordercolor='#667eea', borderwidth=1, borderpad=4
                )
        
        fig.update_layout(
            height=400,
            title=f"Trend KPI & Forecast - {selected_dept}",
            xaxis_title="Periode", yaxis_title="Rata-rata KPI",
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(245,245,245,0.5)',
            yaxis=dict(range=[40, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrik tambahan
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Rata-rata Historis", f"{df_actual['avg_kpi'].mean():.1f}")
        with col2:
            if len(df_forecast) > 0:
                st.metric("📈 Rata-rata Forecast", f"{df_forecast['avg_kpi'].mean():.1f}")
            else:
                st.metric("📈 Rata-rata Forecast", "-")
        with col3:
            st.metric("🎯 Nilai Terakhir", f"{df_actual['avg_kpi'].iloc[-1]:.1f}")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ============================================================
    # RANKINGS DAN KEY INSIGHTS (TETAP SAMA)
    # ============================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-trophy"></i>
                    <span>Department Rankings</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)
        
        if data['dept_performance'] is not None:
            df_rank = data['dept_performance'].copy().sort_values('avg_kpi', ascending=False).reset_index(drop=True)
            df_rank.index = df_rank.index + 1
            st.dataframe(
                df_rank[['departemen', 'avg_kpi', 'pencapaian_%', 'jumlah_karyawan']],
                column_config={
                    'departemen': 'Departemen',
                    'avg_kpi': st.column_config.NumberColumn('Avg KPI', format="%.1f"),
                    'pencapaian_%': st.column_config.NumberColumn('Achievement', format="%.1f%%"),
                    'jumlah_karyawan': 'Jumlah Karyawan'
                },
                use_container_width=True,
                hide_index=False
            )
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-lightbulb"></i>
                    <span>Key Insights</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        if data['dept_performance'] is not None:
            df = data['dept_performance']
            best = df.loc[df['avg_kpi'].idxmax()]
            worst = df.loc[df['avg_kpi'].idxmin()]
            
            st.markdown(f"""
            <div style="background: white; border-radius: 20px; padding: 18px 20px; margin-bottom: 15px; border: 1px solid #e8e0ff;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 14px; color: #8B74FF; margin-bottom: 5px;">🏆 TERBAIK</div>
                        <div style="font-size: 24px; font-weight: 800; color: #6C5CE7;">{best['departemen']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 32px; font-weight: 800; color: #6C5CE7;">{best['avg_kpi']:.1f}</div>
                        <div style="font-size: 12px; color: #8B74FF;">KPI Score</div>
                    </div>
                </div>
                <div style="margin-top: 12px; background: #f0ecff; border-radius: 14px; padding: 10px 15px; text-align: center;">
                    <span style="font-size: 14px;">🎯 Achievement: </span>
                    <span style="font-size: 20px; font-weight: 700; color: #6C5CE7;">{best['pencapaian_%']:.1f}%</span>
                </div>
            </div>
            
            <div style="background: white; border-radius: 20px; padding: 18px 20px; margin-bottom: 15px; border: 1px solid #e8e0ff;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 14px; color: #8B74FF; margin-bottom: 5px;">⚠️ PERLU DITINGKATKAN</div>
                        <div style="font-size: 24px; font-weight: 800; color: #6C5CE7;">{worst['departemen']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 32px; font-weight: 800; color: #6C5CE7;">{worst['avg_kpi']:.1f}</div>
                        <div style="font-size: 12px; color: #8B74FF;">KPI Score</div>
                    </div>
                </div>
            </div>
            
            <div style="background: linear-gradient(135deg, #6C5CE7, #8B74FF); border-radius: 20px; padding: 18px 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 14px; color: rgba(255,255,255,0.85); margin-bottom: 5px;">📊 RATA-RATA ACHIEVEMENT</div>
                        <div style="font-size: 32px; font-weight: 800; color: white;">{df['pencapaian_%'].mean():.1f}%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.2); width: 55px; height: 55px; border-radius: 16px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 28px;">📈</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)


# ============================================================
# CLUSTERING PAGE - FINAL VERSION
# ============================================================
elif menu == "Clustering":
    show_page_info(
        "Clustering",
        "Halaman ini menampilkan hasil pengelompokan (clustering) karyawan berdasarkan karakteristik seperti performa, proyek, dan metrik lainnya. "
        "Cluster membantu Anda memahami pola dan mengelompokkan karyawan dengan sifat serupa untuk strategi yang lebih tepat sasaran.",
        "fa-layer-group"
    )
    
    if data['cluster_summary'] is not None:
        df_c = data['cluster_summary'].copy()
        df_c['Kategori'] = df_c['avg_kpi'].apply(get_cluster_label)
        
        # ========== CHART SECTION ==========
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-chart-bar"></i>
                    <span>Jumlah Karyawan per Kategori Performa</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            category_order = ['High Performer', 'Solid Performer', 'Average Performer', 'Needs Improvement']
            fig = px.bar(
                df_c, 
                x='Kategori', 
                y='jumlah_karyawan', 
                text='jumlah_karyawan',
                color='Kategori',
                color_discrete_map={
                    'High Performer': '#10B981',
                    'Solid Performer': '#8B5CF6',
                    'Average Performer': '#F59E0B',
                    'Needs Improvement': '#EF4444'
                },
                category_orders={'Kategori': category_order},
                title="&#x1F4CA; Jumlah Karyawan per Kategori"
            )
            fig.update_traces(textposition='outside', textfont=dict(size=12))
            fig.update_layout(
                height=450,
                xaxis_title="Kategori Performa",
                yaxis_title="Jumlah Karyawan",
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(245,245,245,0.5)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; border-radius: 16px; padding: 20px; border: 2px solid #667eea; 
                        box-shadow: 0 4px 12px rgba(102,126,234,0.15); min-height: 450px;">
                <h4 style="color: #667eea; margin-top: 0; margin-bottom: 20px; font-size: 18px;">
                    &#x1F4CB; Interpretasi Kategori
                </h4>
                <div style="background: #f0fdf4; border-radius: 12px; padding: 12px; margin-bottom: 12px; border-left: 4px solid #10B981;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span style="font-size: 18px;">&#x1F31F;</span>
                        <strong style="color: #10B981;">High Performer (KPI &#8805; 85)</strong>
                    </div>
                    <div style="font-size: 13px; color: #555; margin-left: 28px;">
                        Karyawan dengan performa terbaik, target strategis untuk retention &amp; leadership
                    </div>
                </div>
                <div style="background: #f5f3ff; border-radius: 12px; padding: 12px; margin-bottom: 12px; border-left: 4px solid #8B5CF6;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span style="font-size: 18px;">&#x1F4CA;</span>
                        <strong style="color: #8B5CF6;">Solid Performer (KPI 70&#8211;84)</strong>
                    </div>
                    <div style="font-size: 13px; color: #555; margin-left: 28px;">
                        Karyawan andal dengan performa konsisten
                    </div>
                </div>
                <div style="background: #fffbeb; border-radius: 12px; padding: 12px; margin-bottom: 12px; border-left: 4px solid #F59E0B;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span style="font-size: 18px;">&#x1F4C8;</span>
                        <strong style="color: #F59E0B;">Average Performer (KPI 55&#8211;69)</strong>
                    </div>
                    <div style="font-size: 13px; color: #555; margin-left: 28px;">
                        Karyawan dengan performa standar, butuh pengembangan
                    </div>
                </div>
                <div style="background: #fef2f2; border-radius: 12px; padding: 12px; border-left: 4px solid #EF4444;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span style="font-size: 18px;">&#x26A0;&#xFE0F;</span>
                        <strong style="color: #EF4444;">Needs Improvement (KPI &lt; 55)</strong>
                    </div>
                    <div style="font-size: 13px; color: #555; margin-left: 28px;">
                        Karyawan yang perlu pembinaan dan pelatihan intensif
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # ========== DATA SUMMARY SECTION ==========
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-table"></i>
                    <span>Data Summary Cluster</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)
        
        display_df = df_c[['Kategori', 'avg_kpi', 'pencapaian', 'rata_masa_kerja', 'jumlah_karyawan']].copy()
        display_df.columns = ['Kategori Performa', 'Rata-rata KPI', 'Pencapaian (%)', 'Rata Masa Kerja (thn)', 'Jumlah Karyawan']
        
        st.dataframe(
            display_df,
            column_config={
                'Kategori Performa': st.column_config.TextColumn(width='medium'),
                'Rata-rata KPI': st.column_config.NumberColumn(format="%.2f", width='small'),
                'Pencapaian (%)': st.column_config.NumberColumn(format="%.2f%%", width='small'),
                'Rata Masa Kerja (thn)': st.column_config.NumberColumn(format="%.2f", width='small'),
                'Jumlah Karyawan': st.column_config.NumberColumn(format="%d", width='small'),
            },
            use_container_width=True,
            hide_index=True
        )
        
        total_karyawan = int(display_df['Jumlah Karyawan'].sum())
        high_performer = int(display_df[display_df['Kategori Performa'] == 'High Performer']['Jumlah Karyawan'].sum()) if len(display_df[display_df['Kategori Performa'] == 'High Performer']) > 0 else 0
        need_improve = int(display_df[display_df['Kategori Performa'] == 'Needs Improvement']['Jumlah Karyawan'].sum()) if len(display_df[display_df['Kategori Performa'] == 'Needs Improvement']) > 0 else 0
        
        st.markdown(f"""
        <div style="background: #f0f4ff; border-radius: 12px; padding: 12px 16px; margin-top: 16px;">
            <span style="font-size: 13px; color: #555;">&#x1F4A1; <strong>Insight:</strong> Dari <strong>{total_karyawan}</strong> karyawan, 
            terdapat <strong>{high_performer}</strong> karyawan High Performer (perlu dipersiapkan untuk program leadership) 
            dan <strong>{need_improve}</strong> karyawan Needs Improvement (perlu pembinaan intensif).</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    else:
        st.info("Data cluster summary tidak tersedia")


# ============================================================
# FORECASTING PAGE - ACTUAL VS PREDICTED (DIPERBAIKI)
# ============================================================
elif menu == "Forecasting":
    show_page_info(
        "Forecasting",
        "Halaman ini menampilkan prediksi (forecasting) KPI setiap departemen untuk periode mendatang. "
        "Grafik menampilkan data aktual (hijau) dan prediksi forecast (oranye) dengan garis pemisah yang jelas.",
        "fa-chart-line"
    )

    if data['forecast_data'] is not None:
        departments = sorted(data['forecast_data']['department_name'].unique())

        # ========== DEPARTMENT SELECTOR ==========
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-building"></i>
                    <span>Pilih Departemen</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        selected_dept = st.selectbox("", departments, label_visibility="collapsed")

        # ========== MAPE METRIC CARD ==========
        if data['forecast_metrics'] is not None:
            dept_metrics = data['forecast_metrics'][data['forecast_metrics']['departemen'] == selected_dept]
            if len(dept_metrics) > 0:
                mape_val = dept_metrics.iloc[0]['MAPE']
                is_good = mape_val < 10
                mape_color = "#10B981" if is_good else "#F59E0B"
                mape_label = "Sangat Baik" if mape_val < 5 else ("Baik" if mape_val < 10 else "Perlu Improvement")
                mape_icon = "&#x2705;" if is_good else "&#x26A0;&#xFE0F;"

                st.markdown(f"""
                <div style="display: flex; gap: 16px; margin: 8px 0 4px 0;">
                    <div style="background: white; border-radius: 14px; padding: 16px 24px; border: 2px solid {mape_color};
                                box-shadow: 0 4px 12px rgba(0,0,0,0.06); display: flex; align-items: center; gap: 16px; flex: 1;">
                        <div style="background: {'#f0fdf4' if is_good else '#fffbeb'}; border-radius: 10px; padding: 12px; font-size: 24px;">
                            {mape_icon}
                        </div>
                        <div>
                            <div style="font-size: 12px; color: #888; margin-bottom: 2px;">Akurasi Forecast (MAPE)</div>
                            <div style="font-size: 28px; font-weight: 700; color: {mape_color}; line-height: 1;">{mape_val:.1f}%</div>
                            <div style="font-size: 12px; color: {mape_color}; margin-top: 2px; font-weight: 600;">{mape_label}</div>
                        </div>
                        <div style="margin-left: auto; font-size: 12px; color: #aaa; text-align: right; line-height: 1.6;">
                            MAPE &lt; 5% &#x2192; Sangat Baik<br>
                            MAPE &lt; 10% &#x2192; Baik<br>
                            MAPE &#x2265; 10% &#x2192; Perlu Improvement
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)

        # ========== CHART ==========
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-chart-line"></i>
                    <span>KPI Forecasting: Actual vs Predicted</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        df_dept = data['forecast_data'][data['forecast_data']['department_name'] == selected_dept].copy()
        df_dept['periode'] = pd.to_datetime(df_dept['periode'])
        df_dept = df_dept.sort_values('periode').reset_index(drop=True)

        n = len(df_dept)
        n_train = max(6, n - 6) if n > 10 else n

        df_actual = df_dept.iloc[:n_train].copy()
        df_forecast = df_dept.iloc[n_train:].copy() if n_train < n else pd.DataFrame()

        fig = go.Figure()

        # Area fill aktual
        fig.add_trace(go.Scatter(
            x=df_actual['periode'], y=df_actual['avg_kpi'],
            fill='tozeroy', fillcolor='rgba(32,201,151,0.08)',
            mode='none', showlegend=False, hoverinfo='skip'
        ))

        # Garis aktual
        fig.add_trace(go.Scatter(
            x=df_actual['periode'], y=df_actual['avg_kpi'],
            mode='lines+markers', name='Aktual (Data Historis)',
            line=dict(color='#20C997', width=3),
            marker=dict(size=7, color='#20C997', symbol='circle', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x|%b %Y}</b><br>KPI Aktual: <b>%{y:.1f}</b><extra></extra>'
        ))

        if len(df_forecast) > 0:
            # Sambungkan titik terakhir aktual ke forecast
            connect_x = [df_actual['periode'].iloc[-1]] + list(df_forecast['periode'])
            connect_y = [df_actual['avg_kpi'].iloc[-1]] + list(df_forecast['avg_kpi'])

            # Area fill forecast
            fig.add_trace(go.Scatter(
                x=connect_x, y=connect_y,
                fill='tozeroy', fillcolor='rgba(253,126,20,0.06)',
                mode='none', showlegend=False, hoverinfo='skip'
            ))

            # Garis forecast
            fig.add_trace(go.Scatter(
                x=df_forecast['periode'], y=df_forecast['avg_kpi'],
                mode='lines+markers', name='Forecast (Prediksi)',
                line=dict(color='#FD7E14', width=3, dash='dot'),
                marker=dict(size=7, color='#FD7E14', symbol='diamond', line=dict(width=2, color='white')),
                hovertemplate='<b>%{x|%b %Y}</b><br>KPI Prediksi: <b>%{y:.1f}</b><extra></extra>'
            ))

            # Garis pemisah
            sep_date = df_actual['periode'].iloc[-1]
            fig.add_shape(
                type='line', x0=sep_date, x1=sep_date, y0=40, y1=100,
                line=dict(color='#667eea', width=2, dash='dash')
            )
            fig.add_annotation(
                x=sep_date, y=98,
                text="&#x25C4; Historis &nbsp;|&nbsp; Forecast &#x25BA;",
                showarrow=False,
                font=dict(size=11, color='#667eea'),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#667eea',
                borderwidth=1,
                borderpad=4
            )

        fig.update_layout(
            height=420,
            xaxis_title="Periode",
            yaxis_title="Rata-rata KPI",
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
                bgcolor='rgba(255,255,255,0.8)', bordercolor='#e5e7eb', borderwidth=1
            ),
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(245,245,245,0.4)',
            yaxis=dict(range=[40, 105], gridcolor='rgba(0,0,0,0.06)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
            margin=dict(t=50, b=40, l=50, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ========== METRIC CARDS ==========
        avg_hist = df_actual['avg_kpi'].mean()
        avg_fore = df_forecast['avg_kpi'].mean() if len(df_forecast) > 0 else None
        last_val = df_actual['avg_kpi'].iloc[-1]
        trend = avg_fore - avg_hist if avg_fore else None

        col1, col2, col3, col4 = st.columns(4)

        def metric_card(label, value, icon, color, suffix="", delta=None):
            delta_html = ""
            if delta is not None:
                arrow = "&#x2191;" if delta >= 0 else "&#x2193;"
                d_color = "#10B981" if delta >= 0 else "#EF4444"
                delta_html = f'<div style="font-size:12px; color:{d_color}; margin-top:2px;">{arrow} {abs(delta):.1f} vs historis</div>'
            return f"""
            <div style="background:white; border-radius:14px; padding:16px; border-top:4px solid {color};
                        box-shadow:0 2px 8px rgba(0,0,0,0.06); text-align:center;">
                <div style="font-size:22px; margin-bottom:6px;">{icon}</div>
                <div style="font-size:11px; color:#888; margin-bottom:4px;">{label}</div>
                <div style="font-size:26px; font-weight:700; color:{color};">{value}{suffix}</div>
                {delta_html}
            </div>"""

        with col1:
            st.markdown(metric_card("Rata-rata Historis", f"{avg_hist:.1f}", "&#x1F4CA;", "#20C997"), unsafe_allow_html=True)
        with col2:
            val = f"{avg_fore:.1f}" if avg_fore else "-"
            st.markdown(metric_card("Rata-rata Forecast", val, "&#x1F52E;", "#FD7E14", delta=trend), unsafe_allow_html=True)
        with col3:
            st.markdown(metric_card("Nilai Terakhir Aktual", f"{last_val:.1f}", "&#x1F3AF;", "#667eea"), unsafe_allow_html=True)
        with col4:
            total_pts = len(df_forecast) if len(df_forecast) > 0 else 0
            st.markdown(metric_card("Periode Diprediksi", str(total_pts), "&#x1F4C5;", "#8B5CF6", suffix=" bln"), unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)

        # ========== DETAIL DATA ==========
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-table"></i>
                    <span>Detail Data</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        df_show = df_dept.copy()
        df_show['periode'] = df_show['periode'].dt.strftime('%b %Y')
        df_show['Tipe'] = ['Aktual'] * n_train + ['Forecast'] * (n - n_train)
        df_show['avg_kpi'] = df_show['avg_kpi'].round(2)
        df_show.columns = ['Departemen', 'Periode', 'Rata-rata KPI', 'Tipe']

        st.dataframe(
            df_show[['Periode', 'Rata-rata KPI', 'Tipe']],
            column_config={
                'Periode': st.column_config.TextColumn(width='medium'),
                'Rata-rata KPI': st.column_config.NumberColumn(format="%.2f", width='medium'),
                'Tipe': st.column_config.TextColumn(width='small'),
            },
            use_container_width=True,
            hide_index=True,
            height=300
        )

        st.markdown('</div></div>', unsafe_allow_html=True)

    else:
        st.info("No forecast data available")

# ============================================================
# FEATURE IMPORTANCE PAGE - TANPA AI INSIGHT
# ============================================================

elif menu == "Feature Importance":
    show_page_info(
        "Feature Importance",
        "Halaman ini menunjukkan faktor-faktor (fitur) yang paling berpengaruh terhadap performa karyawan dan KPI. "
        "Semakin panjang bar, semakin penting fitur tersebut. Gunakan insight ini untuk fokus pada area yang paling berdampak.",
        "fa-chart-simple"
    )

    # ========== CHART SECTION ==========
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <i class="fas fa-chart-simple"></i>
                <span>Feature Importance Analysis</span>
            </div>
        </div>
        <div class="chart-body">
    """, unsafe_allow_html=True)

    label_map = {
        'level_jabatan': 'Level Jabatan', 'lama_bekerja_tahun': 'Lama Bekerja',
        'department_name': 'Departemen', 'usia': 'Usia',
        'kpi_category': 'Kategori KPI', 'jumlah_evaluasi': 'Jumlah Evaluasi',
        'gender': 'Gender', 'jumlah_proyek': 'Jumlah Proyek',
        'rentang_usia': 'Rentang Usia', 'project_budget': 'Budget Proyek',
        'usia_x_cluster': 'Usia x Cluster', 'level_x_masa': 'Level x Masa Kerja',
        'cluster': 'Cluster'
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="margin-bottom: 8px;">
            <div style="font-size: 20px; font-weight: 700; color: #374151;">
                <i class="fas fa-layer-group" style="color:#8B5CF6;"></i> &nbsp;Clustering Model
            </div>
            <span style="font-size: 13px; color: #6B7280;">Fitur yang mempengaruhi pengelompokan karyawan</span>
        </div>
        """, unsafe_allow_html=True)

        if data['feature_importance'] is not None:
            df_fi = data['feature_importance'].sort_values('importance', ascending=True).tail(10).copy()
            df_fi['label'] = df_fi['feature'].map(lambda x: label_map.get(x, x))

            max_val = df_fi['importance'].max()
            colors = [f'rgba(139,92,246,{0.3 + 0.7 * (v / max_val)})' for v in df_fi['importance']]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_fi['importance'], y=df_fi['label'],
                orientation='h',
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{v:.3f}" for v in df_fi['importance']],
                textposition='outside',
                textfont=dict(size=11, color='#374151'),
                hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
            ))
            fig.update_layout(
                height=400,
                xaxis=dict(title='Tingkat Pengaruh', gridcolor='rgba(0,0,0,0.06)', zeroline=False),
                yaxis=dict(title='', tickfont=dict(size=12)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=60, t=10, b=40),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            top = data['feature_importance'].sort_values('importance', ascending=False).iloc[0]
            top_label = label_map.get(top['feature'], top['feature'])
            st.markdown(f"""
            <div style="background: #f5f3ff; border-radius: 10px; padding: 10px 14px; 
                        border-left: 4px solid #8B5CF6; margin-top: 4px;">
                <div style="font-size: 12px; color: #6B7280;">
                    <i class="fas fa-trophy" style="color:#8B5CF6;"></i> &nbsp;Fitur Paling Berpengaruh
                </div>
                <span style="font-size: 15px; font-weight: 700; color: #8B5CF6;">{top_label}</span>
                <span style="font-size: 12px; color: #9CA3AF;">&nbsp;({top['importance']:.4f})</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Data feature importance untuk clustering tidak tersedia")

    with col2:
        st.markdown("""
        <div style="margin-bottom: 8px;">
            <div style="font-size: 20px; font-weight: 700; color: #374151;">
                <i class="fas fa-bullseye" style="color:#667eea;"></i> &nbsp;Regression Model
            </div>
            <span style="font-size: 13px; color: #6B7280;">Fitur yang mempengaruhi prediksi KPI</span>
        </div>
        """, unsafe_allow_html=True)

        if data['feature_importance_reg'] is not None:
            df_reg = data['feature_importance_reg'].sort_values('importance', ascending=True).tail(10).copy()
            df_reg['label'] = df_reg['feature'].map(lambda x: label_map.get(x, x))

            max_val = df_reg['importance'].max()
            colors = [f'rgba(102,126,234,{0.3 + 0.7 * (v / max_val)})' for v in df_reg['importance']]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_reg['importance'], y=df_reg['label'],
                orientation='h',
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{v:.0f}" for v in df_reg['importance']],
                textposition='outside',
                textfont=dict(size=11, color='#374151'),
                hovertemplate='<b>%{y}</b><br>Importance: %{x:.1f}<extra></extra>'
            ))
            fig.update_layout(
                height=400,
                xaxis=dict(title='Tingkat Pengaruh', gridcolor='rgba(0,0,0,0.06)', zeroline=False),
                yaxis=dict(title='', tickfont=dict(size=12)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=60, t=10, b=40),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            top_reg = data['feature_importance_reg'].sort_values('importance', ascending=False).iloc[0]
            top_reg_label = label_map.get(top_reg['feature'], top_reg['feature'])
            st.markdown(f"""
            <div style="background: #eef2ff; border-radius: 10px; padding: 10px 14px; 
                        border-left: 4px solid #667eea; margin-top: 4px;">
                <div style="font-size: 12px; color: #6B7280;">
                    <i class="fas fa-trophy" style="color:#667eea;"></i> &nbsp;Fitur Paling Berpengaruh
                </div>
                <span style="font-size: 15px; font-weight: 700; color: #667eea;">{top_reg_label}</span>
                <span style="font-size: 12px; color: #9CA3AF;">&nbsp;({top_reg['importance']:.1f})</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Data feature importance untuk regression tidak tersedia")

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ========== COMPARISON TABLE ==========
    if data['feature_importance'] is not None and data['feature_importance_reg'] is not None:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <i class="fas fa-table"></i>
                    <span>Perbandingan Feature Importance</span>
                </div>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        df_clust = data['feature_importance'].copy()
        df_clust['label'] = df_clust['feature'].map(lambda x: label_map.get(x, x))
        df_clust = df_clust.sort_values('importance', ascending=False).reset_index(drop=True)
        df_clust['Rank Clustering'] = df_clust.index + 1
        df_clust = df_clust.rename(columns={'importance': 'Importance (Clustering)', 'label': 'Fitur'})

        df_regg = data['feature_importance_reg'].copy()
        df_regg['label'] = df_regg['feature'].map(lambda x: label_map.get(x, x))
        df_regg = df_regg.sort_values('importance', ascending=False).reset_index(drop=True)
        df_regg['Rank Regression'] = df_regg.index + 1
        df_regg = df_regg.rename(columns={'importance': 'Importance (Regression)', 'label': 'Fitur'})

        df_compare = pd.merge(
            df_clust[['Fitur', 'Importance (Clustering)', 'Rank Clustering']],
            df_regg[['Fitur', 'Importance (Regression)', 'Rank Regression']],
            on='Fitur', how='outer'
        ).fillna('-')

        st.dataframe(
            df_compare,
            column_config={
                'Fitur': st.column_config.TextColumn(width='medium'),
                'Importance (Clustering)': st.column_config.NumberColumn(format="%.4f", width='medium'),
                'Rank Clustering': st.column_config.NumberColumn(format="%d", width='small'),
                'Importance (Regression)': st.column_config.NumberColumn(format="%.1f", width='medium'),
                'Rank Regression': st.column_config.NumberColumn(format="%d", width='small'),
            },
            use_container_width=True,
            hide_index=True,
            height=300
        )

        st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================
# DATA TABLES PAGE - INTERAKTIF & MODERN
# ============================================================
elif menu == "Data Tables":
    show_page_info(
        "Data Tables",
        "Halaman ini menampilkan data mentah (raw data) yang digunakan dalam dashboard. "
        "Anda bisa melihat, mencari, dan menganalisis data secara detail. Cocok untuk ekspor data atau pengecekan manual.",
        "fa-table"
    )
    
    # ========== HEADER CARD ==========
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <i class="fas fa-table"></i>
                <span>Data Tables</span>
            </div>
        </div>
        <div class="chart-body">
    """, unsafe_allow_html=True)
    
    # ========== SEARCH BOX ==========
    search = st.text_input("Search Data", placeholder="Type keyword to search...")
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4 = st.tabs([
        "Department Performance", 
        "Cluster Summary", 
        "Forecast Data", 
        "Feature Importance"
    ])
    
    # ========== TAB 1: DEPARTMENT PERFORMANCE ==========
    with tab1:
        if data['dept_performance'] is not None:
            df = data['dept_performance'].copy()
            
            if search:
                mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                df = df[mask]
                st.caption(f"Showing {len(df)} of {len(data['dept_performance'])} rows")
            
            st.dataframe(
                df,
                column_config={
                    'departemen': st.column_config.TextColumn('Department', width='medium'),
                    'avg_kpi': st.column_config.NumberColumn('Avg KPI', format="%.1f", width='small'),
                    'pencapaian_%': st.column_config.NumberColumn('Achievement', format="%.1f%%", width='small'),
                    'jumlah_karyawan': st.column_config.NumberColumn('Total Employees', format="%d", width='small'),
                },
                use_container_width=True,
                hide_index=True
            )
            
            csv = data['dept_performance'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="department_performance.csv",
                mime="text/csv",
                key="download_dept"
            )
        else:
            st.info("Data department performance not available")
    
    # ========== TAB 2: CLUSTER SUMMARY ==========
    with tab2:
        if data['cluster_summary'] is not None:
            df_c = data['cluster_summary'].copy()
            df_c['Kategori'] = df_c['avg_kpi'].apply(get_cluster_label)
            
            if search:
                mask = df_c.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                df_c = df_c[mask]
                st.caption(f"Showing {len(df_c)} of {len(data['cluster_summary'])} rows")
            
            st.dataframe(
                df_c,
                column_config={
                    'cluster': st.column_config.NumberColumn('Cluster', format="%d", width='small'),
                    'Kategori': st.column_config.TextColumn('Category', width='medium'),
                    'avg_kpi': st.column_config.NumberColumn('Avg KPI', format="%.2f", width='small'),
                    'pencapaian': st.column_config.NumberColumn('Achievement', format="%.2f%%", width='small'),
                    'rata_masa_kerja': st.column_config.NumberColumn('Avg Tenure', format="%.2f", width='small'),
                    'jumlah_karyawan': st.column_config.NumberColumn('Total', format="%d", width='small'),
                },
                use_container_width=True,
                hide_index=True
            )
            
            csv = data['cluster_summary'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="cluster_summary.csv",
                mime="text/csv",
                key="download_cluster"
            )
        else:
            st.info("Data cluster summary not available")
    
    # ========== TAB 3: FORECAST DATA ==========
    with tab3:
        if data['forecast_data'] is not None:
            df_fore = data['forecast_data'].copy()
            
            if search:
                mask = df_fore.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                df_fore = df_fore[mask]
                st.caption(f"Showing {len(df_fore)} of {len(data['forecast_data'])} rows")
            
            st.dataframe(
                df_fore,
                column_config={
                    'department_name': st.column_config.TextColumn('Department', width='medium'),
                    'periode': st.column_config.TextColumn('Period', width='medium'),
                    'avg_kpi': st.column_config.NumberColumn('KPI', format="%.2f", width='small'),
                },
                use_container_width=True,
                hide_index=True
            )
            
            csv = data['forecast_data'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="forecast_data.csv",
                mime="text/csv",
                key="download_forecast"
            )
        else:
            st.info("Data forecast not available")
    
    # ========== TAB 4: FEATURE IMPORTANCE ==========
    with tab4:
        if data['feature_importance_reg'] is not None:
            df_fi = data['feature_importance_reg'].copy()
            
            if search:
                mask = df_fi.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                df_fi = df_fi[mask]
                st.caption(f"Showing {len(df_fi)} of {len(data['feature_importance_reg'])} rows")
            
            st.dataframe(
                df_fi,
                column_config={
                    'feature': st.column_config.TextColumn('Feature', width='medium'),
                    'importance': st.column_config.NumberColumn('Importance', format="%.0f", width='small'),
                },
                use_container_width=True,
                hide_index=True
            )
            
            csv = data['feature_importance_reg'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="feature_importance.csv",
                mime="text/csv",
                key="download_feature"
            )
        else:
            st.info("Data feature importance not available")
    
    # ========== STATISTIK RINGKASAN (DENGAN KOTAK) ==========
    st.markdown("---")
    st.markdown("### Data Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if data['dept_performance'] is not None:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Departments</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">{len(data['dept_performance'])}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Departments</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">-</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if data['cluster_summary'] is not None:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Clusters</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">{len(data['cluster_summary'])}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Clusters</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">-</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if data['forecast_data'] is not None:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Forecast Data</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">{len(data['forecast_data']):,}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Forecast Data</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">-</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if data['feature_importance_reg'] is not None:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Features</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">{len(data['feature_importance_reg'])}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;">
                <div style="font-size: 14px; color: #6B7280;">Total Features</div>
                <div style="font-size: 28px; font-weight: 700; color: #6C5CE7;">-</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)


# ============================================================
# KNOWLEDGE BASE PAGE - FINAL VERSION
# ============================================================
elif menu == "Knowledge Base":
    show_page_info(
        "Knowledge Base",
        "Halaman ini berisi penjelasan lengkap tentang semua fitur, istilah, dan konsep yang digunakan dalam dashboard HR Analytics. "
        "Gunakan halaman ini sebagai referensi untuk memahami setiap metrik dan analisis yang tersedia.",
        "fa-book-open"
    )

    def kb_section(icon, title):
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin: 24px 0 16px 0;">
            <div style="width: 44px; height: 44px; border-radius: 14px; background: linear-gradient(135deg, #6C5CE7, #8B5CF6);
                        display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <i class="fas {icon}" style="color: white; font-size: 20px;"></i>
            </div>
            <div style="font-size: 22px; font-weight: 700; color: #2d2d4e;">{title}</div>
            <div style="flex: 1; height: 2px; background: linear-gradient(90deg, #6C5CE730, transparent);"></div>
        </div>
        """, unsafe_allow_html=True)

    # ========== SECTION 1: TENTANG DASHBOARD ==========
    kb_section("fa-info-circle", "Tentang Dashboard HR Analytics")

    st.markdown("""
    <div style="background: white; border-radius: 20px; padding: 28px 32px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #e0e0e0; margin-bottom: 8px;">
        <div style="font-size: 20px; font-weight: 700; color: #6C5CE7; margin-bottom: 12px;">
            <i class="fas fa-bullseye"></i> &nbsp;Apa itu HR Analytics Dashboard?
        </div>
        <p style="color: #4a4a6a; font-size: 17px; line-height: 1.9; margin: 0;">
            HR Analytics Dashboard adalah platform analitik yang dirancang untuk membantu tim HR memantau, 
            menganalisis, dan meningkatkan performa karyawan. Dashboard ini mengintegrasikan data dari berbagai 
            sumber dan menyajikannya dalam visualisasi yang mudah dipahami.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ========== SECTION 2: METRIK & ISTILAH ==========
    kb_section("fa-chart-bar", "Metrik &amp; Istilah Penting")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; 
                    border-left: 4px solid #6C5CE7; box-shadow: 0 2px 8px rgba(108,92,231,0.08);">
            <div style="font-size: 17px; font-weight: 700; color: #6C5CE7; margin-bottom: 10px;">
                <i class="fas fa-chart-line"></i> &nbsp;KPI (Key Performance Indicator)
            </div>
            <p style="color: #4a4a6a; font-size: 15px; line-height: 1.7; margin: 0;">
                Indikator utama yang digunakan untuk mengukur performa karyawan atau departemen. 
                Semakin tinggi nilai KPI, semakin baik performanya.
            </p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; 
                    border-left: 4px solid #10B981; box-shadow: 0 2px 8px rgba(16,185,129,0.08);">
            <div style="font-size: 17px; font-weight: 700; color: #10B981; margin-bottom: 10px;">
                <i class="fas fa-trophy"></i> &nbsp;Achievement
            </div>
            <p style="color: #4a4a6a; font-size: 15px; line-height: 1.7; margin: 0;">
                Persentase pencapaian target yang telah ditetapkan. Achievement 100% berarti target tercapai sempurna.
            </p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; 
                    border-left: 4px solid #F59E0B; box-shadow: 0 2px 8px rgba(245,158,11,0.08);">
            <div style="font-size: 17px; font-weight: 700; color: #F59E0B; margin-bottom: 10px;">
                <i class="fas fa-superscript"></i> &nbsp;R&#178; Score
            </div>
            <p style="color: #4a4a6a; font-size: 15px; line-height: 1.7; margin: 0;">
                Ukuran seberapa baik model regresi dalam memprediksi data. Nilai mendekati 100% menunjukkan prediksi yang akurat.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; 
                    border-left: 4px solid #8B5CF6; box-shadow: 0 2px 8px rgba(139,92,246,0.08);">
            <div style="font-size: 17px; font-weight: 700; color: #8B5CF6; margin-bottom: 10px;">
                <i class="fas fa-layer-group"></i> &nbsp;Cluster / Kategori Performa
            </div>
            <p style="color: #4a4a6a; font-size: 15px; line-height: 1.7; margin: 0;">
                Pengelompokan karyawan berdasarkan performa:<br>
                🌟 High Performer (KPI ≥85) &nbsp;|&nbsp; 📊 Solid (70-84)<br>
                📈 Average (55-69) &nbsp;|&nbsp; ⚠️ Needs Improvement (&lt;55)
            </p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; 
                    border-left: 4px solid #FD7E14; box-shadow: 0 2px 8px rgba(253,126,20,0.08);">
            <div style="font-size: 17px; font-weight: 700; color: #FD7E14; margin-bottom: 10px;">
                <i class="fas fa-chart-line"></i> &nbsp;Forecasting
            </div>
            <p style="color: #4a4a6a; font-size: 15px; line-height: 1.7; margin: 0;">
                Prediksi performa masa depan berdasarkan data historis. Grafik menampilkan data aktual (hijau) vs prediksi (oranye).
            </p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; 
                    border-left: 4px solid #EF4444; box-shadow: 0 2px 8px rgba(239,68,68,0.08);">
            <div style="font-size: 17px; font-weight: 700; color: #EF4444; margin-bottom: 10px;">
                <i class="fas fa-chart-simple"></i> &nbsp;Feature Importance
            </div>
            <p style="color: #4a4a6a; font-size: 15px; line-height: 1.7; margin: 0;">
                Identifikasi faktor-faktor yang paling berpengaruh terhadap performa karyawan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ========== SECTION 3: PENJELASAN SETIAP TAB ==========
    kb_section("fa-layer-group", "Penjelasan Setiap Halaman")

    pages = [
        ("fa-gauge-high", "#6C5CE7", "Dashboard", "Halaman utama dengan ringkasan performa HR, metrik KPI, perbandingan departemen, dan wawasan kunci."),
        ("fa-layer-group", "#8B5CF6", "Clustering", "Pengelompokan karyawan: High Performer, Solid Performer, Average Performer, dan Needs Improvement."),
        ("fa-chart-line", "#FD7E14", "Forecasting", "Prediksi KPI departemen dengan tampilan aktual (hijau) vs forecast (oranye)."),
        ("fa-chart-simple", "#EF4444", "Feature Importance", "Faktor-faktor yang paling berpengaruh terhadap performa karyawan."),
        ("fa-table", "#10B981", "Data Tables", "Data mentah dashboard. Cocok untuk ekspor data atau pengecekan detail."),
        ("fa-book-open", "#F59E0B", "Knowledge Base", "Halaman ini! Penjelasan lengkap semua fitur dan istilah di dashboard."),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, (icon, color, title, desc) in enumerate(pages):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 18px 20px; margin-bottom: 14px;
                        border-top: 4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                <div style="font-size: 17px; font-weight: 700; color: {color}; margin-bottom: 10px;">
                    <i class="fas {icon}"></i> &nbsp;{title}
                </div>
                <p style="color: #6B7280; font-size: 15px; line-height: 1.7; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ========== SECTION 4: TIPS ==========
    kb_section("fa-lightbulb", "Tips &amp; Trik Penggunaan Dashboard")

    tips = [
        ("fa-chart-simple", "#6C5CE7", "Fokus pada Feature Importance", "Ketahui faktor apa yang paling mempengaruhi performa karyawan."),
        ("fa-chart-line", "#FD7E14", "Manfaatkan Forecasting", "Prediksi performa masa depan untuk perencanaan anggaran pelatihan."),
        ("fa-layer-group", "#8B5CF6", "Gunakan Clustering", "Kelompokkan karyawan untuk program pengembangan yang tepat sasaran."),
        ("fa-robot", "#10B981", "Aktifkan AI Insights", "Dapatkan rekomendasi cerdas dari AI untuk meningkatkan performa HR."),
    ]

    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]

    for i, (icon, color, title, desc) in enumerate(tips):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 20px 16px; text-align: center;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-bottom: 4px solid {color}; height: 100%;">
                <div style="width: 52px; height: 52px; border-radius: 14px; background: {color}18;
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;">
                    <i class="fas {icon}" style="font-size: 24px; color: {color};"></i>
                </div>
                <div style="font-weight: 700; color: {color}; font-size: 16px; margin-bottom: 8px; line-height: 1.4;">{title}</div>
                <p style="font-size: 14px; color: #6B7280; line-height: 1.6; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ========== SECTION 5: FAQ ==========
    kb_section("fa-circle-question", "Frequently Asked Questions (FAQ)")

    faqs = [
        ("fa-chart-bar", "#6C5CE7", "Bagaimana cara membaca KPI?", "KPI diukur dalam skala 0-100. Semakin tinggi nilai KPI, semakin baik performa departemen atau karyawan tersebut."),
        ("fa-layer-group", "#8B5CF6", "Apa perbedaan Clustering dan Forecasting?", "Clustering mengelompokkan data saat ini berdasarkan kemiripan karakteristik, sedangkan Forecasting memprediksi data masa depan berdasarkan tren historis."),
        ("fa-file-export", "#10B981", "Bisakah data diekspor?", "Ya! Pada halaman Data Tables, Anda bisa melihat dan menyalin data mentah untuk dianalisis lebih lanjut."),
        ("fa-bullseye", "#FD7E14", "Seberapa akurat prediksi Forecasting?", "Akurasi prediksi diukur dengan MAPE (Mean Absolute Percentage Error). Semakin kecil MAPE, semakin akurat prediksinya."),
        ("fa-users", "#EF4444", "Apa arti label cluster (High Performer, dll)?", "Label berdasarkan rata-rata KPI: High Performer (≥85), Solid Performer (70-84), Average Performer (55-69), Needs Improvement (<55)."),
    ]

    for icon, color, q, a in faqs:
        st.markdown(f"""
        <div style="background: white; border-radius: 14px; padding: 18px 20px; margin-bottom: 10px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05); border-left: 4px solid {color};">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: {color}18;
                            display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    <i class="fas {icon}" style="font-size: 14px; color: {color};"></i>
                </div>
                <div style="font-size: 17px; font-weight: 700; color: #2d2d4e;">{q}</div>
            </div>
            <p style="color: #6B7280; font-size: 15px; line-height: 1.7; margin: 0; padding-left: 42px;">{a}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <i class="fas fa-chart-line"></i> HR Analytics Dashboard • Built with Streamlit • Data Warehouse Project
</div>
""", unsafe_allow_html=True)