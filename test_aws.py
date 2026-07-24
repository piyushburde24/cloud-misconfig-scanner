from scanner.aws_connector import AWSConnector

connector = AWSConnector()

s3 = connector.get_client("s3")

print("Connected successfully!")

response = s3.list_buckets()

print(response)
