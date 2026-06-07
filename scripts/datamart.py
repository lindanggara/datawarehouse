# ============================================================
# IMPLEMENTASI DATA MART HUMAN RESOURCE
# Analisis & Prediksi Performa Karyawan (FIXED VERSION - WITH FOLDER STRUCTURE)
# ============================================================

import sys
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. IMPORT LIBRARY
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine, text
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    silhouette_score, davies_bouldin_score, calinski_harabasz_score,
    mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import Birch, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
import skfuzzy as fuzz
from prophet import Prophet
from statsmodels.tsa.stattools import adfuller
import joblib
import os
import time

# ============================================================
# KONFIGURASI PATH UNTUK STRUKTUR FOLDER BARU
# ============================================================

# Buat semua folder yang diperlukan
os.makedirs('../data/dimensions', exist_ok=True)
os.makedirs('../data/facts', exist_ok=True)
os.makedirs('../data/clustering', exist_ok=True)
os.makedirs('../data/forecasting', exist_ok=True)
os.makedirs('../data/regression', exist_ok=True)
os.makedirs('../data/outputs/eda', exist_ok=True)
os.makedirs('../data/outputs/clustering', exist_ok=True)
os.makedirs('../data/outputs/forecasting', exist_ok=True)
os.makedirs('../data/outputs/regression', exist_ok=True)
os.makedirs('../models', exist_ok=True)

# Dictionary path untuk memudahkan
PATHS = {
    'data': '../data/',
    'dimensions': '../data/dimensions/',
    'facts': '../data/facts/',
    'clustering': '../data/clustering/',
    'forecasting': '../data/forecasting/',
    'regression': '../data/regression/',
    'outputs_eda': '../data/outputs/eda/',
    'outputs_clustering': '../data/outputs/clustering/',
    'outputs_forecasting': '../data/outputs/forecasting/',
    'outputs_regression': '../data/outputs/regression/',
    'models': '../models/'
}

print("✅ Semua library berhasil diimport")

# ============================================================
# 2. KONFIGURASI DATABASE
# ============================================================

MYSQL_URI = "mysql+pymysql://root:@localhost:3307/hr_project_db"
PGSQL_URI = "postgresql+psycopg2://postgres:12345@localhost:5432/hr_dwh"

try:
    engine_mysql = create_engine(MYSQL_URI)
    engine_pg = create_engine(PGSQL_URI)

    with engine_mysql.connect() as conn:
        conn.execute(text("SELECT 1"))
    with engine_pg.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("✅ Koneksi database berhasil")
    print(f"   MySQL  → {MYSQL_URI.split('@')[-1]}")
    print(f"   PgSQL  → {PGSQL_URI.split('@')[-1]}")
except Exception as e:
    print(f"❌ Koneksi database gagal: {e}")
    sys.exit(1)

# ============================================================
# 3. ETL PROCESS - EXTRACT FROM MYSQL
# ============================================================

print("\n" + "="*60)
print("3. ETL PROCESS")
print("="*60)

try:
    df_employee   = pd.read_sql("SELECT * FROM employee", engine_mysql)
    df_department = pd.read_sql("SELECT * FROM department", engine_mysql)
    df_position   = pd.read_sql("SELECT * FROM position", engine_mysql)
    df_project    = pd.read_sql("SELECT * FROM project", engine_mysql)
    df_kpi        = pd.read_sql("SELECT * FROM kpi", engine_mysql)
    df_project_kpi = pd.read_sql("SELECT * FROM project_kpi_fact", engine_mysql)

    print(f"✅ Data berhasil diekstrak dari MySQL:")
    print(f"   employee        : {len(df_employee)} rows")
    print(f"   department      : {len(df_department)} rows")
    print(f"   position        : {len(df_position)} rows")
    print(f"   project         : {len(df_project)} rows")
    print(f"   kpi             : {len(df_kpi)} rows")
    print(f"   project_kpi_fact: {len(df_project_kpi)} rows")

except Exception as e:
    print(f"❌ Error extracting data: {e}")
    sys.exit(1)

# ============================================================
# 4. TRANSFORM - CREATE DIMENSIONS AND FACTS
# ============================================================

# dim_employee
df_dim_employee = pd.merge(df_employee, df_department, on='department_id', how='left')
df_dim_employee = pd.merge(df_dim_employee, df_position, on='position_id', how='left')

df_dim_employee['gender'] = df_dim_employee['gender'].map(
    {'Laki-laki': 'M', 'Perempuan': 'F'}
).fillna('U')
df_dim_employee['usia'] = (
    pd.Timestamp.now().year - pd.to_datetime(df_dim_employee['birth_date']).dt.year
)
df_dim_employee['lama_bekerja_tahun'] = (
    pd.Timestamp.now().year - pd.to_datetime(df_dim_employee['hire_date']).dt.year
)
df_dim_employee['rentang_usia'] = pd.cut(
    df_dim_employee['usia'],
    bins=[20, 30, 40, 50, 60],
    labels=['20-30', '30-40', '40-50', '50-60']
)

df_dim_employee = df_dim_employee[[
    'employee_id', 'employee_name', 'gender', 'usia', 'rentang_usia',
    'lama_bekerja_tahun', 'department_name', 'position_name', 'level_jabatan'
]]

# dim_project
df_dim_project = df_project.copy()
df_dim_project['durasi_hari'] = (
    pd.to_datetime(df_dim_project['project_end_date']) -
    pd.to_datetime(df_dim_project['project_start_date'])
).dt.days
df_dim_project = df_dim_project[[
    'project_id', 'project_name', 'project_status', 'project_budget', 'durasi_hari'
]]

# dim_kpi
df_dim_kpi = df_kpi[['kpi_id', 'kpi_name', 'kpi_category', 'kpi_target']]

