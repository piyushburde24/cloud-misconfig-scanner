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

            print(f"Checking bucket: {bucket_name}")

            # Security Checks
            self.check_public(bucket_name)
            self.check_public_access_block(bucket_name)
            self.check_encryption(bucket_name)
            self.check_versioning(bucket_name)

        return self.findings

    def check_public(self, bucket_name):
        """
        Detect public buckets using both ACLs and Bucket Policies.
        """

        # ----------------------------------------
        # Check Bucket ACL
        # ----------------------------------------

        try:

            acl = self.s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl["Grants"]:

                grantee = grant.get("Grantee", {})

                uri = grantee.get("URI", "")

                if (
                    "AllUsers" in uri
                    or "AuthenticatedUsers" in uri
                ):

                    self.add_finding(
                        "S3",
                        bucket_name,
                        "Critical",
                        "Public Bucket (ACL)",
                        "Bucket is publicly accessible through its ACL.",
                        "Remove public ACL permissions."
                    )

                    return

        except ClientError:
            pass

        # ----------------------------------------
        # Check Bucket Policy
        # ----------------------------------------

        try:

            response = self.s3.get_bucket_policy_status(
                Bucket=bucket_name
            )

            if response["PolicyStatus"]["IsPublic"]:

                self.add_finding(
                    "S3",
                    bucket_name,
                    "Critical",
                    "Public Bucket (Policy)",
                    "Bucket is publicly accessible through its bucket policy.",
                    "Remove public access from the bucket policy."
                )

        except ClientError:
            pass

    def check_public_access_block(self, bucket_name):
        """
        Check whether Block Public Access is disabled.
        """

        try:

            response = self.s3.get_public_access_block(
                Bucket=bucket_name
            )

            config = response["PublicAccessBlockConfiguration"]

            if not all(config.values()):

                self.add_finding(
                    "S3",
                    bucket_name,
                    "Medium",
                    "Public Access Block Disabled",
                    "One or more Block Public Access settings are disabled.",
                    "Enable all Block Public Access settings."
                )

        except ClientError:
            pass

    def check_encryption(self, bucket_name):
        """
        Check if server-side encryption is enabled.
        """

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
        """
        Check if bucket versioning is enabled.
        """

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
                    "Enable bucket versioning."
                )

        except ClientError:
            pass
