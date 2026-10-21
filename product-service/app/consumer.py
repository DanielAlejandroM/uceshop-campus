import os
import json
import time
import pika
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def process_order_created_event(ch, method, properties, body):
    """Callback que procesa el evento y descuenta el stock en la base de datos de productos"""
    try:
        data = json.loads(body)
        print(f" [x] Mensaje recibido de RabbitMQ para Orden #{data.get('order_id')}")

        db: Session = SessionLocal()
        try:
            for item in data.get("items", []):
                product_id = item["product_id"]
                quantity = item["quantity"]

                product = db.query(Product).filter(Product.id == product_id).first()
                if product:
                    if product.stock >= quantity:
                        product.stock -= quantity
                        print(f"   -> Stock actualizado para '{product.name}' (ID: {product_id}): Nuevo stock = {product.stock}")
                    else:
                        print(f"   [!] Stock insuficiente para el producto ID {product_id}")
            db.commit()
        finally:
            db.close()

        # Confirmar recepción exitosa del mensaje
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Error al procesar evento en consumidor: {e}")

def start_consumer():
    """Inicia el bucle de escucha de RabbitMQ con reintentos de conexión"""
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
            )
            channel = connection.channel()
            channel.queue_declare(queue='order_created_queue', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='order_created_queue', on_message_callback=process_order_created_event)

            print(" [*] Consumidor de RabbitMQ iniciado en Product Service. Esperando eventos...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print(" [!] RabbitMQ aún no está disponible. Reintentando conexión en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f" [!] Error inesperado en consumidor: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_consumer()