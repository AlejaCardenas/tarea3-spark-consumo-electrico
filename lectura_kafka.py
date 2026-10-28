from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("LecturaKafka")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

mensajes = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "consumo-electrico")
    .option("startingOffsets", "earliest")
    .load()
)

texto = mensajes.selectExpr("CAST(value AS STRING) AS mensaje")

consulta = (
    texto.writeStream
    .format("console")
    .outputMode("append")
    .start()
)

consulta.awaitTermination()
