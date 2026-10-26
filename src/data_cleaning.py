from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace
from pyspark.sql.types import IntegerType, DoubleType


def get_spark():
    return SparkSession.builder \
        .appName("HospitalDataCleaning") \
        .getOrCreate()


def load_data(spark):
    path = "hdfs://localhost:9000/healthcare_project/raw/hospital_discharge_sample.csv"

    df = spark.read.csv(
        path,
        header=True,
        inferSchema=True
    )

    return df


def clean_data(df):

    # Select useful columns for the project
    selected_columns = [
        "Health Service Area",
        "Hospital County",
        "Facility Name",
        "Age Group",
        "Gender",
        "Race",
        "Length of Stay",
        "Type of Admission",
        "Patient Disposition",
        "CCS Diagnosis Description",
        "APR Severity of Illness Description",
        "APR Risk of Mortality",
        "Total Charges",
        "Total Costs"
    ]

    df = df.select(selected_columns)

    # Convert Length of Stay to integer
    df = df.withColumn(
        "Length of Stay",
        regexp_replace(col("Length of Stay"), "[^0-9]", "").cast(IntegerType())
    )

    # Convert money columns to numeric values
    df = df.withColumn(
        "Total Charges",
        col("Total Charges").cast(DoubleType())
    )

    df = df.withColumn(
        "Total Costs",
        col("Total Costs").cast(DoubleType())
    )

    # Remove rows with missing important values
    df = df.dropna(
        subset=[
            "Facility Name",
            "Age Group",
            "Gender",
            "Length of Stay",
            "Total Charges",
            "Total Costs"
        ]
    )

    # Remove invalid Length of Stay values
    df = df.filter(col("Length of Stay") > 0)

    # Remove duplicate records
    df = df.dropDuplicates()

    return df


if __name__ == "__main__":

    spark = get_spark()

    print("Loading hospital data...")

    df = load_data(spark)

    print("Original rows:", df.count())

    print("Cleaning data...")

    clean_df = clean_data(df)

    print("Cleaned rows:", clean_df.count())

    print("\nCleaned columns:")
    print(clean_df.columns)

    print("\nSample cleaned data:")
    clean_df.show(5, truncate=False)

    # Save cleaned data to HDFS
    output_path = "hdfs://localhost:9000/healthcare_project/cleaned"

    clean_df.write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(output_path)

    print("\nCleaned data saved to HDFS.")

    spark.stop()
