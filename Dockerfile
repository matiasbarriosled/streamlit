FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health
ENTRYPOINT [ "streamlit","run","app.py","--server.port=8080","--server.address=0.0.0.0"]