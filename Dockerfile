FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update -y && \
    apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .
EXPOSE 50051

CMD ["python3", "main.py"]