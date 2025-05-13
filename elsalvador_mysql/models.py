from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Text, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from config.config import Base, engine

# Tabla intermedia: muchos a muchos entre Asunto y Procurador
asunto_procurador = Table(
    'asunto_procurador',
    Base.metadata,
    Column('expediente_id', Integer, ForeignKey('asunto.expediente_id'), primary_key=True),
    Column('id_procurador', Integer, ForeignKey('procurador.id_procurador'), primary_key=True)
)

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    asuntos = relationship("Asunto", back_populates="cliente")

class Asunto(Base):
    __tablename__ = "asunto"

    expediente_id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String(50), nullable=False)

    cliente = relationship("Cliente", back_populates="asuntos")
    procuradores = relationship("Procurador", secondary=asunto_procurador, back_populates="asuntos")
    audiencias = relationship("Audiencia", back_populates="asunto")

class Procurador(Base):
    __tablename__ = "procurador"

    id_procurador = Column(Integer, primary_key=True, autoincrement=True)
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
    pais = Column(Enum('Guatemala', 'México', 'El Salvador'), nullable=False)

    audiencias = relationship("Audiencia", back_populates="abogado")

class Audiencia(Base):
    __tablename__ = "audiencia"

    id_audiencia = Column(Integer, primary_key=True, autoincrement=True)
    expediente_id = Column(Integer, ForeignKey("asunto.expediente_id"), nullable=False)
    fecha = Column(Date, nullable=False)
    lugar = Column(String(100), nullable=False)
    abogado_dni = Column(String(20), ForeignKey("abogado.dni"), nullable=False)

    asunto = relationship("Asunto", back_populates="audiencias")
    abogado = relationship("Abogado", back_populates="audiencias")
    incidencias = relationship("Incidencia", back_populates="audiencia")

class Incidencia(Base):
    __tablename__ = "incidencia"

    id_incidencia = Column(Integer, primary_key=True, autoincrement=True)
    id_audiencia = Column(Integer, ForeignKey("audiencia.id_audiencia"), nullable=False)
    descripcion = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

    audiencia = relationship("Audiencia", back_populates="incidencias")
