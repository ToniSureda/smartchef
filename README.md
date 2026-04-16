# SmartChef - Predicción de Demanda de Ingredientes
# SmartChef — Sistema Predictivo de Aprovisionamiento HORECA

Este repositorio contiene el código y la documentación del proyecto SmartChef, desarrollado para el Curso de Especialización en Inteligencia Artificial y Big Data (Grupo 9).
> Proyecto del Curso de Especialización en Inteligencia Artificial y Big Data · Grupo 9

## Descripción del Proyecto
---

SmartChef es una herramienta de apoyo para restaurantes que utiliza Machine Learning para predecir la demanda semanal de ingredientes perecederos. El sistema cruza los datos históricos de ventas y recetas (escandallos) con variables externas como el clima, las reservas y los festivos locales. 
## 📋 Descripción

El objetivo principal es generar recomendaciones de compra precisas para ayudar a los gerentes a reducir el desperdicio de alimentos y evitar roturas de stock.
SmartChef es una solución integral diseñada para optimizar la cadena de suministro en el sector restauración. Utiliza técnicas de Machine Learning para predecir la demanda semanal de ingredientes, cruzando el histórico de ventas y escandallos con variables externas como meteorología y festivos locales.

## Equipo
El sistema permite a los gerentes reducir el desperdicio alimentario y optimizar el stock mediante recomendaciones de compra basadas en datos reales.

* **Alejandro Fernández** - Data
* **Antoni Sureda** - Platform
* **Blas Martos** - Machine Learning
* **Hugo Barrera** - Project Management / BI
---

## Arquitectura del Sistema
## 👥 Equipo

La infraestructura está diseñada para funcionar mediante procesamiento por lotes (batch) y se divide en cuatro capas:
| Miembro | Rol |
|---|---|
| **Toni Sureda** | Arquitectura de microservicios (Docker) · Frontend (Dashboard interactivo) |
| **Alejandro Fernández** | Núcleo de Machine Learning · Estructura del Backend · Endpoints de la API |
| **Hugo Barrera** | Persistencia en Base de Datos · Módulo de Ingest · Alimentación del modelo |
| **Blas Martos** | Procesos ETL · Mock Data · Integración con APIs meteorológicas |

1. **Fuentes de datos:** Ingesta de archivos CSV (tickets y recetas) y llamadas a APIs públicas (meteorología y calendario).
2. **ETL y Almacenamiento:** Pipeline en Python que limpia, transforma y unifica los datos para guardarlos en PostgreSQL.
3. **Machine Learning y Backend:** El modelo lee el histórico de la base de datos, genera las predicciones y las guarda de nuevo. Una API REST construida con FastAPI se encarga de servir estos datos.
4. **Presentación:** Un dashboard interactivo en Power BI que consume la API para mostrar los KPIs y recomendaciones finales al usuario.
---

## Stack Tecnológico
## 🏗️ Arquitectura

* Python
* PostgreSQL
* FastAPI
* Scikit-learn / XGBoost
* Power BI
El sistema está completamente contenedorizado mediante Docker Compose, dividido en cuatro capas:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/ToniSureda/smartchef-fase1.git](https://github.com/ToniSureda/smartchef-fase1.git)
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
