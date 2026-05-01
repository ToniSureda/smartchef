FROM postgres:17

# Transferencia del script de inicializacion al directorio de autoarranque y asignacion de permisos de ejecucion
COPY init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Aprovisionamiento del archivo de volcado en un directorio temporal para su procesamiento durante el despliegue
COPY SmartChefBBDD.sql /tmp/SmartChefBBDD.sql