import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# 1. Configuración de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://usuario_portfolio:password_secreto@db:5432/base_datos_opiniones"
)

# 2. Creación del motor (Engine) con REINTENTOS AUTOMÁTICOS


def get_engine_with_retry():
    max_retries = 10
    counter = 0
    while counter < max_retries:
        try:
            # Intentamos conectar
            engine = create_engine(DATABASE_URL)
            connection = engine.connect()
            connection.close()
            print("✅ ¡Conexión a Base de Datos exitosa!")
            return engine
        except OperationalError:
            counter += 1
            print(
                f"⏳ Base de datos no lista. Reintentando ({counter}/{max_retries})...")
            time.sleep(5)  # Espera 5 segundos antes de volver a intentar

    raise Exception(
        "❌ No se pudo conectar a la DB después de varios intentos.")


engine = get_engine_with_retry()

# 3. Sesión y Base para modelos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
