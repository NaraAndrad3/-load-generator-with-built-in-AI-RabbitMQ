FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "facer.py"]


