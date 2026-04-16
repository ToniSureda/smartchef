FROM nginx:alpine

# Borramos lo que venga por defecto
RUN rm -rf /usr/share/nginx/html/*

# Copiamos todo el contenido de tu carpeta frontend
COPY . /usr/share/nginx/html/

# Forzamos permisos de lectura para que Nginx no se queje
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]