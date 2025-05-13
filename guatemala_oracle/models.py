from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, CheckConstraint, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from config.config import Base, engine
from oracle_helper import OracleHelper

# Tabla intermedia para la relación muchos a muchos entre Asunto y Procurador
asunto_procurador = Table(
    'asunto_procurador',
    Base.metadata,
    Column('expediente_id', Integer, ForeignKey('asunto.expediente_id'), primary_key=True),
    Column('id_procurador', Integer, ForeignKey('procurador.id_procurador'), primary_key=True)
)

class Cliente(Base):
    __tablename__ = "clientes"  # Nombre de la tabla en Oracle

    id_cliente = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    asuntos = relationship("Asunto", back_populates="cliente")

class Asunto(Base):
    __tablename__ = "asunto"

    expediente_id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)  # Puede estar null si no ha finalizado
    estado = Column(String(50), nullable=False)

    cliente = relationship("Cliente", back_populates="asuntos")
    procuradores = relationship("Procurador", secondary=asunto_procurador, back_populates="asuntos")
    audiencias = relationship("Audiencia", back_populates="asunto")

class Procurador(Base):
    __tablename__ = "procurador"

    id_procurador = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)

    asuntos = relationship("Asunto", secondary=asunto_procurador, back_populates="procuradores")

class Abogado(Base):
    __tablename__ = "abogado"

    dni = Column(String(20), primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    pais = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint("pais IN ('Guatemala', 'México', 'El Salvador')", name="check_pais"),
    )

    audiencias = relationship("Audiencia", back_populates="abogado")

class Audiencia(Base):
    __tablename__ = "audiencia"

    id_audiencia = Column(Integer, primary_key=True)
    expediente_id = Column(Integer, ForeignKey("asunto.expediente_id"), nullable=False)
    fecha = Column(Date, nullable=False)
    lugar = Column(String(100), nullable=False)
    abogado_dni = Column(String(20), ForeignKey("abogado.dni"), nullable=False)

    asunto = relationship("Asunto", back_populates="audiencias")
    abogado = relationship("Abogado", back_populates="audiencias")
    incidencias = relationship("Incidencia", back_populates="audiencia")

class Incidencia(Base):
    __tablename__ = "incidencia"

    id_incidencia = Column(Integer, primary_key=True)
    id_audiencia = Column(Integer, ForeignKey("audiencia.id_audiencia"), nullable=False)
    descripcion = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

    audiencia = relationship("Audiencia", back_populates="incidencias")


# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Crear secuencias y triggers con OracleHelper
helper = OracleHelper(engine)
helper.create_auto_increment("clientes", "id_cliente")
helper.create_auto_increment("asunto", "expediente_id")
helper.create_auto_increment("procurador", "id_procurador")
helper.create_auto_increment("audiencia", "id_audiencia")
helper.create_auto_increment("incidencia", "id_incidencia")