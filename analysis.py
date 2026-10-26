from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, max, min, sum


def get_spark():
    return SparkSession.builder \
        .appName("HospitalDataAnalysis") \
        .getOrCreate()


def load_clean_data(spark):
    path = "hdfs://localhost:9000/healthcare_project/cleaned"

    df = spark.read.csv(
        path,
        header=True,
        inferSchema=True
    )

    return df


if __name__ == "__main__":

    spark = get_spark()

    print("Loading cleaned hospital data...")

    df = load_clean_data(spark)

    print("Total records:", df.count())

    print("\n1. Patients by Age Group")
    df.groupBy("Age Group") \
        .count() \
        .orderBy("count", ascending=False) \
        .show()

    print("\n2. Patients by Gender")
    df.groupBy("Gender") \
        .count() \
        .orderBy("count", ascending=False) \
        .show()

    print("\n3. Top 10 Hospitals by Patient Count")
    df.groupBy("Facility Name") \
        .count() \
        .orderBy("count", ascending=False) \
        .show(10, truncate=False)

    print("\n4. Average Length of Stay")
    df.select(
        avg("Length of Stay").alias("Average Length of Stay")
    ).show()

    print("\n5. Average Total Charges")
    df.select(
        avg("Total Charges").alias("Average Total Charges")
    ).show()

    print("\n6. Patients by Type of Admission")
    df.groupBy("Type of Admission") \
        .count() \
        .orderBy("count", ascending=False) \
        .show()

    print("\n7. Patients by Risk of Mortality")
    df.groupBy("APR Risk of Mortality") \
        .count() \
        .orderBy("count", ascending=False) \
        .show()

    print("\n8. Patients by Severity of Illness")
    df.groupBy("APR Severity of Illness Description") \
        .count() \
        .orderBy("count", ascending=False) \
        .show()

    print("\nAnalysis completed successfully.")

    spark.stop()