# generate_better_data.py - FIXED VERSION
import pymysql
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta, date

fake = Faker('id_ID')
np.random.seed(42)
random.seed(42)

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
print("🌟 GENERATING HIGH QUALITY DATA - v4.1 (FIXED CEILING)")
print("=" * 60)

# ============================================================
# 1. PERSONA dengan BASE YANG LEBIH REALISTIS (tidak terlalu tinggi)
# ============================================================
print("1. Loading employee data dan assign persona...")

cursor.execute("""
    SELECT e.employee_id, e.department_id, e.hire_date,
           p.level_jabatan, d.department_name
    FROM employee e
    JOIN position p ON e.position_id = p.position_id
    JOIN department d ON e.department_id = d.department_id
""")
employees_raw = cursor.fetchall()

# 6 PERSONA dengan BASE KPI YANG REALISTIS (max 88, tidak kena ceiling 100)
PERSONAS = {
    0: {  # HIGH PERFORMER - Elite
        'name': 'High Performer',
        'kpi_base': 88,      # Turun dari 94 (biar tidak kena ceiling 100)
        'kpi_std': 3,
        'levels': ['Manager', 'Senior Manager', 'Head of Department', 'Director'],
        'tenure_min': 7,
    },
    1: {  # TOP TALENT
        'name': 'Top Talent',
        'kpi_base': 80,      # Gap 8 poin
        'kpi_std': 3.5,
        'levels': ['Team Lead', 'Assistant Manager', 'Senior Manager'],
        'tenure_min': 4,
    },
    2: {  # SOLID PERFORMER
        'name': 'Solid Performer',
        'kpi_base': 72,      # Gap 8 poin
        'kpi_std': 4,
        'levels': ['Senior Staff', 'Team Lead', 'Assistant Manager'],
        'tenure_min': 3,
    },
    3: {  # AVERAGE PERFORMER
        'name': 'Average Performer',
        'kpi_base': 62,      # Gap 10 poin
        'kpi_std': 4.5,
        'levels': ['Staff', 'Senior Staff'],
        'tenure_min': 1,
    },
    4: {  # NEEDS IMPROVEMENT
        'name': 'Needs Improvement',
        'kpi_base': 48,      # Gap 14 poin
        'kpi_std': 5,
        'levels': ['Staff', 'Senior Staff'],
        'tenure_min': 0,
    },
    5: {  # VETERAN
        'name': 'Veteran',
        'kpi_base': 58,      # Antara Average dan Needs
        'kpi_std': 4,
        'levels': ['Senior Staff', 'Staff', 'Team Lead'],
        'tenure_min': 8,
    }
}

LEVEL_HIERARCHY = {
    'Staff': 0,
    'Senior Staff': 1,
    'Team Lead': 2,
    'Assistant Manager': 3,
    'Manager': 4,
    'Senior Manager': 5,
    'Head of Department': 6,
    'Director': 7
}

DEPT_PERFORMANCE = {
    'IT': 1.05,
    'Research & Development': 1.04,
    'Quality Assurance': 1.03,
    'Finance': 1.02,
    'Corporate Strategy': 1.02,
    'Marketing': 1.01,
    'Sales': 1.01,
    'Design': 1.00,
    'Operations': 1.00,
    'Human Resources': 0.99,
    'Legal': 0.98,
    'Production': 0.98,
    'Customer Service': 0.97,
    'Procurement': 0.97,
    'Logistics': 0.96,
}

# Assign persona
employee_personas = {}
employee_info = {}

today = date.today()
for emp_id, dept_id, hire_date, level, dept_name in employees_raw:
    if hire_date:
        tenure = (today - hire_date).days / 365
    else:
        tenure = random.uniform(1, 10)

    level_rank = LEVEL_HIERARCHY.get(level, 0)

    # Assign persona
    if level_rank >= 5:
        persona = 0
    elif level_rank >= 3 and tenure >= 5:
        persona = 1
    elif level_rank >= 2 and tenure >= 4:
        persona = 2
    elif level_rank >= 1 and tenure >= 8:
        persona = 5
    elif level_rank >= 1 and tenure < 3:
        persona = 4
    elif level_rank == 0 and tenure < 2:
        persona = 4
    else:
        persona = 3

    employee_personas[emp_id] = persona
    employee_info[emp_id] = {
        'dept_id': dept_id,
        'dept_name': dept_name,
        'level': level,
        'level_rank': level_rank,
        'tenure': tenure
    }

from collections import Counter
persona_dist = Counter(employee_personas.values())
print(f"\n   Distribusi Persona:")
for p_id, count in sorted(persona_dist.items()):
    print(f"   Persona {p_id} ({PERSONAS[p_id]['name']:20}): {count:3d} karyawan")
    print(f"          Base KPI: {PERSONAS[p_id]['kpi_base']} (Std: {PERSONAS[p_id]['kpi_std']})")

