from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from config import Base


class Opinion(Base):
    # Nombre de la tabla en Postgres
    __tablename__ = "opiniones"

    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    texto_original = Column(String)      # El tweet o noticia cruda
    sentimiento = Column(Float)          # Puntuación (-1 a 1)
    fuente = Column(String)              # De dónde vino (ej: "Fake Twitter")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # El equivalente al toString() de Java
    def __repr__(self):
        return f"<Opinion(id={self.id}, sentimiento={self.sentimiento})>"
