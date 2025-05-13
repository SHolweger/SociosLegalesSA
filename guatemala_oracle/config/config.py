from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import dotenv

dotenv.load_dotenv()

# Declaración de la base para los modelos
Base = declarative_base()

# Crear el engine y la sesión globalmente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SERVICE = os.getenv("DB_SERVICE")

try:
    DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    print("Conexion a la base de datos CENTRAL establecida correctamente.")
except Exception as e:
    print(f"Error conectandose a la base de datos CENTRAL: {e}")
    engine = None
    SessionLocal = None

# Función para obtener una sesión de base de datos
def get_db_connection():
    try:
        return engine, SessionLocal, Base
    except Exception as e:
        print(f"Error creando la sesión de base de datos: {e}")
        return None, None, None
