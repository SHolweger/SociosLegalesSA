from flask import jsonify
from models import asunto_procurador

def get_asunto_procuradores(SessionLocal):
    try:
        session = SessionLocal()
        relaciones = session.query(asunto_procurador).all()
        return jsonify([
            {
                "expediente_id": r.expediente_id,
                "id_procurador": r.id_procurador
            }
            for r in relaciones
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def assign_procurador_to_asunto(data, SessionLocal):
    session = SessionLocal()
    expediente_id = data.get("expediente_id")
    id_procurador = data.get("id_procurador")

    if not expediente_id or not id_procurador:
        return jsonify({"error": "expediente_id y id_procurador son obligatorios"}), 400

    try:
        relacion = asunto_procurador(
            expediente_id=expediente_id,
            id_procurador=id_procurador
        )
        session.add(relacion)
        session.commit()
        return jsonify({"message": "Procurador asignado al asunto correctamente", "status": 201})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()
