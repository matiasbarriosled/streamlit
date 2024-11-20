# Utilizamos una imagen base de Python con Streamlit preinstalado
FROM python:3.9-slim-buster

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt
COPY requirements.txt requirements.txt

# Instalamos las dependencias
RUN pip install -r requirements.txt

# Copiamos el código de la aplicación
COPY . .

# Exponemos el puerto donde se ejecutará Streamlit (por defecto 8501)
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]