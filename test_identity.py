import boto3

sts = boto3.client("sts")

identity = sts.get_caller_identity()

print("=" * 50)
print("Connected to AWS Successfully!")
print("=" * 50)
print(f"Account ID : {identity['Account']}")
print(f"User ARN   : {identity['Arn']}")
print(f"User ID    : {identity['UserId']}")
