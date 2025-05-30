CREATE EXTERNAL TABLE IF NOT EXISTS correlation_analysis (
  continent string,
  hdi_cases_correlation string,
  gdp_cases_correlation string,
  density_cases_correlation string,
  country_count int,
  avg_hdi double,
  avg_gdp double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://YOUR-S3-BUCKET/refined/exploratory/correlation_analysis/'
TBLPROPERTIES ("skip.header.line.count" = "1");