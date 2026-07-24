from datetime import datetime, timezone

from botocore.exceptions import ClientError

from scanner.aws_connector import AWSConnector
from scanner.base_scanner import BaseScanner


class IAMScanner(BaseScanner):
    """
    Scans IAM users for common security issues.
    """

    def __init__(self):
        super().__init__()
        self.iam = AWSConnector().get_client("iam")

    def scan(self):
        print("\nScanning IAM...\n")

        users = self.iam.list_users()["Users"]

        for user in users:
            username = user["UserName"]

            print(f"Checking user: {username}")

            self.check_mfa(username)
            self.check_access_keys(username)
            self.check_admin_policy(username)

        return self.findings

    def check_mfa(self, username):
        """
        Check whether MFA is enabled.
        """
        try:
            devices = self.iam.list_mfa_devices(
                UserName=username
            )["MFADevices"]

            if not devices:
                self.add_finding(
                    "IAM",
                    username,
                    "High",
                    "MFA Disabled",
                    "User does not have MFA enabled.",
                    "Enable MFA from the AWS IAM Console."
                )

        except ClientError:
            pass

    def check_access_keys(self, username):
        """
        Check access key age.
        """
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
                        "Rotate the access key."
                    )

        except ClientError:
            pass

    def check_admin_policy(self, username):
        """
        Detect AdministratorAccess policy.
        """
        try:
            policies = self.iam.list_attached_user_policies(
                UserName=username
            )["AttachedPolicies"]

            for policy in policies:
                if policy["PolicyName"] == "AdministratorAccess":
                    self.add_finding(
                        "IAM",
                        username,
                        "Critical",
                        "Administrator Access",
                        "User has AdministratorAccess policy attached.",
                        "Apply the principle of least privilege."
                    )

        except ClientError:
            pass