# ============================================================
# 2. UPDATE KPI TARGETS
# ============================================================
print("\n2. Updating KPI targets...")

cursor.execute("SELECT kpi_id, kpi_category FROM kpi")
kpis = cursor.fetchall()

KPI_TARGETS = {
    'Time Management': 80,
    'Efficiency': 80,
    'Finance': 82,
    'Quality': 85,
    'Development': 75,
    'HR': 88,
    'Performance': 80,
    'Attendance': 90,
    'Innovation': 72,
    'Teamwork': 83,
    'Project': 78,
    'Technical': 82,
}

for kpi_id, category in kpis:
    target = KPI_TARGETS.get(category, 80)
    cursor.execute("UPDATE kpi SET kpi_target = %s WHERE kpi_id = %s", (target, kpi_id))

cursor.execute("SELECT kpi_id, kpi_category, kpi_target FROM kpi")
kpis = cursor.fetchall()
print(f"   ✅ Updated {len(kpis)} KPI targets")

KPI_CATEGORY_BIAS = {
    'Attendance': 4,
    'Teamwork': 2,
    'HR': 1,
    'Quality': -2,
    'Finance': -2,
    'Innovation': -4,
    'Development': -3,
}

# ============================================================
# 3. CLEAR OLD DATA
# ============================================================
print("\n3. Clearing old data...")
cursor.execute("DELETE FROM project_kpi_fact")
conn.commit()

cursor.execute("SELECT project_id, project_start_date, project_end_date FROM project")
projects = cursor.fetchall()
project_list = [p[0] for p in projects]
print(f"   ✅ Cleared. {len(project_list)} projects available.")

# ============================================================
# 4. DATE RANGE 36 BULAN
# ============================================================
print("\n4. Generating 36-month date range...")

end_date = today
start_date = today - timedelta(days=36*30)

monthly_dates = []
current = start_date
while current <= end_date:
    monthly_dates.append(current)
    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1)
    else:
        current = current.replace(month=current.month + 1)

print(f"   Range: {start_date} sampai {end_date}")
print(f"   Total bulan: {len(monthly_dates)}")

# SEASONAL PATTERN
SEASONAL_DEPT = {
    'Sales': [0.94, 0.93, 0.96, 0.98, 1.00, 1.02, 1.01, 1.03, 1.04, 1.06, 1.07, 1.09],
    'Finance': [1.06, 1.04, 1.03, 1.00, 0.98, 0.97, 0.96, 0.97, 0.98, 1.00, 1.02, 1.05],
    'IT': [1.00, 1.01, 1.02, 1.01, 1.00, 0.99, 0.98, 0.97, 1.00, 1.01, 1.02, 1.01],
    'Operations': [1.02, 1.01, 1.00, 1.00, 1.01, 1.02, 1.01, 1.00, 0.99, 0.99, 1.00, 1.01],
    'Marketing': [0.95, 0.96, 1.00, 1.02, 1.03, 1.02, 1.01, 1.00, 1.02, 1.03, 1.04, 1.05],
    'Human Resources': [1.01, 1.00, 1.01, 1.02, 1.01, 1.00, 0.99, 0.99, 1.01, 1.01, 1.00, 1.02],
    'Production': [1.00, 1.00, 1.01, 1.02, 1.02, 1.01, 0.99, 0.99, 1.00, 1.01, 1.01, 1.02],
    'Quality Assurance': [1.02, 1.01, 1.01, 1.00, 1.00, 0.99, 0.99, 1.00, 1.01, 1.01, 1.01, 1.02],
    'Logistics': [0.96, 0.97, 0.99, 1.01, 1.01, 1.00, 1.00, 1.01, 1.02, 1.03, 1.04, 1.06],
    'Research & Development': [1.01, 1.01, 1.02, 1.02, 1.01, 1.00, 0.99, 0.99, 1.00, 1.01, 1.01, 1.01],
    'Customer Service': [0.97, 0.97, 0.98, 1.00, 1.01, 1.02, 1.01, 1.00, 1.01, 1.02, 1.03, 1.04],
    'Design': [1.00, 1.00, 1.01, 1.02, 1.02, 1.01, 1.00, 1.00, 1.01, 1.01, 1.01, 1.01],
    'Legal': [1.00, 1.00, 1.01, 1.01, 1.01, 1.00, 0.99, 0.99, 1.00, 1.01, 1.01, 1.01],
    'Procurement': [1.00, 1.00, 1.01, 1.01, 1.00, 0.99, 0.99, 1.00, 1.01, 1.02, 1.01, 1.01],
    'Corporate Strategy': [1.01, 1.01, 1.02, 1.01, 1.00, 0.99, 0.99, 1.00, 1.01, 1.02, 1.02, 1.01],
}

