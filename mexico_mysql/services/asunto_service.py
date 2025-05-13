from flask import jsonify
from models import Asunto
from datetime import datetime

def get_asuntos(SessionLocal):
    try:
        session = SessionLocal()
        asuntos = session.query(Asunto).all()
        return jsonify([
            {
                "expediente_id": a.expediente_id,
                "id_cliente": a.id_cliente,
                "fecha_inicio": a.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": a.fecha_fin.strftime("%Y-%m-%d") if a.fecha_fin else None,
                "estado": a.estado
            }
            for a in asuntos
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def create_asunto(data, SessionLocal):
    session = SessionLocal()
    id_cliente = data.get("id_cliente")
    fecha_inicio_str = data.get("fecha_inicio")
    fecha_fin_str = data.get("fecha_fin")
    estado = data.get("estado")

    if not all([id_cliente, fecha_inicio_str, estado]):
        return jsonify({"error": "id_cliente, fecha_inicio y estado son obligatorios"}), 400

    try:
        # Validación de fechas
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d") if fecha_fin_str else None
        except ValueError:
            return jsonify({"error": "Formato de fecha no válido. Use el formato YYYY-MM-DD"}), 400

        # Verificación de que fecha_fin no sea anterior a fecha_inicio
        if fecha_fin and fecha_fin < fecha_inicio:
            return jsonify({"error": "La fecha de fin no puede ser anterior a la fecha de inicio"}), 400
        
        # Creación del asunto
        asunto = Asunto(
            id_cliente=id_cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado
        )
        session.add(asunto)
        session.commit()

        return jsonify({"message": "Asunto creado correctamente", "status": 201})

    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_asunto(id, data, SessionLocal):
    session = SessionLocal()
    asunto = session.query(Asunto).filter_by(expediente_id=id).first()
    if not asunto:
        return jsonify({"error": "Asunto no encontrado", "status": 404})

    try:
        if data.get("estado"):
            asunto.estado = data.get("estado")
        if data.get("fecha_fin"):
            try:
                asunto.fecha_fin = datetime.strptime(data.get("fecha_fin"), "%Y-%m-%d")
            except ValueError:
                return jsonify({"error": "Formato de fecha no válido. Use el formato YYYY-MM-DD"}), 400

        session.commit()
        return jsonify({"message": "Asunto actualizado correctamente", "status": 200})

    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def delete_asunto(id, SessionLocal):
    session = SessionLocal()
    asunto = session.query(Asunto).filter_by(expediente_id=id).first()
    if not asunto:
        return jsonify({"error": "Asunto no encontrado", "status": 404})

    try:
        session.delete(asunto)
        session.commit()
        return jsonify({"message": "Asunto eliminado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def get_asunto_by_id(id, SessionLocal):
    session = SessionLocal()
    asunto = session.query(Asunto).filter_by(expediente_id=id).first()
    if not asunto:
        return jsonify({"error": "Asunto no encontrado", "status": 404})
    
    try:
        return jsonify({
            "expediente_id": asunto.expediente_id,
            "id_cliente": asunto.id_cliente,
            "fecha_inicio": asunto.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": asunto.fecha_fin.strftime("%Y-%m-%d") if asunto.fecha_fin else None,
            "estado": asunto.estado
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()