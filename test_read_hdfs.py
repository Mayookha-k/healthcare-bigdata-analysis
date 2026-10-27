from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ReadFromHDFS") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read.csv(
    "hdfs://localhost:9000/healthcare_project/raw/hospital-inpatient-discharges-sparcs-de-identified-2010-1-selected-columns.csv",
    header=True,
    inferSchema=False
)

print("Row count:", df.count())
print("Column count:", len(df.columns))
print("Columns:", df.columns)
df.show(5)

spark.stop()