TREND_DEPT = {
    'IT': 0.002,
    'Research & Development': 0.0025,
    'Marketing': 0.001,
    'Sales': 0.001,
    'Corporate Strategy': 0.0015,
    'Quality Assurance': 0.0005,
    'Operations': 0.0005,
    'Production': 0.0005,
    'Finance': 0.0,
    'Human Resources': 0.0,
    'Design': 0.0005,
    'Legal': -0.0005,
    'Logistics': -0.0005,
    'Customer Service': 0.0,
    'Procurement': 0.0,
}

# ============================================================
# 5. GENERATE KPI RECORDS
# ============================================================
print("\n5. Generating KPI records...")

insert_sql = """
    INSERT INTO project_kpi_fact (project_id, employee_id, kpi_id, evaluation_date, kpi_value)
    VALUES (%s, %s, %s, %s, %s)
"""
batch_data = []
counter = 0

# Assign waktu untuk setiap proyek
project_time_ranges = {}
for i, proj_id in enumerate(project_list):
    quarter_idx = i % 36
    proj_start_month = monthly_dates[min(quarter_idx, len(monthly_dates)-3)]
    proj_end_month = monthly_dates[min(quarter_idx + 2, len(monthly_dates)-1)]
    project_time_ranges[proj_id] = (proj_start_month, proj_end_month)

# Generate records
for emp_id, persona_id in employee_personas.items():
    persona = PERSONAS[persona_id]
    emp = employee_info[emp_id]
    dept_name = emp['dept_name']
    level_rank = emp['level_rank']
    tenure = emp['tenure']

    dept_mult = DEPT_PERFORMANCE.get(dept_name, 1.0)
    
    # Level bonus (lebih kecil agar tidak kena ceiling)
    level_bonus = level_rank * 1.5  # Max 10.5 poin (dari 7 level)
    
    # Tenure bonus (max 8 poin)
    tenure_bonus = min(8, tenure * 0.8)

    n_projects = min(8, len(project_list))
    selected_projects = random.sample(project_list, n_projects)

    for project_id in selected_projects:
        proj_start, proj_end = project_time_ranges[project_id]

        n_evals = random.randint(1, 3)
        
        for eval_num in range(n_evals):
            date_range_days = (proj_end - proj_start).days
            eval_date = proj_start + timedelta(days=random.randint(0, max(0, date_range_days)))

            month_idx = eval_date.month - 1
            month_offset = (eval_date - start_date).days / 30

            seasonal = SEASONAL_DEPT.get(dept_name, [1.0]*12)[month_idx]
            trend = TREND_DEPT.get(dept_name, 0.0) * month_offset
            trend_mult = 1.0 + trend

            for kpi_id, category, target in kpis:
                category_bias = KPI_CATEGORY_BIAS.get(category, 0)

                # FORMULA UTAMA
                base = float(persona['kpi_base'])
                base += level_bonus
                base += tenure_bonus
                base += category_bias
                base *= dept_mult
                base *= seasonal
                base *= trend_mult

                # Noise
                noise = np.random.normal(0, persona['kpi_std'])
                kpi_value = base + noise

                # Clamp realistis (30-98, hindari ceiling 100)
                kpi_value = max(30, min(98, kpi_value))

                counter += 1
                batch_data.append((
                    project_id,
                    emp_id,
                    kpi_id,
                    eval_date,
                    round(float(kpi_value), 2)
                ))

                if len(batch_data) >= 5000:
                    cursor.executemany(insert_sql, batch_data)
                    conn.commit()
                    print(f"   📊 Inserted {counter:,} records...", end='\r')
                    batch_data = []

if batch_data:
    cursor.executemany(insert_sql, batch_data)
    conn.commit()

print(f"\n   ✅ Generated {counter:,} KPI records!")

# ============================================================
# 6. SAVE PERSONA
# ============================================================
print("\n6. Saving persona assignments...")

try:
    cursor.execute("ALTER TABLE employee ADD COLUMN persona_cluster INT DEFAULT NULL")
    conn.commit()
    print("   ✅ Kolom persona_cluster ditambahkan")
except Exception as e:
    if "Duplicate column" in str(e):
        print("   ℹ️  Kolom persona_cluster sudah ada")
    else:
        print(f"   ⚠️  {e}")

for emp_id, persona_id in employee_personas.items():
    cursor.execute(
        "UPDATE employee SET persona_cluster = %s WHERE employee_id = %s",
        (persona_id, emp_id)
    )
conn.commit()
print("   ✅ Persona tersimpan")

# ============================================================
# 7. VERIFIKASI (diperbaiki querynya)
# ============================================================
print("\n" + "=" * 60)
print("📊 VERIFIKASI HASIL")
print("=" * 60)

