#!/bin/bash

# Definición de colores para la terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   🍳 INICIANDO SMARTCHEF (GRUPO 9)   ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Limpiar el entorno por si había algo encendido
echo -e "\n${YELLOW}[1/4] Limpiando contenedores antiguos...${NC}"
docker compose down

# 2. Levantar la infraestructura completa
echo -e "\n${YELLOW}[2/4] Construyendo y levantando servicios...${NC}"
docker compose up -d --build

# 3. Espera dinámica a que PostgreSQL acepte conexiones
echo -n -e "\n${YELLOW}[3/4] Esperando a que la Base de Datos esté lista"
RETRIES=30

# El script hace un ping real a la BBDD. Si falla, espera 1 segundo y vuelve a intentar (máximo 30s)
until docker compose exec -T db pg_isready -U smartchef > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo -n "."
  sleep 1
  let RETRIES-=1
done

if [ $RETRIES -eq 0 ]; then
    echo -e "\n${YELLOW}Advertencia: La base de datos está tardando más de lo normal.${NC}"
else
    echo -e " ${GREEN}¡Lista!${NC}"
fi

# 4. Ejecutar el Pipeline de Datos
echo -e "\n${YELLOW}[4/4] Ejecutando el pipeline de datos históricos y predicciones...${NC}"
# Descomenta la línea de abajo y ajústala al nombre de tu servicio de pipeline si es necesario
docker compose exec pipeline sh /app/run_pipeline.sh

echo -e "\n${BLUE}=========================================${NC}"
echo -e "${GREEN}DESPLIEGUE COMPLETADO CON EXITO${NC}"
echo -e "${GREEN}Accede al Dashboard en: https://localhost${NC}"
echo -e "${BLUE}=========================================${NC}"