# fact_project_kpi
df_fact = pd.merge(df_project_kpi, df_kpi[['kpi_id', 'kpi_target']], on='kpi_id', how='left')
df_fact['status_pencapaian'] = np.where(
    df_fact['kpi_value'] >= df_fact['kpi_target'], 'Tercapai', 'Tidak Tercapai'
)
df_fact = df_fact[[
    'fact_id', 'employee_id', 'project_id', 'kpi_id',
    'evaluation_date', 'kpi_value', 'kpi_target', 'status_pencapaian'
]]

print("✅ Transformasi data selesai")

# ============================================================
# 5. LOAD TO POSTGRESQL
# ============================================================

try:
    with engine_pg.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS fact_project_kpi CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS dim_employee CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS dim_project CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS dim_kpi CASCADE"))
        conn.commit()

    df_dim_employee.to_sql("dim_employee",    engine_pg, if_exists="replace", index=False)
    df_dim_project.to_sql("dim_project",      engine_pg, if_exists="replace", index=False)
    df_dim_kpi.to_sql("dim_kpi",              engine_pg, if_exists="replace", index=False)
    df_fact.to_sql("fact_project_kpi",        engine_pg, if_exists="replace", index=False)
    print("✅ Data berhasil diload ke PostgreSQL")

except Exception as e:
    print(f"❌ Error loading to PostgreSQL: {e}")

# ============================================================
# 6. VERIFIKASI DATA MART
# ============================================================

print("\n" + "="*60)
print("6. VERIFIKASI DATA MART")
print("="*60)

print(f"  dim_employee      : {len(df_dim_employee)} baris")
print(f"  dim_project       : {len(df_dim_project)} baris")
print(f"  dim_kpi           : {len(df_dim_kpi)} baris")
print(f"  fact_project_kpi  : {len(df_fact)} baris")

invalid_gender     = df_dim_employee[~df_dim_employee['gender'].isin(['M', 'F'])].shape[0]
invalid_durasi     = df_dim_project[df_dim_project['durasi_hari'] <= 0].shape[0]
inconsistent_status = df_fact[
    ((df_fact['kpi_value'] >= df_fact['kpi_target']) & (df_fact['status_pencapaian'] != 'Tercapai')) |
    ((df_fact['kpi_value'] <  df_fact['kpi_target']) & (df_fact['status_pencapaian'] != 'Tidak Tercapai'))
].shape[0]

print(f"\n  Gender invalid    : {invalid_gender} {'✅' if invalid_gender == 0 else '❌'}")
print(f"  Durasi <= 0       : {invalid_durasi} {'✅' if invalid_durasi == 0 else '❌'}")
print(f"  Status inkonsisten: {inconsistent_status} {'✅' if inconsistent_status == 0 else '❌'}")

# ============================================================
# 7. EDA
# ============================================================

print("\n" + "="*60)
print("7. EDA - EXPLORATORY DATA ANALYSIS")
print("="*60)

df_eda = pd.merge(
    df_fact,
    df_dim_employee[['employee_id', 'department_name', 'level_jabatan', 'usia', 'lama_bekerja_tahun']],
    on='employee_id', how='left'
)

