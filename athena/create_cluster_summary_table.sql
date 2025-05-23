CREATE EXTERNAL TABLE IF NOT EXISTS cluster_summary (
  cluster int,
  countries int,
  avg_hdi double,
  avg_gdp double,
  avg_density double,
  avg_cases_per_thousand double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/advanced/cluster_summary/'
TBLPROPERTIES ("skip.header.line.count" = "1");