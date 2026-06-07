# backup_data.py
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='root',
    password='',
    database='hr_project_db',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("=" * 60)
print("BACKUP DATA SEBELUM GENERATE ULANG")
print("=" * 60)

# Backup employee
cursor.execute("DROP TABLE IF EXISTS employee_backup")
cursor.execute("CREATE TABLE employee_backup AS SELECT * FROM employee")
print("✅ Backup employee → employee_backup")

# Backup project_kpi_fact
cursor.execute("DROP TABLE IF EXISTS project_kpi_fact_backup")
cursor.execute("CREATE TABLE project_kpi_fact_backup AS SELECT * FROM project_kpi_fact")
print("✅ Backup project_kpi_fact → project_kpi_fact_backup")

conn.commit()

# Cek backup
cursor.execute("SELECT COUNT(*) FROM employee_backup")
emp_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM project_kpi_fact_backup")
fact_count = cursor.fetchone()[0]

print(f"\n📊 Backup Summary:")
print(f"   employee_backup: {emp_count} rows")
print(f"   project_kpi_fact_backup: {fact_count} rows")

cursor.close()
conn.close()

print("\n✅ Backup selesai! Data aman.")
print("🚀 Silakan jalankan generate_better_data.py sekarang")