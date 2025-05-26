CREATE EXTERNAL TABLE IF NOT EXISTS top_countries (
  location string,
  continent string,
  total_cases string,
  population bigint,
  cases_per_thousand double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/exploratory/top_countries/'
TBLPROPERTIES ("skip.header.line.count" = "1");