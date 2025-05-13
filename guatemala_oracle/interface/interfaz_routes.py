from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Cliente, Abogado, Asunto, Audiencia, Procurador, Incidencia
from config.config import engine
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)
interfaz_bp = Blueprint('interfaz', __name__)

@interfaz_bp.route('/')
def index():
    return render_template('index.html')

@interfaz_bp.route('/clientes')
def clientes():
    session = SessionLocal()
    clientes = session.query(Cliente).all()
    session.close()
    return render_template('clientes.html', clientes=clientes)