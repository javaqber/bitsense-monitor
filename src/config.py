import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Obtenemos la URL de la base de datos de las variables de entorno
# (Si no la encuentra, usa la de por defecto)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://usuario_portfolio:password_secreto@db:5432/base_datos_opiniones"
)

# 2. Creamos el "Motor" (Engine). Es el gestor de conexiones.
engine = create_engine(DATABASE_URL)

# 3. Creamos la "Fábrica de Sesiones".
# Cada vez que queramos hablar con la DB, pediremos una sesión a esta fábrica.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Esta es la clase base para tus modelos (Entidades)
Base = declarative_base()
