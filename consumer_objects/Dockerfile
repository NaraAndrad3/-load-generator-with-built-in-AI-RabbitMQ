FROM python:3.9-slim-buster

WORKDIR /app

COPY objects.py .
COPY requirements.txt .

# Instala dependências do sistema para o OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Instala as bibliotecas Python
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install ultralytics

# Executa o script
CMD ["python", "objects.py"]
