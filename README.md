# 🍳 SmartChef - Sistema Predictivo de Aprovisionamiento HORECA

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql)

> Proyecto del Curso de Especialización en Inteligencia Artificial y Big Data · **Grupo 9**

---

## 🎥 Presentación del Proyecto

Puedes visualizar la demostración en funcionamiento y la defensa técnica de la arquitectura en el siguiente enlace:  
👉 **[Ver vídeo de presentación de SmartChef (Google Drive)](https://drive.google.com/file/d/1DpfRgoILcqygcDv487l896uOJv6hH216/view)**

---

## 📋 Descripción

SmartChef es una solución analítica diseñada para optimizar la gestión de restaurantes mediante técnicas de **Machine Learning**.

El sistema predice la demanda semanal de ingredientes perecederos combinando:

- Histórico de ventas
- Recetas (escandallos)
- Variables externas (clima, festivos, contexto)

El objetivo es generar **recomendaciones de compra precisas** que permitan:

- Reducir el desperdicio alimentario
- Evitar roturas de stock
- Optimizar costes operativos

---

## 🏗️ Arquitectura del Sistema

La solución sigue una arquitectura de microservicios completamente contenedorizada con **Docker Compose**:

```text
┌─────────────────────────────────────────────────────┐
│  Presentación   Nginx + HTML/JS/CSS + Chart.js      │  :443
├─────────────────────────────────────────────────────┤
│  Backend        FastAPI (API REST)                  │  :8000
├─────────────────────────────────────────────────────┤
│  Procesamiento  Pipeline ETL + Modelo ML            │
├─────────────────────────────────────────────────────┤
│  Datos          PostgreSQL                          │  :5432
└─────────────────────────────────────────────────────┘
```

### Capas del sistema

- **Capa de Datos:** PostgreSQL almacena ventas, recetas, contexto y predicciones.
- **Capa de Procesamiento:** Pipeline ETL + entrenamiento del modelo de IA.
- **Capa de Servicio:** API REST con FastAPI.
- **Capa de Presentación:** Dashboard web interactivo.

---

## 🛠️ Stack Tecnológico

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Base de datos | PostgreSQL |
| API | FastAPI + Uvicorn |
| Machine Learning | Scikit-learn · Random Forest |
| Frontend | Vanilla JS · Chart.js · CSS3 |
| Servidor web | Nginx |
| Infraestructura | Docker · Docker Compose |

---

## 🚀 Despliegue (Quick Start)

### Requisitos

- Docker y Docker Compose
- Linux / WSL2 / macOS

### Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd smartchef
```

2. Dar permisos al script (solo la primera vez en entornos UNIX):

```bash
chmod +x start.sh
```

3. Ejecutar el entorno:

```bash
bash start.sh
```

4. Acceder al sistema:

👉 **https://localhost**

> ⚠️ El navegador mostrará una advertencia de seguridad rutinaria debido al uso de certificados locales SSL autogenerados (necesarios para la mitigación CORS). Haz clic en "Configuración avanzada" y selecciona "Continuar a localhost (inseguro)".

---

## 🔒 Variables de Entorno y Seguridad

El proyecto sigue la metodología **12-Factor App**, delegando la gestión de secretos a variables de entorno para evitar incrustar contraseñas en el código fuente.

Es necesario crear un archivo `.env` en la raíz del proyecto antes de ejecutar el sistema (ver documentación técnica para las credenciales de evaluación académica).

---

## 👥 Equipo - Grupo 9

| Miembro | Rol Estratégico |
|---|---|
| Alejandro Fernández Fuentes | Data Engineering (Gestión, tratamiento y estructuración de datos) |
| Antoni Sureda Cardona | Platform & Architecture (Infraestructura Docker, Backend API, Frontend y Nginx) |
| Blas Martos Ortega | Machine Learning (Modelos predictivos, cálculo de IC y detección de anomalías) |
| Hugo Barrera Castillo | Project Management & BI (Coordinación, definición de KPIs y valor de negocio) |

---

> Curso de Especialización en IA y Big Data · Grupo 9
