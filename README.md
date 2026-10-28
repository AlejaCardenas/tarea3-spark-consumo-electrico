# Análisis de consumo eléctrico con Apache Spark

**Estudiante:** María Alejandra Cárdenas Anaya  
**Curso:** Datos con Apache Spark  
**Actividad:** Tarea 3 - Procesamiento de Datos con Apache Spark

## Descripción

Este proyecto analiza un conjunto de datos de consumo eléctrico mediante Apache Spark. Incluye un análisis por lotes y una demostración de procesamiento en streaming con Apache Kafka y Spark Structured Streaming.

## Archivos

- `analisis_batch.py`: procesamiento por lotes del conjunto de datos.
- `graficar.py`: generación de una gráfica a partir de los resultados.
- `lectura_kafka.py`: prueba de lectura de mensajes desde Kafka.
- `consumo_streaming.py`: lectura de valores numéricos desde Kafka y cálculo acumulado de cantidad, promedio y máximo.

## Resultados

En el análisis por lotes se obtuvieron **2.049.280 registros válidos**.

Para comprobar el procesamiento en streaming se enviaron los valores de prueba 1.0, 2.0 y 3.0. Spark mostró una cantidad de 3, un promedio de 2.0 y un máximo de 3.0. Estos valores fueron ingresados para la prueba.

## Herramientas

- Ubuntu en una máquina virtual.
- Apache Spark 3.5.8.
- Apache Kafka 3.9.2.
- Python y PySpark.

## Ejecución del streaming

Con ZooKeeper y Kafka iniciados, y el tema `consumo-electrico` creado, ejecutar:

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8 consumo_streaming.py
```

Luego enviar valores numéricos al tema `consumo-electrico` mediante un productor de Kafka. El resumen se muestra en la consola de Spark.

## Datos

El conjunto de datos utilizado para el análisis por lotes se encuentra en la carpeta `datos` de la máquina virtual. Pendiente: agregar aquí el enlace de su fuente y las instrucciones exactas para prepararlo.