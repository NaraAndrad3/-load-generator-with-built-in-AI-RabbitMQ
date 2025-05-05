# consumer_objects.py

import pika
import time
from ultralytics import YOLO
import os


rabbitmq_host = 'rabbitmq'
exchange_name = 'mensagens'
routing_key = 'objects'  
queue_name = 'fila_objetos'
image_path = '/app/images/objects'

# Carregar o modelo YOLO
model = YOLO('yolov8n.pt')
names = model.names

def identificar_objeto(img_name):
    try:
        img_path = os.path.join(image_path, img_name)
        results = model(img_path, verbose=False)
        detections = []
        for box in results[0].boxes:
            cls_id = int(box.cls.item())
            conf = float(box.conf.item())
            label = names[cls_id]
            detections.append(f"{label} ({conf:.2%})")
        if detections:
            return f"Objetos detectados: {', '.join(detections)}"
        else:
            return "Nenhum objeto detectado."
    except Exception as e:
        return f"Erro ao identificar objetos: {e}"

def callback(ch, method, properties, body):
    mensagem = body.decode()
    print(f"Mensagem (Objetos): {mensagem}")
    resultado_ia = identificar_objeto(mensagem)
    print(f" Análise de Objetos da mensagem {mensagem}: {resultado_ia}")
    time.sleep(1.5) 

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar com RabbitMQ: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)

connection, channel = connect_rabbitmq()

try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens (Objetos)')
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print(f"Erro de conexão com o RabbitMQ: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()