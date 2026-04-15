FROM python:3.11-slim

# Instalar cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar las librerías necesarias para tu pipeline
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los scripts
COPY . .

# CONFIGURAR EL CRONTAB PARA LAS 3:00 AM
# "0 3 * * *" significa -> Minuto 0, Hora 3, Todos los días.
# OJO: Suponiendo que context_update.py es el que actualiza los CSV
RUN echo "0 3 * * * root /app/run_pipeline.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/pipeline_cron

# Dar permisos al archivo cron
RUN chmod 0644 /etc/cron.d/pipeline_cron
RUN crontab /etc/cron.d/pipeline_cron
RUN chmod +x /app/run_pipeline.sh

# Crear el archivo de logs para poder ver si falla o acierta
RUN touch /var/log/cron.log

# El TRUCO: Pasamos las variables de entorno a cron y lo dejamos corriendo
CMD printenv > /etc/environment && cron && tail -f /var/log/cron.log