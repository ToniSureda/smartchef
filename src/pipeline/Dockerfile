FROM python:3.11-slim

# Instalacion del servicio cron para la programacion de tareas
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar las librerías necesarias para el pipeline
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los scripts
COPY . .

# Programacion de la ejecucion automatica del pipeline a las 3:00 AM diariamente
RUN echo "0 3 * * * root /app/run_pipeline.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/pipeline_cron

# Asignacion de permisos de seguridad y registro de la tarea en el sistema
RUN chmod 0644 /etc/cron.d/pipeline_cron
RUN crontab /etc/cron.d/pipeline_cron
RUN chmod +x /app/run_pipeline.sh

# Inicializacion del archivo log
RUN touch /var/log/cron.log

# Exportacion de variables de entorno al servicio cron y monitorizacion continua
CMD printenv > /etc/environment && cron && tail -f /var/log/cron.log