# 7.1 KPI per departemen
plt.figure(figsize=(12, 6))
dept_order = df_eda.groupby('department_name')['kpi_value'].mean().sort_values(ascending=False).index
sns.boxplot(data=df_eda, x='department_name', y='kpi_value', order=dept_order, palette='Set2')
plt.xticks(rotation=45, ha='right')
plt.title('Distribusi KPI per Departemen', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(PATHS['outputs_eda'] + 'eda_kpi_by_dept.png', dpi=120)
plt.close()

# 7.2 Korelasi heatmap
numeric_cols_eda = ['usia', 'lama_bekerja_tahun', 'kpi_value', 'kpi_target']
available_cols = [c for c in numeric_cols_eda if c in df_eda.columns]
if len(available_cols) >= 2:
    plt.figure(figsize=(8, 6))
    sns.heatmap(df_eda[available_cols].corr(), annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
    plt.title('Korelasi antar Variabel Numerik', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(PATHS['outputs_eda'] + 'eda_correlation_heatmap.png', dpi=120)
    plt.close()

# 7.3 Achievement per level
df_eda['achievement_pct'] = (100 * df_eda['kpi_value'] / df_eda['kpi_target']).clip(0, 150)
plt.figure(figsize=(10, 6))
sns.violinplot(data=df_eda, x='level_jabatan', y='achievement_pct', palette='muted')
plt.xticks(rotation=45)
plt.title('Distribusi Pencapaian KPI per Level Jabatan', fontsize=14, fontweight='bold')
plt.ylabel('Pencapaian KPI (%)')
plt.tight_layout()
plt.savefig(PATHS['outputs_eda'] + 'eda_achievement_by_level.png', dpi=120)
plt.close()

# 7.4 Trend KPI
df_trend = df_fact.copy()
df_trend['bulan'] = pd.to_datetime(df_trend['evaluation_date']).dt.to_period('M')
df_trend = df_trend.groupby('bulan')['kpi_value'].mean().reset_index()
df_trend['bulan'] = df_trend['bulan'].astype(str)

plt.figure(figsize=(12, 5))
plt.plot(range(len(df_trend)), df_trend['kpi_value'], 'o-', color='steelblue', linewidth=2, markersize=6)
plt.xticks(range(len(df_trend)), df_trend['bulan'], rotation=45, ha='right')
plt.title('Trend Rata-rata KPI Seluruh Karyawan', fontsize=14, fontweight='bold')
plt.xlabel('Periode')
plt.ylabel('Rata-rata KPI')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(PATHS['outputs_eda'] + 'eda_kpi_trend.png', dpi=120)
plt.close()

print("✅ EDA selesai, visualisasi disimpan di folder data/outputs/eda/")

# ============================================================
# 8. ANALYTICAL VIEWS
# ============================================================

print("\n" + "="*60)
print("8. MEMBUAT ANALYTICAL VIEWS")
print("="*60)

# ===== VIEW CLUSTERING =====
print("   Membuat v_analisa_clustering...")

df_fact_temp = df_fact.copy()
df_fact_temp['department_name'] = df_fact_temp['employee_id'].map(
    df_dim_employee.set_index('employee_id')['department_name']
)

sample_frac = 0.4
df_fact_sample, _ = train_test_split(
    df_fact_temp, train_size=sample_frac,
    stratify=df_fact_temp['department_name'], random_state=42
)
df_fact_sample = df_fact_sample.drop('department_name', axis=1)
print(f"   Original: {len(df_fact)} rows, Sampling: {len(df_fact_sample)} rows ({sample_frac*100:.0f}%)")

df_clust = pd.merge(df_fact_sample, df_dim_employee, on='employee_id', how='left')
df_clust = pd.merge(df_clust, df_dim_kpi, on='kpi_id', how='left')

df_clust = df_clust.groupby(
    ['employee_id', 'employee_name', 'gender', 'usia', 'rentang_usia',
     'lama_bekerja_tahun', 'level_jabatan', 'department_name', 'kpi_category'],
    observed=True
).agg(
    avg_kpi_value=('kpi_value', 'mean'),
    jumlah_evaluasi=('fact_id', 'count'),
    jumlah_proyek=('project_id', 'nunique')
).reset_index()

kpi_targets = df_dim_kpi[['kpi_category', 'kpi_target']].drop_duplicates('kpi_category')
df_clust = pd.merge(df_clust, kpi_targets, on='kpi_category', how='left')
df_clust['persen_tercapai'] = (100 * df_clust['avg_kpi_value'] / df_clust['kpi_target']).clip(0, 120)
print(f"  v_analisa_clustering  : {len(df_clust)} baris")

# ===== VIEW FORECASTING =====
print("   Membuat v_analisa_forecasting...")

df_fore = pd.merge(
    df_fact,
    df_dim_employee[['employee_id', 'department_name']],
    on='employee_id', how='left'
)
df_fore['periode'] = pd.to_datetime(df_fore['evaluation_date']).dt.to_period('M').dt.start_time
df_fore = df_fore.groupby(['department_name', 'periode'], observed=True)['kpi_value'].mean().reset_index()
df_fore.columns = ['department_name', 'periode', 'avg_kpi']
df_fore = df_fore.sort_values(['department_name', 'periode'])
print(f"  v_analisa_forecasting : {len(df_fore)} baris")

sample_dept = df_fore['department_name'].iloc[0]
print(f"  🔍 Contoh data untuk {sample_dept}:")
print(df_fore[df_fore['department_name'] == sample_dept].head(5).to_string(index=False))

# ===== VIEW REGRESI =====
print("   Membuat v_analisa_regresi...")

df_fact_temp2 = df_fact.copy()
df_fact_temp2['department_name'] = df_fact_temp2['employee_id'].map(
    df_dim_employee.set_index('employee_id')['department_name']
)

reg_sample_frac = 0.25
df_fact_reg, _ = train_test_split(
    df_fact_temp2, train_size=reg_sample_frac,
    stratify=df_fact_temp2['department_name'], random_state=42
)
df_fact_reg = df_fact_reg.drop('department_name', axis=1)
print(f"   Regresi sampling: {len(df_fact_reg)} rows ({reg_sample_frac*100:.0f}%)")

df_regr = pd.merge(
    df_fact_reg,
    df_dim_employee[['employee_id', 'usia', 'lama_bekerja_tahun', 'level_jabatan', 'department_name']],
    on='employee_id', how='left'
)
df_regr = pd.merge(df_regr, df_dim_project[['project_id', 'project_budget', 'durasi_hari']], on='project_id', how='left')
df_regr = pd.merge(df_regr, df_dim_kpi[['kpi_id', 'kpi_category']], on='kpi_id', how='left')

df_regr = df_regr.groupby(
    ['employee_id', 'usia', 'lama_bekerja_tahun', 'level_jabatan',
     'department_name', 'project_budget', 'durasi_hari', 'kpi_category'],
    observed=True
)['kpi_value'].mean().reset_index()
df_regr.columns = [
    'employee_id', 'usia', 'lama_bekerja_tahun', 'level_jabatan',
    'department_name', 'project_budget', 'durasi_hari', 'kpi_category', 'rata_kpi_value'
]
print(f"  v_analisa_regresi     : {len(df_regr)} baris")

del df_fact_temp, df_fact_temp2

# ============================================================
# 9. FEATURE SELECTION
# ============================================================

print("\n" + "="*60)
print("9. FEATURE SELECTION - Random Forest Regressor")
print("="*60)

df_enc = df_clust.copy()
categorical_cols = ['gender', 'level_jabatan', 'department_name', 'kpi_category', 'rentang_usia']

for col in categorical_cols:
    if col in df_enc.columns:
        le = LabelEncoder()
        df_enc[col] = le.fit_transform(df_enc[col].astype(str))
        joblib.dump(le, PATHS['models'] + f'label_encoder_{col}.pkl')

feature_cols = [
    'usia', 'lama_bekerja_tahun', 'level_jabatan',
    'jumlah_evaluasi', 'jumlah_proyek',
    'gender', 'department_name', 'kpi_category', 'rentang_usia'
]
feature_cols = [c for c in feature_cols if c in df_enc.columns]

X_fs = df_enc[feature_cols].fillna(0)
y_fs = df_enc['avg_kpi_value'].fillna(0)

rf_fs = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_fs.fit(X_fs, y_fs)

importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_fs.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(importance_df.to_string(index=False))

selected_features = importance_df[
    importance_df['importance'] > importance_df['importance'].mean()
]['feature'].tolist()
if len(selected_features) < 4:
    selected_features = importance_df.head(4)['feature'].tolist()

print(f"\nFitur terpilih untuk clustering: {selected_features}")

plt.figure(figsize=(10, 6))
plt.barh(importance_df['feature'], importance_df['importance'], color='steelblue')
plt.xlabel('Importance')
plt.title('Random Forest Feature Importance')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(PATHS['outputs_clustering'] + 'feature_importance.png', dpi=120)
plt.close()

# ============================================================
# 10. CLUSTERING - 4 METODE
# ============================================================

print("\n" + "="*60)
print("10. CLUSTERING - 4 METODE (BIRCH, GMM, AGGLOMERATIVE, FCM)")
print("="*60)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_enc[selected_features].fillna(0))
joblib.dump(scaler, PATHS['models'] + 'scaler_clustering.pkl')

print(f"Dimensi data         : {X_scaled.shape}")
print(f"Jumlah sample        : {len(X_scaled)}")
print(f"Fitur yang digunakan : {selected_features}")

k_range = range(2, 7)
all_results = {}

# ========== BIRCH ==========
print("\n" + "="*60)
print("🌲 1. BIRCH")
print("="*60)

birch_results = {}
for k in k_range:
    t0 = time.time()
    labels = Birch(n_clusters=k, threshold=0.5).fit_predict(X_scaled)
    elapsed = time.time() - t0
    if len(np.unique(labels)) > 1:
        sil = silhouette_score(X_scaled, labels)
        dbi = davies_bouldin_score(X_scaled, labels)
        ch  = calinski_harabasz_score(X_scaled, labels)
        birch_results[k] = {'labels': labels, 'sil': sil, 'dbi': dbi, 'ch': ch, 'time': elapsed}
        print(f"   {'✅' if sil>0.3 else '⚠️'} K={k}: Silhouette={sil:.4f}, DBI={dbi:.4f}, CH={ch:.1f}, Time={elapsed:.3f}s")

best_k_birch = max(birch_results, key=lambda k: birch_results[k]['sil'])
print(f"\n   ✅ BEST K BIRCH: {best_k_birch} (Silhouette: {birch_results[best_k_birch]['sil']:.4f})")
all_results['BIRCH'] = birch_results

# ========== GMM ==========
print("\n" + "="*60)
print("📊 2. GMM (Gaussian Mixture Model)")
print("="*60)

gmm_results = {}
for k in k_range:
    t0 = time.time()
    gmm = GaussianMixture(n_components=k, random_state=42, n_init=10, covariance_type='full')
    labels = gmm.fit_predict(X_scaled)
    elapsed = time.time() - t0
    if len(np.unique(labels)) > 1:
        sil = silhouette_score(X_scaled, labels)
        dbi = davies_bouldin_score(X_scaled, labels)
        bic = gmm.bic(X_scaled)
        gmm_results[k] = {'labels': labels, 'sil': sil, 'dbi': dbi, 'bic': bic, 'time': elapsed}
        print(f"   {'✅' if sil>0.3 else '⚠️'} K={k}: Silhouette={sil:.4f}, DBI={dbi:.4f}, BIC={bic:.1f}, Time={elapsed:.3f}s")

best_k_gmm = max(gmm_results, key=lambda k: gmm_results[k]['sil'])
print(f"\n   ✅ BEST K GMM: {best_k_gmm} (Silhouette: {gmm_results[best_k_gmm]['sil']:.4f})")
all_results['GMM'] = gmm_results

# ========== AGGLOMERATIVE ==========
print("\n" + "="*60)
print("🔗 3. Agglomerative Clustering")
print("="*60)

agg_results = {}
for k in k_range:
    t0 = time.time()
    labels = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(X_scaled)
    elapsed = time.time() - t0
    if len(np.unique(labels)) > 1:
        sil = silhouette_score(X_scaled, labels)
        dbi = davies_bouldin_score(X_scaled, labels)
        ch  = calinski_harabasz_score(X_scaled, labels)
        agg_results[k] = {'labels': labels, 'sil': sil, 'dbi': dbi, 'ch': ch, 'time': elapsed}
        print(f"   {'✅' if sil>0.3 else '⚠️'} K={k}: Silhouette={sil:.4f}, DBI={dbi:.4f}, CH={ch:.1f}, Time={elapsed:.3f}s")

best_k_agg = max(agg_results, key=lambda k: agg_results[k]['sil'])
print(f"\n   ✅ BEST K Agglomerative: {best_k_agg} (Silhouette: {agg_results[best_k_agg]['sil']:.4f})")
all_results['Agglomerative'] = agg_results

# ========== FCM ==========
print("\n" + "="*60)
print("🌀 4. Fuzzy C-Means (FCM)")
print("="*60)

fcm_results = {}
for k in k_range:
    t0 = time.time()
    try:
        cntr, u, _, _, _, _, fpc = fuzz.cluster.cmeans(
            X_scaled.T, k, 2, error=0.005, maxiter=1000, seed=42
        )
        labels = np.argmax(u, axis=0)
        elapsed = time.time() - t0
        if len(np.unique(labels)) > 1:
            sil = silhouette_score(X_scaled, labels)
            dbi = davies_bouldin_score(X_scaled, labels)
            fcm_results[k] = {'labels': labels, 'sil': sil, 'dbi': dbi, 'fpc': fpc, 'membership': u, 'time': elapsed}
            print(f"   {'✅' if sil>0.3 else '⚠️'} K={k}: Silhouette={sil:.4f}, DBI={dbi:.4f}, FPC={fpc:.4f}, Time={elapsed:.3f}s")
    except Exception as e:
        print(f"   ❌ K={k}: Error - {str(e)[:50]}")

best_k_fcm = max(fcm_results, key=lambda k: fcm_results[k]['sil'])
best_fcm_fpc = fcm_results[best_k_fcm]['fpc']
print(f"\n   ✅ BEST K FCM: {best_k_fcm} (Silhouette: {fcm_results[best_k_fcm]['sil']:.4f}, FPC: {best_fcm_fpc:.4f})")
all_results['FCM'] = fcm_results

# ========== COMPOSITE SCORE ==========
print("\n" + "="*60)
print("🏆 PERBANDINGAN LENGKAP 4 METODE CLUSTERING")
print("="*60)

comparison_data = []
for metode, results in all_results.items():
    for k, v in results.items():
        comparison_data.append({
            'Metode': metode, 'K': k,
            'Silhouette': v['sil'], 'DBI': v['dbi'], 'Waktu': v['time']
        })

comparison_df = pd.DataFrame(comparison_data)

print("\n📊 COMPOSITE SCORE PER K (Silhouette + DBI_norm + K_bonus)")
print("="*60)
print("   Catatan: K=2 diberi penalti karena kurang informatif untuk analisis HR")

composite_results = []
for k in k_range:
    subset = [r for r in comparison_data if r['K'] == k]
    if not subset:
        continue
    sil_best = max(r['Silhouette'] for r in subset)
    dbi_best = min(r['DBI'] for r in subset)

    dbi_norm = 1 / (1 + dbi_best)
    k_bonus = 0.02 if k >= 3 else 0.0
    composite = (sil_best + dbi_norm) / 2 + k_bonus

    composite_results.append({
        'K': k,
        'Best_Silhouette': round(sil_best, 4),
        'Best_DBI': round(dbi_best, 4),
        'Composite_Score': round(composite, 4)
    })

composite_df = pd.DataFrame(composite_results)
best_k_composite = int(composite_df.loc[composite_df['Composite_Score'].idxmax(), 'K'])

for _, row in composite_df.iterrows():
    marker = "⭐ BEST" if row['K'] == best_k_composite else ""
    print(f"   K={int(row['K'])}: Silhouette={row['Best_Silhouette']:.4f} | DBI={row['Best_DBI']:.4f} | Composite={row['Composite_Score']:.4f} {marker}")

print(f"\n🏆 BEST K berdasarkan Composite Score: {best_k_composite}")

# ========== METODE TERBAIK UNTUK K TERPILIH ==========
print("\n" + "="*60)
print(f"📊 METODE TERBAIK UNTUK K={best_k_composite}")
print("="*60)

best_k_data = [r for r in comparison_data if r['K'] == best_k_composite]
best_k_df = pd.DataFrame(best_k_data).sort_values('Silhouette', ascending=False)
print(best_k_df.to_string(index=False))

best_method   = best_k_df.iloc[0]['Metode']
best_sil      = best_k_df.iloc[0]['Silhouette']
best_dbi      = best_k_df.iloc[0]['DBI']

print(f"\n🏆 METODE TERBAIK untuk K={best_k_composite}: {best_method}")
print(f"   Silhouette: {best_sil:.4f}")
print(f"   DBI       : {best_dbi:.4f}")

# ========== AMBIL LABEL FINAL ==========
final_k   = best_k_composite
final_res = all_results[best_method][final_k]
final_labels     = final_res['labels']
final_membership = final_res.get('membership', None)
final_fpc_score  = final_res.get('fpc', 0.0)
final_sil_score  = final_res['sil']
final_dbi_score  = final_res['dbi']

print("\n" + "="*60)
print("🎯 HASIL FINAL BERDASARKAN COMPOSITE SCORE")
print("="*60)
print(f"\n🏆 HASIL FINAL:")
print(f"   Jumlah Cluster (K) = {final_k}")
print(f"   Metode             = {best_method}")
print(f"   Silhouette Score   = {final_sil_score:.4f}")
print(f"   DBI Score          = {final_dbi_score:.4f}")
if best_method == 'FCM':
    print(f"   FPC Score          = {final_fpc_score:.4f}")

# ========== DF CLUSTER RESULT ==========
df_cluster_result = df_clust.copy()
df_cluster_result['cluster'] = final_labels

if final_membership is not None:
    for i in range(final_k):
        df_cluster_result[f'membership_c{i}'] = final_membership[i]

df_cluster_result.to_csv(PATHS['clustering'] + 'hasil_clustering_final.csv', index=False)

print("\nProfil Rata-rata KPI per Cluster:")
cluster_profile = df_cluster_result.groupby('cluster')[
    ['avg_kpi_value', 'persen_tercapai', 'jumlah_proyek']
].mean().round(2)
print(cluster_profile.to_string())

# Plot distribusi cluster
cluster_counts = df_cluster_result['cluster'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
cluster_counts.plot(kind='bar', color='teal', edgecolor='black')
plt.title(f'Distribusi Karyawan per Cluster ({best_method}, K={final_k})')
plt.xlabel('Cluster')
plt.ylabel('Jumlah Karyawan')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(PATHS['outputs_clustering'] + 'final_cluster_distribution.png', dpi=120)
plt.close()

print(f"\n✅ Clustering selesai! Metode terpilih: {best_method} dengan K={final_k}")

# ============================================================
# 11. FORECASTING - Facebook Prophet
# ============================================================

print("\n" + "="*60)
print("11. FORECASTING - Facebook Prophet")
print("="*60)

def calculate_mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def check_stationarity(series):
    try:
        pval = adfuller(series.dropna())[1]
        return pval < 0.05, pval
    except:
        return False, 1.0

df_forecast = df_fore.copy()
df_forecast['periode'] = pd.to_datetime(df_forecast['periode'])

dept_counts = df_forecast.groupby('department_name')['periode'].nunique()
departments = dept_counts[dept_counts >= 24].index.tolist()
skipped = dept_counts[dept_counts < 24].index.tolist()
if skipped:
    print(f"⚠️  Departemen dilewati (data < 24 bulan): {skipped}")

print(f"Departemen yang akan diforecast: {len(departments)} departemen")

forecast_results  = {}
all_metrics       = []
PERIODS           = 6

for dept in departments:
    print(f"\n📊 Memproses departemen: {dept}")

    df_dept = df_forecast[df_forecast['department_name'] == dept].copy()
    df_dept = df_dept.groupby('periode')['avg_kpi'].mean().reset_index()
    df_dept.columns = ['ds', 'y']
    df_dept = df_dept.sort_values('ds').reset_index(drop=True)

    is_stat, pval = check_stationarity(df_dept['y'])
    print(f"  📈 Stasioneritas: p-value={pval:.4f} ({'Stasioner' if is_stat else 'Tidak Stasioner'})")

    Q1, Q3 = df_dept['y'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    n_outlier = ((df_dept['y'] < Q1 - 1.5*IQR) | (df_dept['y'] > Q3 + 1.5*IQR)).sum()
    print(f"  🔍 Outliers: {n_outlier} points")

    model = Prophet(
        growth='linear',
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='additive',
        changepoint_prior_scale=0.05
    )
    model.fit(df_dept)

    future   = model.make_future_dataframe(periods=PERIODS, freq='MS')
    forecast = model.predict(future)

    y_true      = df_dept['y'].values
    y_pred_train = forecast[forecast['ds'].isin(df_dept['ds'])]['yhat'].values[:len(y_true)]

    mae  = mean_absolute_error(y_true, y_pred_train)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred_train))
    mape = calculate_mape(y_true, y_pred_train)

    print(f"  ✅ MAE: {mae:.2f} | RMSE: {rmse:.2f} | MAPE: {mape:.2f}% | Data: {len(df_dept)}")

    forecast_results[dept] = forecast
    all_metrics.append({
        'departemen': dept, 'MAE': round(mae, 2), 'RMSE': round(rmse, 2),
        'MAPE': round(mape, 2), 'data_points': len(df_dept),
        'stasioner': 'Ya' if is_stat else 'Tidak'
    })
    joblib.dump(model, PATHS['models'] + f'prophet_model_{dept.replace(" ", "_").replace("/", "_")}.pkl')

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_dept['ds'], df_dept['y'], 'o-', label='Aktual', color='steelblue', linewidth=2, markersize=5)
    future_fc = forecast[forecast['ds'] > df_dept['ds'].max()]
    ax.plot(future_fc['ds'], future_fc['yhat'], 's--', label='Forecast', color='darkorange', linewidth=2, markersize=5)
    ax.fill_between(future_fc['ds'], future_fc['yhat_lower'], future_fc['yhat_upper'],
                    alpha=0.2, color='darkorange', label='Confidence Interval')
    ax.axvline(df_dept['ds'].max(), color='gray', linestyle=':', label='Batas Aktual')
    ax.set_title(f'Forecast KPI - {dept}\nMAE: {mae:.2f} | RMSE: {rmse:.2f} | MAPE: {mape:.2f}%',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Periode')
    ax.set_ylabel('Rata-rata KPI')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PATHS['outputs_forecasting'] + f'forecast_{dept.replace(" ", "_").replace("/", "_")}.png', dpi=120)
    plt.close()

metrics_df = pd.DataFrame(all_metrics).sort_values('MAPE')
metrics_df.to_csv(PATHS['forecasting'] + 'forecasting_metrics.csv', index=False)

print("\n" + "="*60)
print("📊 RINGKASAN METRIK FORECASTING")
print("="*60)
print(metrics_df.to_string(index=False))
print(f"\n✅ Forecasting selesai untuk {len(forecast_results)} departemen")
print(f"📊 Rata-rata MAPE : {metrics_df['MAPE'].mean():.2f}%")
print(f"📊 Rata-rata MAE  : {metrics_df['MAE'].mean():.2f}")
print(f"📊 Rata-rata RMSE : {metrics_df['RMSE'].mean():.2f}")

# ============================================================
# 12. REGRESSION - LightGBM & NGBoost
# ============================================================

print("\n" + "="*60)
print("12. REGRESSION - METODE JARANG DIPAKAI")
print("="*60)

df_reg = df_regr.copy()
df_reg = pd.merge(
    df_reg,
    df_cluster_result[['employee_id', 'cluster']].drop_duplicates('employee_id'),
    on='employee_id', how='left'
)
df_reg['cluster'] = df_reg['cluster'].fillna(0).astype(int)

for col in ['level_jabatan', 'department_name', 'kpi_category']:
    if col in df_reg.columns:
        le = LabelEncoder()
        df_reg[col] = le.fit_transform(df_reg[col].astype(str))
        joblib.dump(le, PATHS['models'] + f'label_encoder_reg_{col}.pkl')

reg_features = [
    'level_jabatan', 'lama_bekerja_tahun', 'cluster',
    'usia', 'kpi_category', 'department_name', 'project_budget'
]
reg_features = [c for c in reg_features if c in df_reg.columns]

df_reg['level_x_masa']   = df_reg['level_jabatan'] * df_reg['lama_bekerja_tahun']
df_reg['usia_x_cluster'] = df_reg['usia'] * df_reg['cluster']
reg_features += ['level_x_masa', 'usia_x_cluster']

X = df_reg[reg_features].fillna(0)
y = df_reg['rata_kpi_value'].fillna(0)

scaler_reg = StandardScaler()
X_scaled_reg = scaler_reg.fit_transform(X)
joblib.dump(scaler_reg, PATHS['models'] + 'scaler_regression.pkl')

if len(X) > 50000:
    print(f"   Data terlalu besar ({len(X)} samples), melakukan sampling...")
    X_s, _, y_s, _ = train_test_split(X_scaled_reg, y, train_size=50000, random_state=42)
    print(f"   Menggunakan {len(X_s)} samples untuk training")
else:
    X_s, y_s = X_scaled_reg, y

X_train, X_test, y_train, y_test = train_test_split(X_s, y_s, test_size=0.2, random_state=42)
print(f"Dataset: {len(X_train)} train samples, {len(X_test)} test samples, {X.shape[1]} features")

# ===== LIGHTGBM =====
print("\n" + "="*50)
print("🚀 1. LightGBM Regressor")
print("="*50)

lgb_r2 = -999
try:
    import lightgbm as lgb

    lgb_params = {
        'n_estimators': 300, 'learning_rate': 0.05, 'max_depth': 6,
        'num_leaves': 31, 'subsample': 0.8, 'colsample_bytree': 0.8,
        'reg_alpha': 0.1, 'reg_lambda': 0.1, 'random_state': 42, 'verbose': -1
    }
    lgb_reg = lgb.LGBMRegressor(**lgb_params)

    lgb_cv  = cross_val_score(lgb_reg, X_train, y_train, cv=5, scoring='r2')
    lgb_cv_rmse = cross_val_score(lgb_reg, X_train, y_train, cv=5, scoring='neg_root_mean_squared_error')
    print(f"   Cross Validation R²  : {lgb_cv.mean():.4f} ± {lgb_cv.std():.4f}")
    print(f"   Cross Validation RMSE: {(-lgb_cv_rmse).mean():.4f} ± {(-lgb_cv_rmse).std():.4f}")

    lgb_reg.fit(X_train, y_train)
    joblib.dump(lgb_reg, PATHS['models'] + 'lgb_regressor.pkl')

    y_pred_lgb = lgb_reg.predict(X_test)
    lgb_r2   = r2_score(y_test, y_pred_lgb)
    lgb_mae  = mean_absolute_error(y_test, y_pred_lgb)
    lgb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lgb))

    print(f"\n   Test Set Results:")
    print(f"   R²  : {lgb_r2:.4f}")
    print(f"   MAE : {lgb_mae:.4f}")
    print(f"   RMSE: {lgb_rmse:.4f}")

    lgb_importance = pd.DataFrame({
        'feature': reg_features, 'importance': lgb_reg.feature_importances_
    }).sort_values('importance', ascending=False)
    print(f"\n   Feature Importance (LightGBM):")
    print(lgb_importance.to_string(index=False))

