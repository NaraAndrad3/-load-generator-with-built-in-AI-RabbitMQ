# consumer_face.py

import pika
import time
from deepface import DeepFace
import os

# Configurações do RabbitMQ
rabbitmq_host = 'rabbitmq'
exchange_name = 'mensagens'
routing_key = 'face'
queue_name = 'fila_sentimentos'
image_path = '/app/images/faces' # Caminho dentro do container

def analisar_sentimento(img_name):
    try:
        img_path = os.path.join(image_path, img_name)
        result = DeepFace.analyze(img_path=img_path, actions=['emotion'], silent=True)
        if result:
            dominant = result[0]["dominant_emotion"]
            return f"Emoção dominante: {dominant}"
        else:
            return "Não foi possível analisar a emoção."
    except Exception as e:
        return f"Erro ao analisar a emoção: {e}"

def callback(ch, method, properties, body):
    mensagem = body.decode()
    print(f"Mensagem recebida (Sentimentos): {mensagem}")
    resultado_ia = analisar_sentimento(mensagem)
    print(f"Análise de Sentimento da mensagem: {mensagem}: {resultado_ia}")
    time.sleep(1) 
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

    print(' [*] Aguardando mensagens (Sentimentos). Para sair, pressione CTRL+C')
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print(f"Erro de conexão com o RabbitMQ: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()