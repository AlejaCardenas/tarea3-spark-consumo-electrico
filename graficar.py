import csv
import glob
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = Path.home() / "tarea3-spark"
archivos = glob.glob(str(base / "resultados/promedio_por_hora/part-*.csv"))

if not archivos:
    raise FileNotFoundError("No se encontro el archivo CSV de resultados")

horas = []
promedios = []

with open(archivos[0], newline="", encoding="utf-8") as archivo:
    for fila in csv.DictReader(archivo):
        horas.append(fila["hora"])
        promedios.append(float(fila["promedio_kw"]))

plt.figure(figsize=(12,6))
plt.plot(horas, promedios, marker="o")
plt.title("Potencia activa promedio por hora")
plt.xlabel("Hora del dia")
plt.ylabel("Potencia promedio (kW)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

salida = base / "resultados/potencia_por_hora.png"
plt.savefig(salida, dpi=150)
print(f"Grafica guardada en: {salida}")
