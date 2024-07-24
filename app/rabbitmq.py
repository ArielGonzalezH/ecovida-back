import pika
import logging

# Configuración básica del logging para imprimir en la consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def enviar_mensaje_a_rabbitmq(queue_name, mensaje):
    connection = None
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                'rabbitmq',  # Nombre del contenedor de RabbitMQ
                5672,        # Puerto por defecto de RabbitMQ
                '/',          # Virtual host por defecto
                pika.PlainCredentials('user', 'password')  # Credenciales
            )
        )
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=mensaje,
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
        
        logging.info(f" [x] Mensaje enviado a la cola '{queue_name}': {mensaje}")
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error de conexión a RabbitMQ: {e}")
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()
