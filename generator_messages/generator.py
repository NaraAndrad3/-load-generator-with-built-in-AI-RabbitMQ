# generator.py

import pika
import time
import random
import os


rabbitmq_host = 'rabbitmq'
exchange_name = 'mensagens'


faces_dir = '/app/images/faces'
objetos_dir = '/app/images/objects'

arquivos_faces = [f for f in os.listdir(faces_dir) if os.path.isfile(os.path.join(faces_dir, f))]
arquivos_objetos = [f for f in os.listdir(objetos_dir) if os.path.isfile(os.path.join(objetos_dir, f))]

tipos_mensagens = ['face', 'objects']

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar com RabbitMQ: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)

connection, channel = connect_rabbitmq()

try:
    while True:
        tipo = random.choice(tipos_mensagens)
        if tipo == 'face':
            if arquivos_faces:
                routing_key = 'face'
                mensagem = random.choice(arquivos_faces)
                channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=mensagem.encode())
                print(f"Enviada mensagem (face): '{mensagem}'")
            else:
                print(" Sem imagens de rosto disponíveis.")
                time.sleep(1)
                continue
        else:
            if arquivos_objetos:
                routing_key = 'objects'
                mensagem = random.choice(arquivos_objetos)
                channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=mensagem.encode())
                print(f"Enviada mensagem (objects): '{mensagem}'")
            else:
                print("Sem imagens de time disponíveis.")
                time.sleep(1)
                continue

        time.sleep(0.2)  # --> 5 mensagens por segundo

except pika.exceptions.AMQPConnectionError as e:
    print(f"Erro de conexão com o RabbitMQ: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()