except ImportError:
    print("   ❌ LightGBM tidak terinstall. Install: pip install lightgbm")

# ===== NGBOOST =====
print("\n" + "="*50)
print("🎲 2. NGBoost Regressor (Probabilistic - JARANG DIPAKAI)")
print("="*50)

ngb_r2 = -999
try:
    from ngboost import NGBRegressor
    from ngboost.distns import Normal

    X_ngb = X_train[:20000] if len(X_train) > 20000 else X_train
    y_ngb = y_train[:20000] if len(y_train) > 20000 else y_train
    print(f"   NGBoost menggunakan {len(X_ngb)} samples")

    ngb_reg = NGBRegressor(
        n_estimators=200, learning_rate=0.01,
        minibatch_frac=0.5, verbose=False, random_state=42, Dist=Normal
    )
    ngb_cv = cross_val_score(ngb_reg, X_ngb, y_ngb, cv=3, scoring='r2')
    print(f"   Cross Validation R² : {ngb_cv.mean():.4f} ± {ngb_cv.std():.4f}")

    ngb_reg.fit(X_ngb, y_ngb)
    joblib.dump(ngb_reg, PATHS['models'] + 'ngb_regressor.pkl')

    y_pred_ngb = ngb_reg.predict(X_test)
    ngb_r2   = r2_score(y_test, y_pred_ngb)
    ngb_mae  = mean_absolute_error(y_test, y_pred_ngb)
    ngb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_ngb))

    print(f"\n   Test Set Results:")
    print(f"   R²  : {ngb_r2:.4f}")
    print(f"   MAE : {ngb_mae:.4f}")
    print(f"   RMSE: {ngb_rmse:.4f}")

