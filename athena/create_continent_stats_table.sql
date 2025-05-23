CREATE EXTERNAL TABLE IF NOT EXISTS continent_stats (
  continent   string,
  countries   int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/descriptive/continent_stats/'
TBLPROPERTIES ("skip.header.line.count" = "1");