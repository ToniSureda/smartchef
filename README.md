# SmartChef - Predicción de Demanda de Ingredientes

Este repositorio contiene el código y la documentación del proyecto SmartChef, desarrollado para el Curso de Especialización en Inteligencia Artificial y Big Data (Grupo 9).

## Descripción del Proyecto

SmartChef es una herramienta de apoyo para restaurantes que utiliza Machine Learning para predecir la demanda semanal de ingredientes perecederos. El sistema cruza los datos históricos de ventas y recetas (escandallos) con variables externas como el clima, las reservas y los festivos locales. 

El objetivo principal es generar recomendaciones de compra precisas para ayudar a los gerentes a reducir el desperdicio de alimentos y evitar roturas de stock.

## Equipo

* **Alejandro Fernández** - Data
* **Antoni Sureda** - Platform
* **Blas Martos** - Machine Learning
* **Hugo Barrera** - Project Management / BI

## Arquitectura del Sistema

La infraestructura está diseñada para funcionar mediante procesamiento por lotes (batch) y se divide en cuatro capas:

1. **Fuentes de datos:** Ingesta de archivos CSV (tickets y recetas) y llamadas a APIs públicas (meteorología y calendario).
2. **ETL y Almacenamiento:** Pipeline en Python que limpia, transforma y unifica los datos para guardarlos en PostgreSQL.
3. **Machine Learning y Backend:** El modelo lee el histórico de la base de datos, genera las predicciones y las guarda de nuevo. Una API REST construida con FastAPI se encarga de servir estos datos.
4. **Presentación:** Un dashboard interactivo en Power BI que consume la API para mostrar los KPIs y recomendaciones finales al usuario.

## Stack Tecnológico

* Python
* PostgreSQL
* FastAPI
* Scikit-learn / XGBoost
* Power BI

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/ToniSureda/smartchef-fase1.git](https://github.com/ToniSureda/smartchef-fase1.git)