except ImportError:
    print("   ❌ NGBoost tidak terinstall. Install: pip install ngboost")

# ===== PERBANDINGAN =====
print("\n" + "="*60)
print("🏆 PERBANDINGAN HASIL REGRESSION")
print("="*60)

comparison_reg = []
if lgb_r2 != -999:
    comparison_reg.append({'Metode': 'LightGBM', 'R²': lgb_r2, 'MAE': lgb_mae, 'RMSE': lgb_rmse})
if ngb_r2 != -999:
    comparison_reg.append({'Metode': 'NGBoost',  'R²': ngb_r2, 'MAE': ngb_mae, 'RMSE': ngb_rmse})

if comparison_reg:
    comp_df = pd.DataFrame(comparison_reg).sort_values('R²', ascending=False)
    print("\n📊 Ranking Metode Regresi (berdasarkan R²):")
    print(comp_df.to_string(index=False))

    best_reg_method = comp_df.iloc[0]['Metode']
    r2   = comp_df.iloc[0]['R²']
    mae  = comp_df.iloc[0]['MAE']
    rmse = comp_df.iloc[0]['RMSE']

    if best_reg_method == 'LightGBM':
        final_y_pred    = y_pred_lgb
        final_importance = lgb_importance
    else:
        final_y_pred     = y_pred_ngb
        final_importance = pd.DataFrame({'feature': reg_features, 'importance': [0]*len(reg_features)})

    print(f"\n🏆 METODE REGRESI TERBAIK: {best_reg_method} (R² = {r2:.4f})")
