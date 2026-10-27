from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestConnection") \
    .master("local[*]") \
    .getOrCreate()

print("Spark version:", spark.version)
print("SUCCESS - PySpark is working!")

spark.stop()
