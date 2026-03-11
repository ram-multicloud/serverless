import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all running instances
    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = instance.get('Tags', [])

            # Check if Environment=dev tag exists
            has_dev_tag = any(tag['Key'] == 'Environment' and tag['Value'].lower() == 'dev'
                              for tag in tags)

            if not has_dev_tag:
                print(f"Stopping instance {instance_id} (no Environment=dev tag)")
                ec2.stop_instances(InstanceIds=[instance_id])
