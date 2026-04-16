FROM python:3.11-slim

WORKDIR /app

# Instalacion de dependencias minimizando el almacenamiento cache para optimizar la imagen
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Transferencia del codigo fuente al entorno de ejecucion del contenedor
COPY . .

# Definicion del comando de arranque para el servidor web y exposicion del puerto principal
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]