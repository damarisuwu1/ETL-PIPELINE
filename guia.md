# 🚀 Guía de Ejecución: Pipeline ETL de Salud Mental y Dashboard

Este documento detalla los pasos técnicos exactos para levantar la infraestructura, ejecutar la tubería de datos y generar el dashboard de visualización.

---

## 🛠️ 1. Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Docker Desktop** (Debe estar abierto y corriendo "Engine running").
2. **Python 3.x** instalado en tu sistema local.
3. **Visual Studio Code** (o tu terminal de preferencia).

---

## 📂 2. Estructura de Archivos

Asegúrate de que tu carpeta de proyecto tenga esta organización para que los volúmenes de Docker funcionen correctamente:

```text
mi_proyecto_airflow/
├── dags/
│   └── mental_health_etl_matrix.py       <-- El código del DAG (ETL)
├── output_data/                          <-- Carpeta vacía (Docker guardará datos aquí)
├── dashboard_final_v18_funnel_mix.py     <-- El script del Dashboard
├── docker-compose.yaml                   <-- Configuración de infraestructura
├── Dockerfile                            <-- Configuración de imagen
└── requirements.txt                      <-- Dependencias (pandas, numpy, etc.)
```

---

## ⚡ 3. Paso a Paso: Cómo Levantar el Proyecto

### Paso 1: Iniciar la Infraestructura (Docker)

Abre tu terminal en la carpeta del proyecto y ejecuta el siguiente comando para descargar las imágenes e iniciar Airflow:

```bash
docker-compose up --build -d
```

> *Nota: La primera vez puede tardar unos minutos. Espera a que la terminal te devuelva el control.*

### Paso 2: Ejecutar el ETL (Airflow)

Una vez que Docker esté corriendo:

1. Abre tu navegador web e ingresa a: **http://localhost:8080**
2. Inicia sesión con las credenciales por defecto:
   - **Usuario:** `airflow`
   - **Contraseña:** `airflow`
3. En la lista de DAGs, busca: **`mental_health_etl_matrix`**.
4. **Actívalo:** Haz clic en el interruptor (Toggle) a la izquierda del nombre para que se ponga azul (ON).
5. **Ejecútalo:** Haz clic en el botón **Play (▷)** a la derecha y selecciona "Trigger DAG".
6. **Verificación:** Haz clic en el nombre del DAG y ve a la vista "Graph". Espera hasta que las cajas (`extract`, `transform`, `load`) tengan un borde **Verde Oscuro** (Success).

> *Resultado:* Un archivo llamado `mental_health_final.parquet` aparecerá automáticamente en tu carpeta local `output_data/`.

### Paso 3: Generar el Dashboard

Ahora que tenemos los datos, vamos a crear la visualización. En tu terminal local (fuera de Docker), ejecuta:

1. Instala las librerías necesarias (solo la primera vez):

   ```bash
   pip install pandas plotly pyarrow
   ```

2. Ejecuta el script generador:

   ```bash
   python dashboard_final_v18_funnel_mix.py
   ```

### Paso 4: Ver Resultados

Al finalizar el script, verás un mensaje de confirmación:
`🔥 DASHBOARD FINAL LISTO: dashboard_final_v18_funnel_mix.html`

1. Ve a tu carpeta del proyecto.
2. Haz doble clic en el archivo **`dashboard_final_v18_funnel_mix.html`**.
3. Se abrirá en tu navegador con todas las gráficas interactivas.

---

## 🛑 Cómo Detener el Proyecto

Cuando termines de trabajar y quieras liberar memoria de tu computadora, ejecuta en la terminal:

```bash
docker-compose down
```

---

## 🆘 Solución de Problemas Comunes

- **Error: "No se encuentra el archivo .parquet"**:
  - *Solución:* Asegúrate de haberle dado "Play" al DAG en Airflow y que todas las tareas estén en verde.
- **Airflow no carga en localhost:8080**:
  - *Solución:* Verifica que Docker Desktop esté corriendo. Si el puerto 8080 está ocupado por otra app, cambia el puerto en el archivo `docker-compose.yaml` (ej. a `8081:8080`).