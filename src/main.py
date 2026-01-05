import time
import requests
import random
from textblob import TextBlob
from config import engine, SessionLocal, Base
from models import Opinion

# --- 1. PREPARACIÓN DB ---
print("Creando tablas...")
Base.metadata.create_all(bind=engine)

# --- LISTAS DE ORACIONES SIMULADAS (DATASET) ---
TWEETS_POSITIVOS = [
    "Bitcoin is going to the moon! 🚀",
    "Just bought more BTC, this technology is amazing.",
    "Best investment of my life, so happy! 😊",
    "Crypto is the future of money, banks are dead.",
    "Bull run is here! Green candles everywhere."
]

TWEETS_NEGATIVOS = [
    "This is a scam, I lost all my money! 😡",
    "Bitcoin is crashing, panic sell now!",
    "Crypto is dead, worst investment ever.",
    "I hate this volatility, too risky.",
    "Government will ban crypto soon, be careful."
]

TWEETS_NEUTRALES = [
    "Bitcoin price is holding steady today.",
    "Watching the charts, waiting for a move.",
    "Crypto market analysis for the week.",
    "Just read a news article about blockchain.",
    "What do you guys think about the current price?"
]

# --- 2. FUNCIONES ETL ---


def extract_data():
    """
    FASE E (Extract):
    1. Obtiene el precio Y el cambio en 24h de CoinGecko.
    2. Genera una opinión basada en si el mercado sube o baja.
    """
    print("--- [E] Extrayendo datos... ---")

    precio_msg = "BTC Price: Unavailable"
    cambio_24h = None  # Variable para guardar el porcentaje

    # 1. Intentamos obtener datos reales
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            precio = data['bitcoin']['usd']
            # Capturamos el cambio
            cambio_24h = data['bitcoin']['usd_24h_change']
            precio_msg = f"BTC Price: ${precio}"
    except Exception as e:
        print(f"Error conectando a API: {e}")

    # 2. Generación de Opinión (Lógica basada en precio)

    if cambio_24h is not None:
        # --- LÓGICA INTELIGENTE ---
        print(f"   > El mercado ha variado un: {cambio_24h}%")

        if cambio_24h > 0.1:  # Si ha subido más de un 0.1%
            opinion_elegida = random.choice(TWEETS_POSITIVOS)
            tipo = "Bullish (Mercado Subiendo)"
        elif cambio_24h < -0.1:  # Si ha bajado más de un 0.1%
            opinion_elegida = random.choice(TWEETS_NEGATIVOS)
            tipo = "Bearish (Mercado Bajando)"
        else:  # Si está casi igual (-0.1 a 0.1)
            opinion_elegida = random.choice(TWEETS_NEUTRALES)
            tipo = "Neutral (Mercado Lateral)"

    else:
        # --- LÓGICA DE RESPALDO (Si falla la API, usamos azar) ---
        print("   > API falló, usando modo aleatorio...")
        dado = random.random()
        if dado < 0.4:
            opinion_elegida = random.choice(TWEETS_POSITIVOS)
            tipo = "Random Bullish"
        elif dado < 0.8:
            opinion_elegida = random.choice(TWEETS_NEGATIVOS)
            tipo = "Random Bearish"
        else:
            opinion_elegida = random.choice(TWEETS_NEUTRALES)
            tipo = "Random Neutral"

    mensaje_final = f"{precio_msg} | {opinion_elegida}"

    print(f"   > Simulación: {tipo}")
    return [mensaje_final]


def transform_data(texto):
    """
    FASE T (Transform):
    Analiza el sentimiento del texto completo.
    """
    blob = TextBlob(texto)
    score = blob.sentiment.polarity
    print(f"   > [T] Score calculado: {score}")
    return score


def load_data(texto, score):
    """
    FASE L (Load):
    Guarda en DB.
    """
    session = SessionLocal()
    try:
        nueva_opinion = Opinion(
            texto_original=texto,
            sentimiento=score,
            fuente="Smart Simulator"  # Indicamos que ahora es 'Smart'
        )
        session.add(nueva_opinion)
        session.commit()
        print(f"   > [L] Guardado ID: {nueva_opinion.id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

# --- 3. MAIN LOOP ---


def main():
    print("Iniciando Simulador Inteligente (Basado en Precio)...")
    while True:
        datos = extract_data()
        for dato in datos:
            score = transform_data(dato)
            load_data(dato, score)

        print("--- Esperando 15 segundos... ---")
        time.sleep(15)


if __name__ == "__main__":
    main()
