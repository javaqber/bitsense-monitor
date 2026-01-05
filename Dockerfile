# 1. Usamos una imagen base de Python ligera
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de requisitos primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# 4. Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 5. Descargamos los datos necesarios para TextBlob (la librería de IA)
# (Esto es específico de esta librería, necesita descargar un pequeño corpus de palabras)
RUN python -m textblob.download_corpora

# 6. Copiamos el resto de tu código (la carpeta src)
COPY src/ ./src/

# 7. Comando para ejecutar tu app cuando arranque el contenedor
# Le decimos que ejecute el archivo dentro de la carpeta src
CMD ["python", "src/main.py"]