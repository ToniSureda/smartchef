from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard")
def get_dashboard():
    try:
        conn = get_connection()
        
        # 1. Extraccion de predicciones a 7 dias vista agrupadas por ingrediente
        query_pred = """
            SELECT 
                r.ingrediente, 
                SUM(p.cantidad_predicha * r.cantidad) AS kg_predicho, 
                MAX(p.intervalo_confianza) AS intervalo_confianza,
                MAX(r.unidad) AS unidad
            FROM fact_predictions p
            JOIN dim_recipes r ON p.id_plato = r.id_plato
            WHERE p.fecha_prediccion >= CURRENT_DATE AND p.fecha_prediccion < CURRENT_DATE + 7
            GROUP BY r.ingrediente
            ORDER BY kg_predicho DESC;
        """
        df_pred = pd.read_sql(query_pred, conn)

        # 2. Calculo de Indicadores Clave de Rendimiento consolidados
        query_kpis = """
           SELECT 
                COALESCE(SUM(s.cantidad * m.precio_venta), 0) AS total_revenue,
                COUNT(DISTINCT s.id_ticket) AS total_tickets,
                COALESCE(SUM(s.cantidad * m.precio_venta) / NULLIF(COUNT(DISTINCT s.id_ticket), 0), 0) AS avg_ticket,
                COUNT(DISTINCT s.fecha) AS days_analyzed
            FROM fact_sales s
            JOIN dim_menu m ON s.id_plato = m.id_plato;
        """
        df_kpis = pd.read_sql(query_kpis, conn)
        kpis = df_kpis.iloc[0].to_dict() if not df_kpis.empty else {}

        # 3. Agregacion de volumen de ventas por categoria de producto
        query_cat = """
            SELECT 
                m.categoria, 
                SUM(s.cantidad) AS unidades
            FROM fact_sales s
            JOIN dim_menu m ON s.id_plato = m.id_plato
            GROUP BY m.categoria
            ORDER BY unidades DESC;
        """
        df_cat = pd.read_sql(query_cat, conn)

        # 4. Serie temporal historica de ingresos para analisis de tendencia
        query_rev = """
            SELECT 
                TO_CHAR(s.fecha, 'YYYY-MM-DD') AS fecha, 
                SUM(s.cantidad * m.precio_venta) AS revenue
            FROM fact_sales s
            JOIN dim_menu m ON s.id_plato = m.id_plato
            GROUP BY s.fecha
            ORDER BY s.fecha ASC;
        """
        df_rev = pd.read_sql(query_rev, conn)

        # 5. Identificacion de los platos con mayor volumen de venta historico
        query_top = """
            SELECT 
                m.nombre_plato AS plato, 
                SUM(s.cantidad) AS unidades
            FROM fact_sales s
            JOIN dim_menu m ON s.id_plato = m.id_plato
            GROUP BY m.nombre_plato
            ORDER BY unidades DESC
            LIMIT 6;
        """
        df_top = pd.read_sql(query_top, conn)

        # 6. Extraccion de metricas climaticas consolidadas en ventana de 90 dias
        query_ctx = """
            SELECT 
                COALESCE(AVG(temp_max), 0) AS avg_temp,
                SUM(CASE WHEN precipitation > 0 THEN 1 ELSE 0 END) AS rainy_days,
                SUM(is_holiday) AS holiday_days
            FROM dim_context
            WHERE date <= CURRENT_DATE AND date >= CURRENT_DATE - 90;
        """
        df_ctx = pd.read_sql(query_ctx, conn)
        ctx = df_ctx.iloc[0].to_dict() if not df_ctx.empty else {}

        # 7. Cuantificacion de demanda real de ingredientes cruzando ventas con escandallos
        query_ing = """
            SELECT 
                r.ingrediente, 
                SUM(s.cantidad * r.cantidad) AS total_valor,
                MAX(r.unidad) AS unidad
            FROM fact_sales s
            JOIN dim_recipes r ON s.id_plato = r.id_plato
            WHERE s.fecha >= CURRENT_DATE - 90  
            GROUP BY r.ingrediente
            ORDER BY total_valor DESC
            LIMIT 12;
        """
        df_ing = pd.read_sql(query_ing, conn)

        # 8. Analisis predictivo de riesgo de desperdicio basado en desviacion de demanda media
        query_waste = """
            WITH predicted AS (
                SELECT r.ingrediente, SUM(p.cantidad_predicha * r.cantidad) AS kg_predicho
                FROM fact_predictions p
                JOIN dim_recipes r ON p.id_plato = r.id_plato
                WHERE p.fecha_prediccion >= CURRENT_DATE AND p.fecha_prediccion < CURRENT_DATE + 7
                GROUP BY r.ingrediente
            ),
            historical AS (
                SELECT r.ingrediente, SUM(s.cantidad * r.cantidad)/12.0 AS kg_historico_semana
                FROM fact_sales s
                JOIN dim_recipes r ON s.id_plato = r.id_plato
                WHERE s.fecha >= CURRENT_DATE - 84
                GROUP BY r.ingrediente
            )
            SELECT 
                p.ingrediente,
                ROUND(p.kg_predicho::numeric, 2) AS kg_predicho,
                ROUND(COALESCE(h.kg_historico_semana, 0)::numeric, 2) AS kg_historico_semana,
                ROUND((CASE WHEN h.kg_historico_semana > 0 
                    THEN ((p.kg_predicho - h.kg_historico_semana) / h.kg_historico_semana) * 100 
                    ELSE 0 END)::numeric, 2) AS desviacion_pct,
                CASE WHEN p.kg_predicho > (h.kg_historico_semana * 1.2) THEN 'alto'
                     WHEN p.kg_predicho < (h.kg_historico_semana * 0.8) THEN 'bajo'
                     ELSE 'medio' END AS riesgo
            FROM predicted p
            LEFT JOIN historical h ON p.ingrediente = h.ingrediente
            ORDER BY desviacion_pct DESC;
        """
        df_waste = pd.read_sql(query_waste, conn)

        conn.close()

        # Consolidacion de estructura de datos para transferencia al cliente
        return {
            "status": "success",
            "next_week_predictions": df_pred.to_dict(orient="records"),
            "kpis": kpis,
            "sales_by_category": df_cat.to_dict(orient="records"),
            "revenue_series": df_rev.to_dict(orient="records"),
            "top_dishes": df_top.to_dict(orient="records"),
            "dim_context_summary": ctx,
            "ingredient_demand": df_ing.to_dict(orient="records"),
            "waste_risk": df_waste.to_dict(orient="records")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}