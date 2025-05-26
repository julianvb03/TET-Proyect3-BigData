import boto3

# Cambia esto al nombre exacto de tu función Lambda
LAMBDA_FUNCTION_NAME = "crearClusterEMR"

def trigger_lambda():
    client = boto3.client("lambda", region_name="us-east-1")
    response = client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType="Event"
    )
    print(f"✅ Lambda invoked. Status code: {response['StatusCode']}")

if __name__ == "__main__":
    trigger_lambda()