# Statistik umum
cursor.execute("""
    SELECT 
        ROUND(AVG(kpi_value), 2) as avg_kpi,
        ROUND(MIN(kpi_value), 2) as min_kpi,
        ROUND(MAX(kpi_value), 2) as max_kpi,
        ROUND(STD(kpi_value), 2) as std_kpi,
        COUNT(*) as total
    FROM project_kpi_fact
""")
stats = cursor.fetchone()
print(f"\n📈 KPI Statistics:")
print(f"   Total Records : {stats[4]:,}")
print(f"   Average       : {stats[0]}")
print(f"   Min / Max     : {stats[1]} / {stats[2]}")
print(f"   Std Dev       : {stats[3]}")

# KPI per persona
cursor.execute("""
    SELECT 
        e.persona_cluster,
        ROUND(AVG(pkf.kpi_value), 2) as avg_kpi,
        ROUND(STD(pkf.kpi_value), 2) as std_kpi,
        COUNT(DISTINCT e.employee_id) as n_emp
    FROM project_kpi_fact pkf
    JOIN employee e ON pkf.employee_id = e.employee_id
    WHERE e.persona_cluster IS NOT NULL
    GROUP BY e.persona_cluster
    ORDER BY avg_kpi DESC
""")
print(f"\n📊 KPI per Persona Cluster:")
print(f"   {'Persona':>8} | {'Avg KPI':>8} | {'Std':>6} | {'Karyawan':>9} | Nama")
rows = cursor.fetchall()
for i, row in enumerate(rows):
    persona_id = row[0]
    name = PERSONAS.get(persona_id, {}).get('name', 'Unknown')
    base_target = PERSONAS.get(persona_id, {}).get('kpi_base', 0)
    print(f"   Persona {persona_id:>1} | {row[1]:>8} | {row[2]:>6} | {row[3]:>9} | {name} (base:{base_target})")
    if i > 0:
        gap = rows[i-1][1] - row[1]
        print(f"           ↓ GAP: {gap:.1f} poin")

# KPI per level (untuk regresi)
cursor.execute("""
    SELECT 
        p.level_jabatan,
        ROUND(AVG(pkf.kpi_value), 2) as avg_kpi,
        COUNT(*) as n,
        ROUND(MIN(pkf.kpi_value), 2) as min_val,
        ROUND(MAX(pkf.kpi_value), 2) as max_val
    FROM project_kpi_fact pkf
    JOIN employee e ON pkf.employee_id = e.employee_id
    JOIN position p ON e.position_id = p.position_id
    GROUP BY p.level_jabatan
    ORDER BY avg_kpi DESC
""")
print(f"\n📊 KPI per Level:")
level_results = cursor.fetchall()
for row in level_results:
    bar = "█" * int(float(row[1]) / 3)
    print(f"   {row[0]:25} | {row[1]:5.1f} {bar} (range: {row[3]:.0f}-{row[4]:.0f})")

# Range temporal
cursor.execute("""
    SELECT 
        MIN(evaluation_date) as earliest,
        MAX(evaluation_date) as latest,
        COUNT(DISTINCT DATE_FORMAT(evaluation_date, '%%Y-%%m')) as n_months
    FROM project_kpi_fact
""")
temporal = cursor.fetchone()
print(f"\n📅 Temporal Coverage:")
print(f"   Earliest : {temporal[0]}")
print(f"   Latest   : {temporal[1]}")
print(f"   Months   : {temporal[2]}")

# Top departemen
cursor.execute("""
    SELECT d.department_name, 
           ROUND(AVG(pkf.kpi_value), 2) as avg_kpi,
           COUNT(*) as n_records
    FROM project_kpi_fact pkf
    JOIN employee e ON pkf.employee_id = e.employee_id
    JOIN department d ON e.department_id = d.department_id
    GROUP BY d.department_name
    ORDER BY avg_kpi DESC
    LIMIT 5
""")
print(f"\n📊 Top 5 Departemen:")
for row in cursor.fetchall():
    print(f"   {row[0]:25} | {row[1]:.2f} ({row[2]:,} records)")

cursor.close()
conn.close()

print("\n" + "=" * 60)
print("✅ DATA GENERATION SELESAI!")
print("=" * 60)
print(f"""
📊 Ringkasan:
   Total Records : {counter:,}
   Periode Data  : 36 bulan
   Jumlah Cluster: 6 persona
   
🎯 Perubahan:
   1. BASE KPI: [88, 80, 72, 62, 48, 58] → tidak kena ceiling 100
   2. Max clamp: 98 (bukan 100) → menghindari ceiling effect
   3. Level bonus lebih kecil (1.5 per level)
   
🚀 Jalankan: python scripts/datamart.py
""")