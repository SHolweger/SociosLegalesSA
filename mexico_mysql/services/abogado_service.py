from flask import jsonify
from models import Abogado

def get_abogados(SessionLocal):
    try:
        session = SessionLocal()
        abogados = session.query(Abogado).all()
        return jsonify([
            {
                "dni": a.dni,
                "nombre": a.nombre,
                "apellido": a.apellido,
                "pais": a.pais
            }
            for a in abogados
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500

def create_abogado(data, SessionLocal):
    session = SessionLocal()
    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    pais = data.get("pais")

    if not all([dni, nombre, apellido, pais]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        abogado = Abogado(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            pais=pais
        )
        session.add(abogado)
        session.commit()
        return jsonify({"message": "Abogado creado correctamente", "status": 201})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_abogado(dni, data, SessionLocal):
    session = SessionLocal()
    abogado = session.query(Abogado).filter_by(dni=dni).first()
    if not abogado:
        return jsonify({"error": "Abogado no encontrado", "status": 404})

    try:
        if data.get("pais"):
            abogado.pais = data.get("pais")

        session.commit()
        return jsonify({"message": "Abogado actualizado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def delete_abogado(dni, SessionLocal):
    session = SessionLocal()
    abogado = session.query(Abogado).filter_by(dni=dni).first()
    if not abogado:
        return jsonify({"error": "Abogado no encontrado", "status": 404})

    try:
        session.delete(abogado)
        session.commit()
        return jsonify({"message": "Abogado eliminado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()
def get_abogado_by_dni(dni, SessionLocal):
    session = SessionLocal()
    abogado = session.query(Abogado).filter_by(dni=dni).first()
    if not abogado:
        return jsonify({"error": "Abogado no encontrado", "status": 404})

    try:
        return jsonify({
            "dni": abogado.dni,
            "nombre": abogado.nombre,
            "apellido": abogado.apellido,
            "pais": abogado.pais
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()