else:
    print("   ❌ Tidak ada metode regresi yang berhasil dijalankan")
    best_reg_method = 'None'
    r2 = mae = rmse = 0
    final_y_pred    = None
    final_importance = pd.DataFrame()

# Plot scatter aktual vs prediksi
if final_y_pred is not None:
    plt.figure(figsize=(8, 8))
    plt.scatter(y_test, final_y_pred, alpha=0.4, color='steelblue', edgecolors='white', linewidth=0.3)
    mn, mx = y_test.min(), y_test.max()
    plt.plot([mn, mx], [mn, mx], 'r--', linewidth=2, label='Ideal')
    plt.xlabel('KPI Aktual')
    plt.ylabel('KPI Prediksi')
    plt.title(f'{best_reg_method} - Aktual vs Prediksi\nR² = {r2:.4f}', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PATHS['outputs_regression'] + 'regression_best_scatter.png', dpi=120)
    plt.close()

if not final_importance.empty:
    final_importance.to_csv(PATHS['regression'] + 'feature_importance_regression.csv', index=False)
print("\n✅ Feature importance regression disimpan")
print(f"\n✅ Regression selesai! Metode terpilih: {best_reg_method} (R² = {r2:.4f})")

# ============================================================
# 13 & 14. SIMPAN DATA DASHBOARD
# ============================================================

