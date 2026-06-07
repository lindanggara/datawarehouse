# cek_db.py
import pymysql
import pandas as pd
from sqlalchemy import create_engine, inspect

# Koneksi ke database (sesuaikan dengan konfigurasi Anda)
DB_HOST = "localhost"
DB_PORT = "3307"  # atau "3306" jika default XAMPP
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "hr_project_db"

# Buat koneksi
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("=" * 60)
print("CHECKING DATABASE STRUCTURE")
print("=" * 60)

# 1. Lihat semua tabel
inspector = inspect(engine)
tables = inspector.get_table_names()

print("\n📋 TABLES FOUND:")
for table in tables:
    print(f"   - {table}")

# 2. Lihat struktur setiap tabel
print("\n" + "=" * 60)
print("TABLE STRUCTURES:")
print("=" * 60)

for table in tables:
    print(f"\n📋 TABLE: {table}")
    print("-" * 50)
    
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"   {col['name']:25} {str(col['type']):20} Nullable: {col['nullable']}")
    
    # Lihat sample data
    try:
        df = pd.read_sql(f"SELECT * FROM {table} LIMIT 3", engine)
        if len(df) > 0:
            print(f"\n   Sample data:")
            for idx, row in df.iterrows():
                print(f"   Row {idx+1}:", dict(row))
    except Exception as e:
        print(f"   Error reading data: {e}")

# 3. Hitung jumlah data per tabel
print("\n" + "=" * 60)
print("ROW COUNTS:")
print("=" * 60)
for table in tables:
    df = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine)
    count = df['count'].iloc[0]
    print(f"   {table}: {count} rows")

print("\n✅ Done!")