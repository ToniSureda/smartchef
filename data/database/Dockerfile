FROM postgres:17

# Copiamos el script de arranque a la carpeta mágica y le damos permisos
COPY init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Copiamos tu base de datos a una carpeta temporal para que pg_restore la lea
COPY SmartChefBBDD.sql /tmp/SmartChefBBDD.sql