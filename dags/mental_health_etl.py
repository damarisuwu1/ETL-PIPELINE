from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging
import os

OUTPUT_PATH = "/tmp/airflow_data_mental/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# --- TAREA 1: EXTRACCIÓN CON GÉNERO ---
def extract_mental_health_data(**kwargs):
    logging.info("Generando Dataset con Demografía Completa...")
    try:
        num_records = 6000
        np.random.seed(42)

        # 1. EDAD
        ages = np.random.randint(22, 65, num_records)
        
        # 2. GÉNERO (NUEVO)
        genders = np.random.choice(['Hombre', 'Mujer', 'No Binario'], num_records, p=[0.48, 0.48, 0.04])

        # 3. SECTOR
        sectors_opts = ['Tecnología', 'Salud', 'Finanzas', 'Educación', 'Construcción', 'Retail']
        sectors = np.random.choice(sectors_opts, num_records)

        # 4. FUENTES Y MÉTODOS
        stress_source = np.random.choice(['Carga Laboral', 'Finanzas', 'Familia', 'Salud'], num_records)
        destress_method = np.random.choice(['Deporte', 'Naturaleza', 'Videojuegos', 'Socializar'], num_records)

        # 5. CÁLCULO DE ESTRÉS (Con sesgo demográfico para que la matriz se vea bien)
        base_stress = np.random.normal(5.5, 1.5, num_records)
        stress_level = base_stress.copy()
        
        # Simulamos que la Gen Z (gente joven) reporta más estrés
        stress_level[ages < 30] += 0.8
        # Simulamos que el sector Salud tiene más estrés
        stress_level[sectors == 'Salud'] += 1.0
        
        # Clip final
        stress_level = np.clip(stress_level, 1, 10).astype(int)

        data = {
            'employee_id': np.arange(num_records),
            'age_raw': ages,
            'gender': genders, # <--- IMPORTANTE
            'sector': sectors,
            'stress_level': stress_level,
            'stress_source': stress_source,
            'destress_method': destress_method,
            'sleep_hours': np.random.normal(6.5, 1.5, num_records)
        }
        
        df = pd.DataFrame(data)
        filename = f"{OUTPUT_PATH}raw_mental_health.csv"
        df.to_csv(filename, index=False)
        return filename

    except Exception as e:
        logging.error(f"Error CRÍTICO: {e}")
        raise e

# --- TAREA 2: TRANSFORMACIÓN ---
def transform_mental_health_data(ti, **kwargs):
    input_file = ti.xcom_pull(task_ids='extract_task')
    df = pd.read_csv(input_file)
    
    # Grupos de edad
    bins = [20, 30, 40, 50, 100]
    labels = ['Gen Z (20-29)', 'Millennials (30-39)', 'Gen X (40-49)', 'Boomers (50+)']
    df['age_group'] = pd.cut(df['age_raw'], bins=bins, labels=labels)
    
    # Categoría de Riesgo
    conditions = [
        (df['stress_level'] >= 8),
        (df['stress_level'] >= 5) & (df['stress_level'] < 8),
        (df['stress_level'] < 5)
    ]
    choices = ['Alto Riesgo', 'Riesgo Moderado', 'Bajo Riesgo']
    df['risk_category'] = np.select(conditions, choices, default='Riesgo Moderado')
    
    output_file = f"{OUTPUT_PATH}clean_mental_health.csv"
    df.to_csv(output_file, index=False)
    return output_file

# --- TAREA 3: CARGA ---
def load_data(ti, **kwargs):
    input_file = ti.xcom_pull(task_ids='transform_task')
    df = pd.read_csv(input_file)
    output_parquet = f"{OUTPUT_PATH}mental_health_final.parquet"
    df.to_parquet(output_parquet, engine='pyarrow')

# DAG
default_args = {'owner': 'student', 'retries': 1, 'retry_delay': timedelta(seconds=30)}
with DAG('mental_health_etl_matrix', default_args=default_args, schedule_interval='@daily', start_date=datetime(2023,1,1), catchup=False) as dag:
    t1 = PythonOperator(task_id='extract_task', python_callable=extract_mental_health_data)
    t2 = PythonOperator(task_id='transform_task', python_callable=transform_mental_health_data)
    t3 = PythonOperator(task_id='load_task', python_callable=load_data)
    t1 >> t2 >> t3