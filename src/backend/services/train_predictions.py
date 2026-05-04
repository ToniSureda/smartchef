import os
import pandas as pd
import numpy as np
import warnings
from datetime import date
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

warnings.filterwarnings("ignore", category=UserWarning)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

DATA_DIR = os.path.join(BASE_DIR, "data", "clean_data")

# Usamos join para que las barras funcionen bien en Linux
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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

## ENTRENAMIENTO (REGULARIZADO)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Modelo entrenado")

## EVALUACIÓN DEL MODELO

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"MAE del modelo: {mae:.2f}")

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

today = date.today().isoformat()

filename = f"fact_predictions_ml_{today}.csv"

output_path = os.path.join(EXPORT_DIR, filename)
pred_df.to_csv(output_path, index=False, encoding="utf-8")

print("CSV final generado:")
print(output_path)