print("\n" + "="*60)
print("13. MENYIMPAN DATA UNTUK DASHBOARD")
print("="*60)

print(f"   Clustering Final : {best_method} dengan K={final_k}")
print(f"   Silhouette Score : {final_sil_score:.4f}")
print(f"   FPC Score        : {final_fpc_score:.4f}")

# Simpan ke folder masing-masing
df_cluster_result.to_csv(PATHS['clustering'] + 'data_clustering.csv', index=False)
df_fore.to_csv(PATHS['forecasting'] + 'data_forecasting.csv', index=False)
df_regr.to_csv(PATHS['regression'] + 'data_regression.csv', index=False)

summary_stats = {
    'total_employees': len(df_dim_employee),
    'total_projects':  len(df_dim_project),
    'total_kpi_records': len(df_fact),
    'clusters_used':   final_k,
    'silhouette_score': final_sil_score,
    'fpc_score':        final_fpc_score,
    'regression_r2':    r2,
    'regression_rmse':  rmse,
    'regression_method': best_reg_method
}
pd.DataFrame([summary_stats]).to_csv(PATHS['data'] + 'summary_statistics.csv', index=False)
print("✅ Data untuk dashboard disimpan")

print("\n" + "="*60)
print("14. MENYIMPAN DATA UNTUK STREAMLIT DASHBOARD")
print("="*60)

