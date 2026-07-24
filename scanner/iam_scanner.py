from datetime import datetime, timezone

from botocore.exceptions import ClientError

from scanner.aws_connector import AWSConnector
from scanner.base_scanner import BaseScanner


class IAMScanner(BaseScanner):

    def __init__(self):

        super().__init__()

        self.iam = AWSConnector().get_client("iam")

    def scan(self):

        print("\nScanning IAM...\n")

        users = self.iam.list_users()["Users"]

        for user in users:

            username = user["UserName"]

            self.check_mfa(username)

            self.check_access_keys(username)

        return self.findings

    def check_mfa(self, username):

        devices = self.iam.list_mfa_devices(
            UserName=username
        )["MFADevices"]

        if len(devices) == 0:

            self.add_finding(
                "IAM",
                username,
                "High",
                "MFA Disabled",
                "User has no MFA device.",
                "Enable MFA."
            )

    def check_access_keys(self, username):

        try:

            keys = self.iam.list_access_keys(
                UserName=username
            )["AccessKeyMetadata"]

            for key in keys:

                age = (
                    datetime.now(timezone.utc)
                    - key["CreateDate"]
                ).days

                if age > 90:

                    self.add_finding(
                        "IAM",
                        username,
                        "Medium",
                        "Old Access Key",
                        f"Access key is {age} days old.",
                        "Rotate the key."
                    )

        except ClientError:

            pass
