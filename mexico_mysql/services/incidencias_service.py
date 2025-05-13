from flask import jsonify
from models import Incidencia
from datetime import datetime

def get_incidencias(SessionLocal):
    try:
        session = SessionLocal()
        incidencias = session.query(Incidencia).all()
        return jsonify([
            {
                "id": i.id_incidencia,
                "id_audiencia": i.id_audiencia,
                "descripcion": i.descripcion,
                "tipo": i.tipo,
                "fecha": i.fecha.strftime("%Y-%m-%d")
            }
            for i in incidencias
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500

def create_incidencia(data, SessionLocal):
    session = SessionLocal()
    id_audiencia = data.get("id_audiencia")
    descripcion = data.get("descripcion")
    tipo = data.get("tipo")
    fecha_str = data.get("fecha")

    if not all([id_audiencia, descripcion, tipo, fecha_str]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        incidencia = Incidencia(
            id_audiencia=id_audiencia,
            descripcion=descripcion,
            tipo=tipo,
            fecha=fecha
        )
        session.add(incidencia)
        session.commit()
        return jsonify({"message": "Incidencia creada correctamente", "status": 201})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_incidencia(id, data, SessionLocal):
    session = SessionLocal()
    incidencia = session.query(Incidencia).filter_by(id_incidencia=id).first()
    if not incidencia:
        return jsonify({"error": "Incidencia no encontrada", "status": 404})

    try:
        if data.get("descripcion"):
            incidencia.descripcion = data.get("descripcion")
        if data.get("tipo"):
            incidencia.tipo = data.get("tipo")
        if data.get("fecha"):
            incidencia.fecha = datetime.strptime(data.get("fecha"), "%Y-%m-%d")

        session.commit()
        return jsonify({"message": "Incidencia actualizada correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def delete_incidencia(id, SessionLocal):
    session = SessionLocal()
    incidencia = session.query(Incidencia).filter_by(id_incidencia=id).first()
    if not incidencia:
        return jsonify({"error": "Incidencia no encontrada", "status": 404})

    try:
        session.delete(incidencia)
        session.commit()
        return jsonify({"message": "Incidencia eliminada correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def get_incidencia_by_id(id, SessionLocal): 
    session = SessionLocal()
    incidencia = session.query(Incidencia).filter_by(id_incidencia=id).first()
    if not incidencia:
        return jsonify({"error": "Incidencia no encontrada", "status": 404})

    try:
        return jsonify({
            "id": incidencia.id_incidencia,
            "id_audiencia": incidencia.id_audiencia,
            "descripcion": incidencia.descripcion,
            "tipo": incidencia.tipo,
            "fecha": incidencia.fecha.strftime("%Y-%m-%d")
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()