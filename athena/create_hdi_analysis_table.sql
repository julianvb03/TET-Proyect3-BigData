CREATE EXTERNAL TABLE IF NOT EXISTS hdi_analysis (
  hdi_category string,
  countries int,
  avg_cases_per_thousand double,
  avg_deaths_per_million double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/exploratory/hdi_analysis/'
TBLPROPERTIES ("skip.header.line.count" = "1");