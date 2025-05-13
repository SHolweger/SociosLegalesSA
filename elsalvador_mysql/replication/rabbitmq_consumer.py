import pika
import json
from sqlalchemy.orm import sessionmaker
from models import Cliente, Abogado, Asunto, Audiencia, Procurador, Incidencia
from config.config import engine

# Crea la sesión de base de datos
SessionLocal = sessionmaker(bind=engine)

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        model = data.get("model")
        action = data.get("action", "create")
        model_data = data.get("data")
        session = SessionLocal()
        try:
            if model == "clientes":
                existente = session.query(Cliente).filter_by(id_cliente=model_data["id_cliente"]).first()
                pk = model_data["id_cliente"]
            elif model == "abogado":
                existente = session.query(Abogado).filter_by(dni=model_data["dni"]).first()
                pk = model_data["dni"]
            elif model == "asunto":
                existente = session.query(Asunto).filter_by(id_asunto=model_data["id_asunto"]).first()
                pk = model_data["id_asunto"]
            elif model == "audiencia":
                existente = session.query(Audiencia).filter_by(id_audiencia=model_data["id_audiencia"]).first()
                pk = model_data["id_audiencia"]
            elif model == "procurador":
                existente = session.query(Procurador).filter_by(id_procurador=model_data["id_procurador"]).first()
                pk = model_data["id_procurador"]
            elif model == "incidencia":
                existente = session.query(Incidencia).filter_by(id_incidencia=model_data["id_incidencia"]).first()
                pk = model_data["id_incidencia"]
            else:
                print(f"[WARN] Modelo no soportado: {model}")
                session.close()
                return

            if action == "delete":
                if existente:
                    session.delete(existente)
                    session.commit()
                    print(f"{model.capitalize()} eliminado: {pk}")
                else:
                    print(f"{model.capitalize()} a eliminar no existe: {pk}")
            elif action == "update":
                if existente:
                    for campo, valor in model_data.items():
                        setattr(existente, campo, valor)
                    session.commit()
                    print(f"{model.capitalize()} actualizado: {pk}")
                else:
                    print(f"{model.capitalize()} a actualizar no existe: {pk}")
            else:  # create
                if not existente:
                    # Instancia dinámica según el modelo
                    modelo_clase = {
                        "clientes": Cliente,
                        "abogado": Abogado,
                        "asunto": Asunto,
                        "audiencia": Audiencia,
                        "procurador": Procurador,
                        "incidencia": Incidencia
                    }[model]
                    nuevo = modelo_clase(**model_data)
                    session.add(nuevo)
                    session.commit()
                    print(f"{model.capitalize()} replicado en base de datos local: {pk}")
                else:
                    print(f"{model.capitalize()} ya existe: {pk}")
        except Exception as e:
            session.rollback()
            print(f"Error al replicar {model}: {e}")
        finally:
            session.close()
    except Exception as e:
        print(f"[ERROR] Fallo en el callback: {e}")

def iniciar_consumidor():
    try:
        print("[DEBUG] Intentando conectar a RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'sebas123'),
            heartbeat=600,
            blocked_connection_timeout=300
        ))
        print("[DEBUG] Conexión a RabbitMQ exitosa.")
        channel = connection.channel()
        print("[DEBUG] Canal creado.")

        # Declarar el exchange tipo fanout
        channel.exchange_declare(exchange='replicacion_fanout', exchange_type='fanout', durable=True)
        # Declarar una cola única para esta sucursal (puedes personalizar el nombre)
        queue_name = 'replicacion_elsalvador'
        channel.queue_declare(queue=queue_name, durable=True)
        # Enlazar la cola al exchange fanout
        channel.queue_bind(exchange='replicacion_fanout', queue=queue_name)

        print("[DEBUG] Cola y binding declarados.")
        print("[*] Esperando mensajes. Para salir presiona CTRL+C")
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("[DEBUG] Consumidor registrado.")
        channel.start_consuming()
        print("[!] El consumidor dejó de consumir (start_consuming terminó)")
    except Exception as e:
        print(f"[ERROR] Fallo en iniciar_consumidor: {e}")


if __name__ == "__main__":
    iniciar_consumidor()
