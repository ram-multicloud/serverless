
```json
{
  "action": "start",
  "tag_key": "Environment",
  "tag_value": "dev"
}
```

```py
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    tag_key = event.get('tag_key', 'Schedule')
    tag_value = event.get('tag_value', 'StartStop')
    action = event.get('action')

    response = ec2.describe_instances(
        Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
    )

    results = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']

            if action == 'start' and state == 'stopped':
                ec2.start_instances(InstanceIds=[instance_id])
                results.append(f"Started {instance_id}")

            elif action == 'stop' and state == 'running':
                ec2.stop_instances(InstanceIds=[instance_id])
                results.append(f"Stopped {instance_id}")

            else:
                results.append(f"Instance {instance_id} is already {state}")

    # ✅ Return a structured response
    return {
        "statusCode": 200,
        "body": {
            "action": action,
            "tag_key": tag_key,
            "tag_value": tag_value,
            "results": results
        }

```
    }

```
