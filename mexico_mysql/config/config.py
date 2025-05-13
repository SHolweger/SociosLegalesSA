import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv

dotenv.load_dotenv()

# Declaración de la base para los modelos
Base = declarative_base()

# Carga de variables de entorno (asegúrate de tener un .env)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")  # nombre del contenedor MySQL
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

try:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    print("Conexión Sucursal MySQL México exitosa")
except Exception as e:
    print(f"Error al conectar con Sucursal MySQL México: {e}")
    engine = None
    SessionLocal = None

# Función para obtener una sesión de base de datos
def get_db_connection():
    try:
        return engine, SessionLocal, Base
    except Exception as e:
        print(f"Error creando la sesion de base de datos: {e}")
        return None, None, None
