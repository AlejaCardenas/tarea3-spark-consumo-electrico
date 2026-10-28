from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring, round as spark_round

def main():
    #Ubicaciones del archivo original y de los resultados.
    carpeta = Path(__file__).resolve().parent
    archivo = carpeta / "datos" / "household_power_consumption.txt"
    salida = carpeta / "resultados" / "promedio_por_hora"

    #Iniciar Spark
    spark = (
        SparkSession.builder
        .appName("AnalisisConsumoElectrico")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    #Cargar el archivo original, separado por punto y coma.
    datos = (
        spark.read
        .option("header", True)
        .option("sep", ";")
        .csv(str(archivo))
    )

    print("\n--- EXPLORACION INICIAL ---")
    print("Total de registros: ", datos.count())
    datos.printSchema()
    datos.select("Date", "Time", "Global_active_power").show(5)

    #Convertir la potencia a numero y conservar los valores validos.
    preparados = datos.withColumn(
        "potencia_kw",
        col("Global_active_power").cast("double")
    )

    limpios = preparados.filter(col("potencia_kw").isNotNull())

    print("\ln--- LIMPIEZA ---")
    print(" Registros con potencia valida: ", limpios.count())
    print("Registros con potencia faltante o invalida: ", preparados.filter(col("potencia_kw").isNull()).count()
    )

    #Obtener la hora a partir de la columna Time.
    por_hora = limpios.withColumn( "hora", substring(col("Time"), 1, 2))

    #Calcular el promedio de potencia para cada hora.
    promedio_hora = (
        por_hora.groupBy("hora")
        .avg("potencia_kw")
        .select(
            "hora", spark_round(col("avg(potencia_kw)"), 4).alias("promedio_kw")
        )
        .orderBy("hora")
    )

    print("\n--- POTENCIA PROMEDIO POR HORA (kW) ---")
    promedio_hora.show(24)

    #Guardar la tabla para su posterior visualizacion.
    (
        promedio_hora.coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(str(salida))
    )

    print("\nResultado guardado en: ", salida)
    spark.stop()

if __name__ == "__main__":
    main()
