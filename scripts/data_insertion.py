import pandas as pd
from datetime import datetime
from io import StringIO
import boto3

s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

BUCKET_NAME = 'st0263-proyecto3'  # Replace with your S3 bucket name
COVID_RAW_PREFIX = 'raw/'
EMR_LAMBDA_NAME = 'crearClusterEMR'  # Replace with your EMR Lambda function name

def lambda_handler(event, context):
    """
    Lambda AWS function to load a CSV file from a URL into an S3 bucket, load a csv from a Relational Database and trigger an EMR cluster creation.
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # --- CSV desde URL ---
    try:
        covid_url = "https://raw.githubusercontent.com/julianvb03/TET-Proyect3-BigData/refs/heads/main/data/covid_data.csv"
        df = pd.read_csv(covid_url)

        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        covid_key = f'{COVID_RAW_PREFIX}covid_data.csv'
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=covid_key,
            Body=csv_buffer.getvalue()
        )

        lambda_client.invoke(
            FunctionName=EMR_LAMBDA_NAME,
            InvocationType='Event'
        )
        return {'status': True, 'message': 'CSV cargado correctamente'}
    except Exception as e:
        return {'status': False, 'error': str(e)}