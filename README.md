# 🪙 Monitor de Sentimiento y Precio de Bitcoin (ETL + Docker)

Este proyecto es un sistema de **Ingeniería de Datos end-to-end** que monitoriza el precio de Bitcoin en tiempo real, simula opiniones de mercado (sentimiento) y visualiza los datos en un Dashboard interactivo.

Todo el entorno está contenerizado con **Docker**, asegurando que funcione en cualquier máquina con un solo comando.

## 🏗️ Arquitectura

El sistema consta de 3 microservicios orquestados con Docker Compose:

1.  **Base de Datos (PostgreSQL):** Persistencia de datos transaccional.
2.  **ETL Service (Python):** \* Extrae el precio real y el cambio (24h) de la API pública de **CoinGecko**.
    - **Smart Simulation:** Genera opiniones sintéticas basadas en la tendencia del mercado:
      - 📈 Mercado Subiendo -> Genera comentarios de euforia ("Bullish").
      - 📉 Mercado Bajando -> Genera comentarios de pánico ("Bearish").
      - ➖ Mercado Lateral -> Genera comentarios neutrales.
    - Analiza el sentimiento del texto generado con **TextBlob** (IA).
    - Carga los datos enriquecidos en PostgreSQL.
3.  **Frontend (Streamlit):** \* Consulta la base de datos en tiempo real.
    - Muestra KPIs y gráficas de evolución de sentimiento y precio.

## 🚀 Tecnologías

- **Lenguaje:** Python 3.9
- **Contenedores:** Docker & Docker Compose
- **Base de Datos:** PostgreSQL 15
- **Librerías Clave:** Pandas, SQLAlchemy, Streamlit, Requests.

## 🛠️ Instalación y Uso

### Prerrequisitos

- Tener [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo.

### Pasos

1.  Clonar el repositorio:

    ```bash
    git clone https://github.com/javaqber/bitcoin-sentiment-etl-docker.git
    cd portfolio-etl-crypto
    ```

2.  Arrancar los servicios:

    ```bash
    docker compose up --build
    ```

3.  Acceder al Dashboard:

    - Abre tu navegador en: `http://localhost:8501`

4.  Detener el sistema:
    - Pulsa `Ctrl + C` en la terminal.

## 📊 Previsualización

El sistema procesa datos cada 5-15 segundos. La gráfica muestra la correlación entre las noticias simuladas (positivas/negativas) y el precio capturado en tiempo real.

---

_Proyecto realizado como práctica de Arquitectura de Datos y Docker._
