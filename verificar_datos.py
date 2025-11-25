import pandas as pd
import os

file_path = "output_data/mental_health_final.parquet"

if os.path.exists(file_path):
    df = pd.read_parquet(file_path)
    print("--- COLUMNAS ENCONTRADAS ---")
    print(df.columns.tolist())
    
    print("\n--- MUESTRA DE DATOS DE EDAD ---")
    if 'age_group' in df.columns:
        print(df['age_group'].head())
    else:
        print("❌ ERROR: La columna 'age_group' NO existe. Debes correr el DAG de nuevo.")

    print("\n--- MUESTRA DE DATOS DE SECTOR ---")
    if 'sector' in df.columns:
        print(df['sector'].head())
    else:
        print("❌ ERROR: La columna 'sector' NO existe. Debes correr el DAG de nuevo.")
else:
    print("El archivo no existe.")