from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, max

spark = (
    SparkSession.builder
    .appName("ConsumoElectricoStreaming")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

mensajes = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "consumo-electrico")
    .option("startingOffsets", "latest")
    .load()
)

consumos = (
    mensajes
    .selectExpr("CAST(value AS STRING) AS texto")
    .select(col("texto").cast("double").alias("consumo"))
    .filter(col("consumo").isNotNull())
)

resumen = consumos.groupBy().agg(
    count("consumo").alias("cantidad"),
    avg("consumo").alias("promedio"),
    max("consumo").alias("maximo")
)

consulta = (
    resumen.writeStream
    .format("console")
    .outputMode("complete")
    .start()
)

consulta.awaitTermination()
