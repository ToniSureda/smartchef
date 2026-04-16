# SmartChef — Sistema Predictivo de Aprovisionamiento HORECA

> Proyecto del Curso de Especialización en Inteligencia Artificial y Big Data · Grupo 9

---

## 📋 Descripción

SmartChef es una solución integral diseñada para optimizar la cadena de suministro en el sector restauración. Utiliza técnicas de Machine Learning para predecir la demanda semanal de ingredientes, cruzando el histórico de ventas y escandallos con variables externas como meteorología y festivos locales.

El sistema permite a los gerentes reducir el desperdicio alimentario y optimizar el stock mediante recomendaciones de compra basadas en datos reales.

---

## 👥 Equipo

| Miembro | Rol |
|---|---|
| **Toni Sureda** | Arquitectura de microservicios (Docker) · Frontend (Dashboard interactivo) |
| **Alejandro Fernández** | Núcleo de Machine Learning · Estructura del Backend · Endpoints de la API |
| **Hugo Barrera** | Persistencia en Base de Datos · Módulo de Ingest · Alimentación del modelo |
| **Blas Martos** | Procesos ETL · Mock Data · Integración con APIs meteorológicas |

---

## 🏗️ Arquitectura

El sistema está completamente contenedorizado mediante Docker Compose, dividido en cuatro capas:

```
┌─────────────────────────────────────────────────────┐
│  4. Presentación   Nginx + HTML/JS/CSS + Chart.js   │  :80
├─────────────────────────────────────────────────────┤
│  3. Servicio       FastAPI (API REST)                │  :8000
├─────────────────────────────────────────────────────┤
│  2. Procesamiento  Pipeline ETL + Modelo ML          │
├─────────────────────────────────────────────────────┤
│  1. Datos          PostgreSQL                        │  :5432
└─────────────────────────────────────────────────────┘
```

- **Capa de Datos** — PostgreSQL almacena el histórico de ventas, recetas, contexto climático y las predicciones generadas por el modelo.
- **Capa de Procesamiento** — Orquestador Python que ejecuta limpieza (ETL), sincronización incremental y entrenamiento del modelo de IA.
- **Capa de Servicio** — API REST que procesa la lógica de negocio y sirve los datos procesados.
- **Capa de Presentación** — Dashboard web interactivo que visualiza KPIs, tendencias y alertas de riesgo de desperdicio.

---

## 🛠️ Stack Tecnológico

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Base de datos | PostgreSQL 17 |
| API | FastAPI + Uvicorn |
| Machine Learning | Scikit-learn · XGBoost |
| Frontend | Vanilla JS · Chart.js · CSS3 |
| Servidor web | Nginx |
| Infraestructura | Docker · Docker Compose |

---

## 🚀 Ejecución rápida

### Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

### Pasos

**1. Clonar el repositorio**

```bash
git clone https://github.com/ToniSureda/smartchef.git
cd smartchef
```

**2. Levantar los contenedores**

```bash
docker compose up --build
```

Este comando construye las imágenes, inicializa la base de datos con el esquema y los datos históricos, y arranca todos los servicios automáticamente.

**3. Ejecutar el pipeline (primera carga y predicción)**

```bash
docker exec -it smartchef_pipeline bash run_pipeline.sh
```

**4. Acceder al sistema**

| Servicio | URL |
|---|---|
| Dashboard | http://localhost |
| API Swagger | http://localhost:8000/docs |

---

## 📁 Estructura del proyecto

```
smartchef/
├── data/
│   ├── clean_data/
│   │   ├── dim_context.csv
│   │   ├── maestro_platos_limpio.csv
│   │   ├── recetas_ingredientes_limpio.csv
│   │   └── ventas_historico_limpio.csv
│   ├── database/
│   │   ├── Dockerfile
│   │   ├── init-db.sh
│   │   ├── SmartChefBBDD.sql
│   │   └── SmartChefBBDD.txt
│   └── raw_data/
│       ├── agentes_externos.csv
│       └── ventas_historico_sucio.csv
├── docs/
│   ├── arquitectura.png
│   └── fase1_grupo9.pdf
├── src/
│   ├── backend/
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── context.py
│   │   │   ├── menu.py
│   │   │   ├── predictions.py
│   │   │   ├── recipes.py
│   │   │   └── sales.py
│   │   ├── exports/
│   │   │   ├── compras_historico/
│   │   │   │   └── 2026-04-13_historico_compras.csv
│   │   │   └── predictions/
│   │   │       └── fact_predictions_ml.csv
│   │   ├── repos/
│   │   │   ├── __init__.py
│   │   │   ├── compras_repo.py
│   │   │   ├── context_repo.py
│   │   │   ├── menu_repo.py
│   │   │   ├── predictions_repo.py
│   │   │   ├── recipes_repo.py
│   │   │   └── Sales_repo.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── export_compras.py
│   │   │   ├── import_predictions.py
│   │   │   └── train_predictions.py
│   │   ├── database.py
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── dashboard.css
│   │   ├── dashboard.js
│   │   ├── Dockerfile
│   │   └── index.html
│   └── pipeline/
│       ├── context_init.py
│       ├── context_update.py
│       ├── db_sync.py
│       ├── Dockerfile
│       ├── generate_raw_historic.py
│       ├── ingest.py
│       ├── requirements.txt
│       └── run_pipeline.sh
├── docker-compose.yml
├── .gitignore
└── README.md
```

---



*Curso de Especialización en IA y Big Data · Modalidad Online · Grupo 9*
