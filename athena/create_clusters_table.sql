CREATE EXTERNAL TABLE IF NOT EXISTS clusters (
  location string,
  continent string,
  cluster int,
  human_development_index double,
  gdp_per_capita double,
  cases_per_thousand double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/advanced/clusters/'
TBLPROPERTIES ("skip.header.line.count" = "1");