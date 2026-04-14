
import os
import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

## Carga del CSV

## PONER RUTA DONDE ESTEN LOS CSVs
DATA_DIR = r""

VENTAS = os.path.join(DATA_DIR, "ventas_historico_limpio.csv")
CONTEXTO = os.path.join(DATA_DIR, "dim_context.csv")
PLATOS = os.path.join(DATA_DIR, "maestro_platos_limpio.csv")
RECETAS = os.path.join(DATA_DIR, "recetas_ingredientes_limpio.csv")

## Carga de Datos

ventas = pd.read_csv(VENTAS, parse_dates=["fecha"])
contexto = pd.read_csv(CONTEXTO, parse_dates=["date"], encoding="latin-1")
platos = pd.read_csv(PLATOS)
recetas = pd.read_csv(RECETAS)

## FEATURES DE RECETAS

recetas_feat = (
    recetas
    .groupby("id_plato")
    .agg(
        num_ingredientes=("ingrediente", "count"),
        coste_medio=("coste_unitario_kg", "mean")
    )
    .reset_index()
)

## DataSet de entrenamiento

ventas_dia = (
    ventas
    .groupby(["fecha", "id_plato"], as_index=False)
    .agg(total_vendido=("cantidad", "sum"))
)

df = (
    ventas_dia
    .merge(contexto, left_on="fecha", right_on="date")
    .merge(platos, on="id_plato")
    .merge(recetas_feat, on="id_plato")
)

df.drop(columns=["date"], inplace=True)

## Preprocesado

le_day = LabelEncoder()
le_cat = LabelEncoder()
le_plato = LabelEncoder()

df["day_of_week"] = le_day.fit_transform(df["day_of_week"])
df["categoria"] = le_cat.fit_transform(df["categoria"])
df["id_plato"] = le_plato.fit_transform(df["id_plato"])

X = df[
    [
        "id_plato",
        "categoria",
        "precio_venta",
        "num_ingredientes",
        "coste_medio",
        "is_holiday",
        "es_vispera",
        "day_of_week",
        "temp_max",
        "precipitation"
    ]
]

y = df["total_vendido"]

## Entrenamiento

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

print("Modelo entrenado")


## Predicción Futura

ultima_fecha = df["fecha"].max()
horizonte = 7

contexto_futuro = contexto[
    contexto["date"] > ultima_fecha
].head(horizonte)

predicciones = []
id_counter = 1

for _, ctx in contexto_futuro.iterrows():
    for _, plato in platos.iterrows():

        receta = recetas_feat[recetas_feat["id_plato"] == plato["id_plato"]].iloc[0]

        X_pred = pd.DataFrame([{
            "id_plato": le_plato.transform([plato["id_plato"]])[0],
            "categoria": le_cat.transform([plato["categoria"]])[0],
            "precio_venta": plato["precio_venta"],
            "num_ingredientes": receta["num_ingredientes"],
            "coste_medio": receta["coste_medio"],
            "is_holiday": ctx["is_holiday"],
            "es_vispera": ctx["es_vispera"],
            "day_of_week": le_day.transform([ctx["day_of_week"]])[0],
            "temp_max": ctx["temp_max"],
            "precipitation": ctx["precipitation"]
        }])

        # Predicción por árbol
        tree_preds = np.array([
            tree.predict(X_pred)[0] for tree in model.estimators_
        ])

        pred = tree_preds.mean()
        low = np.percentile(tree_preds, 10)
        high = np.percentile(tree_preds, 90)

        predicciones.append({
            "id_prediction": id_counter,
            "fecha_prediccion": ctx["date"],
            "id_plato": str(plato["id_plato"]),
            "cantidad_predicha": round(pred, 2),
            "intervalo_confianza": f"{round(low,2)} - {round(high,2)}"
        })

        id_counter += 1

pred_df = pd.DataFrame(predicciones)

## Export CSV Final


EXPORT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "exports",
    "predictions"
)

os.makedirs(EXPORT_DIR, exist_ok=True)

output_path = os.path.join(EXPORT_DIR, "fact_predictions_ml.csv")
pred_df.to_csv(output_path, index=False, encoding="utf-8")

print("CSV final generado:")
print(output_path)











