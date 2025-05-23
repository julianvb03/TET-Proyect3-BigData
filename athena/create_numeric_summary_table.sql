CREATE EXTERNAL TABLE IF NOT EXISTS numeric_summary (
  total_records int,
  avg_total_cases double,
  max_total_cases bigint,
  avg_total_deaths double,
  max_total_deaths bigint,
  avg_population double,
  max_population bigint,
  avg_cases_per_thousand double,
  max_cases_per_thousand double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/descriptive/numeric_summary/'
TBLPROPERTIES ("skip.header.line.count" = "1");