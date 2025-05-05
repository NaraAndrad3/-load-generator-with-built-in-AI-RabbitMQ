# Projeto de Análise de Imagens com Filas RabbitMQ

Este projeto demonstra uma arquitetura de processamento de imagens utilizando filas de mensagens RabbitMQ para desacoplar as etapas de geração e análise de imagens. O sistema é composto por três serviços principais, orquestrados com Docker Compose:

* **Gerador (`gerador`):** Responsável por selecionar aleatoriamente arquivos de imagem de duas pastas (`images/faces` e `images/objects`) e enviar o nome do arquivo como uma mensagem para o RabbitMQ, roteando-as para exchanges específicas (`face` ou `objects`).
* **Consumidor de Sentimentos (`consumer_face`):** Um consumidor do RabbitMQ que recebe mensagens roteadas para a fila de sentimentos (`fila_sentimentos`). Ele utiliza a biblioteca `deepface` para analisar as emoções faciais nas imagens recebidas.
* **Consumidor de Objetos (`consumer_objects`):** Outro consumidor do RabbitMQ que recebe mensagens roteadas para a fila de objetos (`fila_objetos`). Ele utiliza o modelo YOLOv8 para detectar objetos nas imagens recebidas.
* **RabbitMQ (`rabbitmq`):** O broker de mensagens que facilita a comunicação assíncrona entre os serviços.

## Pré-requisitos

* **Docker:** Certifique-se de ter o Docker instalado em sua máquina. Você pode encontrar as instruções de instalação para sua plataforma em [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).
* **Docker Compose:** O Docker Compose geralmente é instalado junto com o Docker Desktop. Se você precisa instalá-lo separadamente, siga as instruções em [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).
* **Imagens nas pastas `images/faces` e `images/objects`:** Crie as pastas `images/faces` e `images/objects` no mesmo diretório do arquivo `docker-compose.yaml` e adicione arquivos de imagem (JPG, PNG, etc.) relevantes para análise de rosto e detecção de objetos, respectivamente.

## 📦 Estrutura do projeto e seus Componentes

```
.
├── consumer_face/
│   ├── consumer_face.py
│   └── Dockerfile
│   └── requirements.txt
├── consumer_objects/
│   ├── consumer_objects.py
│   └── Dockerfile
│   └── requirements.txt
├── gerador/
│   ├── generator.py
│   └── Dockerfile
│   └── requirements.txt
├── images/
│   ├── faces/
│   └── objects/
└── docker-compose.yaml
```

## Como Executar o Projeto

1.  **Clone este repositório  ou crie a estrutura de arquivos conforme descrito.** Certifique-se de ter os arquivos e pastas na estrutura correta.

2.  **Navegue até o diretório raiz do projeto no seu terminal.** Este diretório deve conter o arquivo `docker-compose.yaml` e a pasta `images`.

3.  **Execute o comando para subir os containers:**

    ```bash
    docker-compose up -d --build ou docker-compose up
    ```

    A flag `-d` faz com que os containers rodem em background, e a flag `--build` garante que as imagens Docker sejam construídas (ou reconstruídas, se houver alterações) antes de iniciar os containers.

4.  **Acompanhe os logs dos serviços:**

    Para ver os logs de um serviço específico, use:

    ```bash
    docker-compose logs <nome_do_servico>
    ```

    No caso deste projeto:

    ```bash
    docker-compose logs gerador
    docker-compose logs consumidor_sentimentos
    docker-compose logs consumidor_objetos
    docker-compose logs rabbitmq
    ```

5.  **Acesse a interface de gerenciamento do RabbitMQ (opcional):**

    Se configurado corretamente (verifique a seção `ports` no `docker-compose.yaml`), você pode acessar a interface web do RabbitMQ Management Plugin através do seu navegador na porta 15672 (geralmente `http://localhost:15672`). As credenciais padrão são `guest/guest`. Nesta interface, você pode monitorar as exchanges (`mensagens`), as filas (`fila_sentimentos`, `fila_objetos`) e as mensagens.

## Como Funciona

1.  O `gerador` escolhe aleatoriamente um arquivo de imagem das pastas `images/faces` ou `images/objects`.
2.  O nome do arquivo é publicado no exchange `mensagens` do RabbitMQ.
    * Se a imagem for escolhida da pasta `faces`, a mensagem é roteada com a routing key `face`.
    * Se a imagem for escolhida da pasta `objects`, a mensagem é roteada com a routing key `objects`.
3.  O `consumidor_sentimentos` está vinculado à fila `fila_sentimentos` com a routing key `face` e consome as mensagens correspondentes, realizando a análise de sentimentos faciais com `deepface`.
4.  O `consumidor_objetos` está vinculado à fila `fila_objetos` com a routing key `objects` e consome as mensagens correspondentes, realizando a detecção de objetos com YOLOv8.
5.  Os resultados das análises são impressos nos logs dos respectivos consumidores.

## Alterando as Imagens

Para adicionar, remover ou modificar as imagens nas pastas `images/faces` e `images/objects`, basta alterar os arquivos nessas pastas no seu sistema de arquivos local.

## Autores

Nara Raquel Dias Andrade
