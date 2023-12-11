from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .conexion import engine

# Crear una clase base para tus modelos
Base = declarative_base()

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
