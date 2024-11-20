FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8081

HEALTHCHECK CMD curl --fail http://localhost:8081/_stcore/health
ENTRYPOINT [ "streamlit","run","app.py","--server.port=8081","--server.address=0.0.0.0"]