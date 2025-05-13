# utils/rabbitmq_utils.py
import pika
import json

def publicar_evento(model, data, action):
    try:
        mensaje = {
            "model": model,
            "action": action,
            "data": data
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'sebas123')
        ))
        channel = connection.channel()
        # Declarar el exchange tipo fanout
        channel.exchange_declare(exchange='replicacion_fanout', exchange_type='fanout', durable=True)
        # Publicar al exchange, no a una cola específica
        channel.basic_publish(
            exchange='replicacion_fanout',
            routing_key='',
            body=json.dumps(mensaje),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        print(f"[✔] {model.upper()} publicado a RabbitMQ (fanout): {mensaje}")
    except Exception as e:
        print(f"[✖] Error publicando {model} en RabbitMQ: {e}")
