import json

def lambda_handler(event, context):
    # Print to CloudWatch Logs
    print("Hello from AWS Lambda!")

    return {
        "statusCode": 200,
        "body": json.dumps("Message logged successfully")
    }
