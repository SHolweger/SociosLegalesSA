from flask import jsonify
from models import Audiencia
from datetime import datetime

def get_audiencias(SessionLocal):
    try:
        session = SessionLocal()
        audiencias = session.query(Audiencia).all()
        return jsonify([
            {
                "id_audiencia": a.id_audiencia,
                "expediente_id": a.expediente_id,
                "fecha": a.fecha.strftime("%Y-%m-%d") if a.fecha else None,
                "lugar": a.lugar,
                "abogado_dni": a.abogado_dni
            }
            for a in audiencias
        ])
    except Exception as e:
        print(f"[ERROR] get_audiencias: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def create_audiencia(data, SessionLocal):
    session = SessionLocal()
    expediente_id = data.get("expediente_id")
    fecha_str = data.get("fecha")
    lugar = data.get("lugar")
    abogado_dni = data.get("abogado_dni")

    if not all([expediente_id, fecha_str, lugar, abogado_dni]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        # 🔐 Validación segura de fecha
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido, debe ser YYYY-MM-DD"}), 400

        audiencia = Audiencia(
            expediente_id=expediente_id,
            fecha=fecha,
            lugar=lugar,
            abogado_dni=abogado_dni
        )
        session.add(audiencia)
        session.commit()
        return jsonify({
            "message": "Audiencia creada correctamente",
            "audiencia_id": audiencia.id_audiencia
        }), 201
    except Exception as e:
        session.rollback()
        print(f"[ERROR] create_audiencia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_audiencia(id, data, SessionLocal):
    session = SessionLocal()
    try:
        audiencia = session.query(Audiencia).filter_by(id_audiencia=id).first()
        if not audiencia:
            return jsonify({"error": "Audiencia no encontrada"}), 404

        fecha_str = data.get("fecha")
        if fecha_str:
            try:
                audiencia.fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido, debe ser YYYY-MM-DD"}), 400

        if "expediente_id" in data:
            audiencia.expediente_id = data["expediente_id"]

        if "lugar" in data:
            audiencia.lugar = data["lugar"]

        if "abogado_dni" in data:
            audiencia.abogado_dni = data["abogado_dni"]

        session.commit()
        return jsonify({"message": "Audiencia actualizada correctamente"}), 200
    except Exception as e:
        session.rollback()
        print(f"[ERROR] update_audiencia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def delete_audiencia(id, SessionLocal):
    session = SessionLocal()
    try:
        audiencia = session.query(Audiencia).filter_by(id_audiencia=id).first()
        if not audiencia:
            return jsonify({"error": "Audiencia no encontrada"}), 404

        session.delete(audiencia)
        session.commit()
        return jsonify({"message": "Audiencia eliminada correctamente"}), 200
    except Exception as e:
        session.rollback()
        print(f"[ERROR] delete_audiencia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def get_audiencia_by_id(id, SessionLocal):
    session = SessionLocal()
    try:
        audiencia = session.query(Audiencia).filter_by(id_audiencia=id).first()
        if not audiencia:
            return jsonify({"error": "Audiencia no encontrada"}), 404

        return jsonify({
            "id_audiencia": audiencia.id_audiencia,
            "expediente_id": audiencia.expediente_id,
            "fecha": audiencia.fecha.strftime("%Y-%m-%d") if audiencia.fecha else None,
            "lugar": audiencia.lugar,
            "abogado_dni": audiencia.abogado_dni
        })
    except Exception as e:
        print(f"[ERROR] get_audiencia_by_id: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()