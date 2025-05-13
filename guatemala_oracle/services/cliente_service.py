from flask import jsonify
from models import Cliente
from utils.rabbitmq_utils import publicar_evento

def get_clientes(SessionLocal):
    try:
        session = SessionLocal()
        clientes = session.query(Cliente).all()
        return jsonify([
            {
                "id": c.id_cliente,
                "nombre": c.nombre,
                "apellido": c.apellido,
                "telefono": c.telefono,
                "direccion": c.direccion,
                "email": c.email
            } 
            for c in clientes
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500

def create_cliente(data, SessionLocal):
    session = SessionLocal()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    telefono = data.get("telefono")
    direccion = data.get("direccion")
    email = data.get("email")

    # Validación
    if not all([nombre, apellido, telefono, direccion, email]):
        return jsonify({"error": "Todos los campos son obligatorios: nombre, apellido, telefono, direccion, email"}), 400

    try:
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            email=email
        )
        session.add(cliente)
        session.commit()

        # Publicamos en RabbitMQ
        cliente_data = {
                "id_cliente": cliente.id_cliente,  # Incluimos el id_cliente generado
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "telefono": cliente.telefono,
                "direccion": cliente.direccion,
                "email": cliente.email
        }
        publicar_evento("clientes",cliente_data,action="create")  # Llamamos a la función que publica el mensaje
        return jsonify({"message": "Cliente creado correctamente", "status": 201})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_cliente(id, data, SessionLocal):
    session = SessionLocal()
    cliente = session.query(Cliente).filter_by(id_cliente=id).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    telefono = data.get("telefono")
    direccion = data.get("direccion")
    email = data.get("email")

    try:
        if telefono: cliente.telefono = telefono
        if direccion: cliente.direccion = direccion
        if email: cliente.email = email

        session.commit()

        # Publicar evento en RabbitMQ
        event_data = {
            #"id_cliente": cliente.id_cliente,
            #"nombre": cliente.nombre,
            #"apellido": cliente.apellido,
            "telefono": cliente.telefono,
            "direccion": cliente.direccion,
            "email": cliente.email
        }
        publicar_evento("clientes",event_data, action="update")

        return jsonify({"message": "Cliente actualizado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def delete_cliente(id, SessionLocal):
    session = SessionLocal()
    cliente = session.query(Cliente).filter_by(id_cliente=id).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado", "status": 404})

    try:
        session.delete(cliente)
        session.commit()
        # Publicar evento de eliminación
        publicar_evento("clientes",{"id_cliente": id}, action="delete")
        return jsonify({"message": "Cliente eliminado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def get_cliente_by_id(id, SessionLocal):
    session = SessionLocal()
    cliente = session.query(Cliente).filter_by(id_cliente=id).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado", "status": 404})

    return jsonify({
        "id": cliente.id_cliente,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido,
        "telefono": cliente.telefono,
        "direccion": cliente.direccion,
        "email": cliente.email
    })
