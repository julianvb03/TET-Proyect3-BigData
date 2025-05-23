from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

spark = SparkSession.builder \
    .appName("Project3_ETL") \
    .getOrCreate()

BUCKET_NAME = "st0263-proyecto3"

raw_country_csv = f"s3://{BUCKET_NAME}/raw/country_data.csv"
raw_covid_csv   = f"s3://{BUCKET_NAME}/raw/covid_data.csv"

# S3 output paths,
trusted_joined_path = f"s3://{BUCKET_NAME}/trusted/joined/"
analytics_path      = f"s3://{BUCKET_NAME}/trusted/analytics/"

df_country = spark.read \
    .option("header", True) \
    .option("sep", ";") \
    .option("inferSchema", True) \
    .csv(raw_country_csv)

df_covid = spark.read \
    .option("header", True) \
    .option("sep", ";") \
    .option("inferSchema", True) \
    .csv(raw_covid_csv)

df_covid = df_covid.withColumn("last_updated_date", to_date(col("last_updated_date"), "yyyy/MM/d"))

df_covid = df_covid.drop("continent")
df_covid = df_covid.drop("iso_code")
df_joined = df_covid.join(df_country, on="location", how="left")

df_transformed = df_joined.withColumn(
    "cases_per_thousand",
    col("total_cases") / col("population") * 1e3
)

(df_transformed
    .repartition(3)
    .write
    .mode("overwrite")
    .partitionBy("continent")
    .parquet(trusted_joined_path)
)
