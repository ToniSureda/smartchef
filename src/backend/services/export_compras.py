import os
from datetime import date
from repos.compras_repo import get_historico_compras

# Ruta base del backend
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Carpeta de salida
EXPORT_DIR = os.path.join(
    BASE_DIR,
    "exports",
    "compras_historico"
)

os.makedirs(EXPORT_DIR, exist_ok=True)


# Nombre del archivo con fecha
today = date.today().isoformat()
filename = f"{today}_historico_compras.csv"
output_path = os.path.join(EXPORT_DIR, filename)


# Obtener datos desde el repo
df = get_historico_compras()


# Exportar CSV
df.to_csv(output_path, index=False, encoding="utf-8")


print(f"CSV generado correctamente en: {output_path}")
print(f"Filas exportadas: {len(df)}")




