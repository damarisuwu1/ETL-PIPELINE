
# 🏥 Proyecto ETL: Análisis de Salud Mental y Riesgo de Burnout Laboral

Este proyecto implementa una tubería de datos (ETL) automatizada utilizando **Apache Airflow** y **Docker** para procesar datos simulados de salud mental en el entorno corporativo. El resultado final es un Dashboard interactivo diseñado en **Python (Plotly)** que permite identificar riesgos de "Burnout" y proponer estrategias de bienestar efectivas.

---

## 📋 Fase 1: Justificación del Problema

**Relevancia, Problema y Beneficiarios**
El análisis de la salud mental laboral es vital hoy en día, ya que el estrés crónico impacta directamente en la economía (pérdida de productividad) y el bienestar social **(Relevancia)**. El problema principal que aborda este proyecto es la detección tardía del "Burnout" y la falta de comprensión sobre qué factores (sector, edad o hábitos) lo provocan realmente **(Problema)**. Los beneficiarios directos de estos insights son los departamentos de Recursos Humanos y Salud Ocupacional, quienes pueden pasar de soluciones genéricas a estrategias preventivas personalizadas para mejorar la calidad de vida de los empleados **(Beneficiarios)**.

---

## ⚙️ Fase 2: Arquitectura de la Tubería ETL (Airflow)

El proceso ETL se orquesta mediante un DAG en Airflow (`mental_health_etl_matrix`) que se ejecuta diariamente.

### 1. Extract (Extracción)
* **Fuente:** Generación de datos sintéticos mediante `NumPy` y `Pandas`.
* **Volumen:** 6,000 registros simulados.
* **Variables:** Incluye datos demográficos (Edad, Género), laborales (Sector, Horas de Trabajo) y de salud (Horas de Sueño, Nivel de Estrés, Métodos de Desestrés).

### 2. Transform (Transformación)
* **Limpieza:** Manejo de tipos de datos y validación de rangos.
* **Feature Engineering:**
    * Creación de `age_group` (Grupos generacionales: Gen Z, Millennials, etc.).
    * Clasificación de `risk_category` (Alto, Moderado, Bajo) basada en umbrales de estrés y sueño.
* **Manejo de Errores:** Implementación de bloques `try/except` y logging para monitorear la ejecución.

### 3. Load (Carga)
* **Almacenamiento:** Los datos procesados se guardan en formato **Parquet** (`mental_health_final.parquet`).
* **Escalabilidad:** Se eligió Parquet por ser un formato columnar comprimido, ideal para analítica de datos a gran escala y mucho más eficiente que CSV.

---

## 📊 Fase 3: Dashboard y Visualización de Insights

El dashboard final (`dashboard_final_v18_funnel_mix.html`) utiliza un diseño oscuro de alto contraste y presenta los siguientes análisis estratégicos:

| Visualización | Tipo de Gráfico | Propósito e Insight |
|---|---|---|
| **KPIs Globales** | Indicadores Numéricos | Lectura inmediata del nivel promedio de estrés y conteo de empleados en riesgo crítico. |
| **Perfil por Sector** | Gráfico de Radar | Comparación multidimensional para detectar si el estrés es sistémico o específico de una industria. |
| **Tendencia por Edad** | Gráfico de Área | Visualización de cómo el estrés impacta de forma diferente a las generaciones (Gen Z vs Boomers). |
| **Efectividad de Soluciones** | **Gráfico de Embudo (Funnel)** | **Insight de Acción:** Clasifica qué actividades (ej. Deporte, Naturaleza) son más efectivas para reducir el estrés. |
| **Desglose de Riesgo** | **Barras Apiladas 100%** | **Insight de Riesgo:** Muestra el porcentaje exacto de empleados en "Alto Riesgo" dentro de cada sector (ej. Salud vs Tecnología). |

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
* Docker y Docker Compose instalados.
* Python 3.x instalado localmente (para correr el script del dashboard).

### Paso 1: Levantar la Infraestructura
En la terminal, dentro de la carpeta del proyecto:
```bash
docker-compose up --build -d
````

### Paso 2: Ejecutar el ETL en Airflow

1.  Accede a `http://localhost:8080` (Usuario/Pass: `airflow`).
2.  Busca el DAG **`mental_health_etl_matrix`**.
3.  Activa el DAG (Toggle ON) y haz clic en el botón **Play (Trigger DAG)**.
4.  Espera a que las tareas (`extract`, `transform`, `load`) se pongan en verde oscuro.

### Paso 3: Generar el Dashboard

Una vez que el ETL haya generado el archivo `mental_health_final.parquet` en la carpeta `output_data/`:

1.  Instala las librerías necesarias:
    ```bash
    pip install pandas plotly pyarrow
    ```
2.  Ejecuta el script generador:
    ```bash
    python dashboard_final_v18_funnel_mix.py
    ```
3.  Abre el archivo HTML generado (`dashboard_final_v18_funnel_mix.html`) en tu navegador web.

-----

## 🛠️ Tecnologías Utilizadas

  * **Orquestación:** Apache Airflow 2.9
  * **Contenerización:** Docker
  * **Procesamiento:** Python (Pandas, NumPy)
  * **Visualización:** Plotly Graph Objects
  * **Almacenamiento:** Apache Parquet



