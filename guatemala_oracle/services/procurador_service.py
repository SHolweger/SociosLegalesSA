from flask import jsonify
from models import Procurador
from utils.rabbitmq_utils import publicar_evento

def get_procuradores(SessionLocal):
    try:
        session = SessionLocal()
        procuradores = session.query(Procurador).all()
        return jsonify([
            {
                "id": p.id_procurador,
                "nombre": p.nombre,
                "apellido": p.apellido,
                "telefono": p.telefono,
                "email": p.email
            }
            for p in procuradores
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500

def create_procurador(data, SessionLocal):
    session = SessionLocal()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    telefono = data.get("telefono")
    email = data.get("email")

    if not all([nombre, apellido, telefono, email]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        procurador = Procurador(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email
        )
        session.add(procurador)
        session.commit()
        #Publicar en RabbitMQ
        procurador_data = {
            "nombre":procurador.nombre,
            "apellido":procurador.apellido,
            "telefono":procurador.telefono,
            "email":procurador.email
        }
        publicar_evento("procurador",procurador_data,action="create")
        return jsonify({"message": "Procurador creado correctamente", "status": 201})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_procurador(id, data, SessionLocal):
    session = SessionLocal()
    procurador = session.query(Procurador).filter_by(id_procurador=id).first()
    if not procurador:
        return jsonify({"error": "Procurador no encontrado", "status": 404})

    try:
        if data.get("telefono"):
            procurador.telefono = data.get("telefono")
        if data.get("email"):
            procurador.email = data.get("email")

        session.commit()
        
        #Publicar en RabbitMQ
        procurador_data = {
            "nombre":procurador.nombre,
            "apellido":procurador.apellido,
            "telefono":procurador.telefono,
            "email":procurador.email
        }
        publicar_evento("procurador",procurador_data,action="update")
        
        return jsonify({"message": "Procurador actualizado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()
        
def delete_procurador(id, SessionLocal):
    session = SessionLocal()
    procurador = session.query(Procurador).filter_by(id_procurador=id).first()
    if not procurador:
        return jsonify({"error": "Procurador no encontrado", "status": 404})

    try:
        session.delete(procurador)
        session.commit()
        #Publicar eliminacion en RabbitMQ
        publicar_evento("procurador",{"id_procurador":id}, action="delete")
        return jsonify({"message": "Procurador eliminado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def get_procurador_by_id(id, SessionLocal):
    session = SessionLocal()
    procurador = session.query(Procurador).filter_by(id_procurador=id).first()
    if not procurador:
        return jsonify({"error": "Procurador no encontrado", "status": 404})

    try:
        return jsonify({
            "id": procurador.id_procurador,
            "nombre": procurador.nombre,
            "apellido": procurador.apellido,
            "telefono": procurador.telefono,
            "email": procurador.email
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()