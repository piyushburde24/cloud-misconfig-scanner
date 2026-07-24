from botocore.exceptions import ClientError

from scanner.aws_connector import AWSConnector
from scanner.base_scanner import BaseScanner


class S3Scanner(BaseScanner):

    def __init__(self):
        super().__init__()

        self.s3 = AWSConnector().get_client("s3")

    def scan(self):

        print("\nScanning S3 Buckets...\n")

        buckets = self.s3.list_buckets()["Buckets"]

        if not buckets:
            print("No buckets found.")
            return self.findings

        for bucket in buckets:

            bucket_name = bucket["Name"]

            print(f"Checking {bucket_name}")

            self.check_public(bucket_name)

            self.check_encryption(bucket_name)

            self.check_versioning(bucket_name)

        return self.findings

    def check_public(self, bucket_name):

        try:

            acl = self.s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl["Grants"]:

                grantee = grant.get("Grantee", {})

                uri = grantee.get("URI", "")

                if "AllUsers" in uri:

                    self.add_finding(
                        "S3",
                        bucket_name,
                        "Critical",
                        "Public Bucket",
                        "Bucket is publicly accessible.",
                        "Remove public permissions."
                    )

        except ClientError:
            pass

    def check_encryption(self, bucket_name):

        try:

            self.s3.get_bucket_encryption(Bucket=bucket_name)

        except ClientError:

            self.add_finding(
                "S3",
                bucket_name,
                "High",
                "Encryption Disabled",
                "Server-side encryption is not enabled.",
                "Enable SSE-S3 or SSE-KMS."
            )

    def check_versioning(self, bucket_name):

        try:

            response = self.s3.get_bucket_versioning(
                Bucket=bucket_name
            )

            if response.get("Status") != "Enabled":

                self.add_finding(
                    "S3",
                    bucket_name,
                    "Medium",
                    "Versioning Disabled",
                    "Bucket versioning is disabled.",
                    "Enable versioning."
                )

        except ClientError:
            pass
