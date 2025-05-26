import boto3
import psycopg2
import requests
import pandas as pd
from io import StringIO

BUCKET_NAME = "st0263-proyecto3"
GITHUB_CSV_URL = "https://raw.githubusercontent.com/julianvb03/TET-Proyect3-BigData/refs/heads/main/data/covid_data.csv"
GLUE_WORKFLOW_NAME = "run_ETL"

def lambda_handler(event, context):
    response = requests.get(GITHUB_CSV_URL)
    if response.status_code == 200:
        s3 = boto3.client("s3")
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key="raw/covid_data.csv",
            Body=response.content
        )
        print("✅ Archivo de GitHub subido correctamente a S3.")
    else:
        raise Exception("❌ Error al descargar el archivo desde GitHub.")

    conn = psycopg2.connect(
        host="database-p3.cr7nhi9bkmhs.us-east-1.rds.amazonaws.com",
        port=5432,
        database="postgres",
        user="postgres",
        password="admin123"
    )
    query = "SELECT * FROM country_data"
    df = pd.read_sql(query, conn)
    conn.close()

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="raw/country_data.csv",
        Body=csv_buffer.getvalue()
    )
    print("✅ Archivo desde PostgreSQL subido correctamente a S3.")
    
    glue = boto3.client('glue')
    response = glue.start_workflow_run(Name=GLUE_WORKFLOW_NAME)
    print(f"🚀 Workflow iniciado: runId = {response['RunId']}")

    return {"status": "success"}
