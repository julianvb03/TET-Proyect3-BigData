from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, sum as spark_sum, avg

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Project3_ETL") \
    .getOrCreate()

# Define the S3 bucket name
BUCKET_NAME = "st0263-proyecto3"

# Define input paths for raw data
raw_country_csv = f"s3://{BUCKET_NAME}/raw/country_data.csv"
raw_covid_csv   = f"s3://{BUCKET_NAME}/raw/covid_data.csv"

# Define output paths for transformed data
trusted_joined_path = f"s3://{BUCKET_NAME}/trusted/joined/"
analytics_path      = f"s3://{BUCKET_NAME}/trusted/analytics/"

# Read country-level data from S3 (comma-separated)
df_country = spark.read \
    .option("header", True) \
    .option("sep", ",") \
    .option("inferSchema", True) \
    .csv(raw_country_csv)

# Read COVID-19 data from S3 (comma-separated)
df_covid = spark.read \
    .option("header", True) \
    .option("sep", ",") \
    .option("inferSchema", True) \
    .csv(raw_covid_csv)

print("📄 Columns in df_covid:", df_covid.columns)
print("📄 Columns in df_country:", df_country.columns)

# Format 'last_updated_date' if the column exists
if "last_updated_date" in df_covid.columns:
    df_covid = df_covid.withColumn("last_updated_date", to_date(col("last_updated_date"), "yyyy/MM/d"))

# Drop unnecessary columns from COVID data if present (they exist in country data)
for col_name in ["continent", "iso_code"]:
    if col_name in df_covid.columns:
        df_covid = df_covid.drop(col_name)

# Join both datasets using 'location' as key (left join to preserve all COVID data)
df_joined = df_covid.join(df_country, on="location", how="left")

# Add a calculated column: cases per thousand people
df_transformed = df_joined.withColumn(
    "cases_per_thousand",
    col("total_cases") / col("population") * 1000
)

# Save the full joined dataset as Parquet, partitioned by continent
df_transformed.repartition(3).write \
    .mode("overwrite") \
    .partitionBy("continent") \
    .parquet(trusted_joined_path)

# Create a summary table grouped by continent
df_summary = df_transformed.groupBy("continent").agg(
    spark_sum("total_cases").alias("total_cases"),
    spark_sum("total_deaths").alias("total_deaths"),
    avg("cases_per_thousand").alias("avg_cases_per_thousand")
)

# Save the summary as Parquet in the analytics zone
df_summary.write.mode("overwrite").parquet(analytics_path)

print("✅ ETL completed successfully.")
