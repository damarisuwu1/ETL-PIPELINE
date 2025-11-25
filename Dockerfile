# Usamos la imagen oficial de Airflow como base
FROM apache/airflow:2.9.1

# Copiamos el archivo de requisitos al contenedor
COPY requirements.txt /requirements.txt

# Instalamos las librerías extra (Pandas, Numpy, etc.)
RUN pip install --no-cache-dir -r /requirements.txt