# 1. cluster_results
df_cluster_result.to_csv(PATHS['clustering'] + 'cluster_results.csv', index=False)
print("✅ cluster_results.csv disimpan")

# 2. cluster_summary
cluster_summary = df_cluster_result.groupby('cluster').agg(
    avg_kpi=('avg_kpi_value', 'mean'),
    pencapaian=('persen_tercapai', 'mean'),
    rata_usia=('usia', 'mean'),
    rata_masa_kerja=('lama_bekerja_tahun', 'mean'),
    jumlah_karyawan=('employee_id', 'count')
).round(2).reset_index()
cluster_summary.to_csv(PATHS['clustering'] + 'cluster_summary.csv', index=False)
print("✅ cluster_summary.csv disimpan")

# 3. dept_performance
dept_performance = df_cluster_result.groupby('department_name').agg(
    avg_kpi=('avg_kpi_value', 'mean'),
    pencapaian=('persen_tercapai', 'mean'),
    jumlah_karyawan=('employee_id', 'count')
).round(2).reset_index()
dept_performance.columns = ['departemen', 'avg_kpi', 'pencapaian_%', 'jumlah_karyawan']
dept_performance.to_csv(PATHS['clustering'] + 'dept_performance.csv', index=False)
print("✅ dept_performance.csv disimpan")

# 4. forecast_data
df_fore.to_csv(PATHS['forecasting'] + 'forecast_data.csv', index=False)
print("✅ forecast_data.csv disimpan")

# 5. regression_data
df_regr.merge(
    df_cluster_result[['employee_id', 'cluster']].drop_duplicates('employee_id'),
    on='employee_id', how='left'
).to_csv(PATHS['regression'] + 'regression_data.csv', index=False)
print("✅ regression_data.csv disimpan")

# 6. feature importance (clustering & regresi)
importance_df.to_csv(PATHS['clustering'] + 'feature_importance.csv', index=False)
if not final_importance.empty:
    final_importance.to_csv(PATHS['regression'] + 'feature_importance_regression.csv', index=False)
print("✅ feature importance disimpan")

# 7. dashboard_summary
dashboard_summary = {
    'total_employees':    len(df_dim_employee),
    'total_projects':     len(df_dim_project),
    'total_kpi_records':  len(df_fact),
    'clusters_used':      final_k,
    'silhouette_score':   round(final_sil_score, 4),
    'fpc_score':          round(final_fpc_score, 4),
    'regression_r2':      round(r2, 4),
    'regression_rmse':    round(rmse, 4),
    'dept_forecasted':    len(forecast_results),
    'clustering_method':  best_method,
    'regression_method':  best_reg_method
}
pd.DataFrame([dashboard_summary]).to_csv(PATHS['data'] + 'dashboard_summary.csv', index=False)
print("✅ dashboard_summary.csv disimpan")

# Simpan juga dimensi dan fakta ke folder masing-masing
df_dim_employee.to_csv(PATHS['dimensions'] + 'dim_employee.csv', index=False)
df_dim_project.to_csv(PATHS['dimensions'] + 'dim_project.csv', index=False)
df_dim_kpi.to_csv(PATHS['dimensions'] + 'dim_kpi.csv', index=False)
df_fact.to_csv(PATHS['facts'] + 'fact_project_kpi.csv', index=False)
print("✅ dimension dan fact tables disimpan")

print("\n" + "="*60)
print("✅ SEMUA DATA UNTUK STREAMLIT DASHBOARD TERSIMPAN!")
print("   Folder: data/dimensions/, data/facts/, data/clustering/,")
print("          data/forecasting/, data/regression/, data/outputs/")
print("="*60)