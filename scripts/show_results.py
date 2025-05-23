import json
import boto3

athena = boto3.client('athena')
DB_NAME = "covid_analytics"
BUCKET_NAME = "st0263-proyecto3"  # Replace with your S3 bucket name
OUTPUT_S3 = f"s3://{BUCKET_NAME}/athena_results/"

VALID_TABLES = {
    'continent_stats',
    'numeric_summary',
    'top_countries',
    'correlation_analysis',
    'hdi_analysis',
    'clusters',
    'cluster_summary'
}

def lambda_handler(event, context):
    """
    Lambda function to query Athena and return results.
    """
    
    try:
        body = json.loads(event.get('body') or "{}")
        table = body.get('table')
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Payload mal formado, JSON inválido'})
        }

    if not table and event.get('table'):
        table = event['table']
    print(f"table: {table}")

    if table not in VALID_TABLES:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Tabla inválida',
                'valid_tables': sorted(VALID_TABLES)
            })
        }

    sql = f"SELECT * FROM {DB_NAME}.{table} LIMIT 1000"
    resp = athena.start_query_execution(
        QueryString         = sql,
        QueryExecutionContext={'Database': DB_NAME},
        ResultConfiguration = {'OutputLocation': OUTPUT_S3}
    )
    qid = resp['QueryExecutionId']

    # Wait for the query to finish
    state = 'RUNNING'
    while state in ('QUEUED','RUNNING'):
        meta = athena.get_query_execution(QueryExecutionId=qid)
        state = meta['QueryExecution']['Status']['State']

    if state != 'SUCCEEDED':
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Consulta fallida', 'state': state})
        }

    rows = athena.get_query_results(QueryExecutionId=qid)['ResultSet']['Rows']
    headers = [c['VarCharValue'] for c in rows[0]['Data']]
    data = []
    for r in rows[1:]:
        values = [c.get('VarCharValue') for c in r['Data']]
        data.append(dict(zip(headers, values)))

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }
