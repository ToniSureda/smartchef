FROM nginx:alpine

# Eliminacion del contenido estatico predeterminado del servidor base
RUN rm -rf /usr/share/nginx/html/*

# Transferencia de los activos del frontend al directorio de despliegue
COPY . /usr/share/nginx/html/

# Asignacion de permisos de lectura y ejecucion para garantizar el acceso web
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]