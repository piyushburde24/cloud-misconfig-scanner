"""
EC2 Security Scanner

Checks:
1. SSH open to the Internet
2. RDP open to the Internet
3. Public IP addresses
"""

from botocore.exceptions import ClientError

from scanner.aws_connector import AWSConnector
from scanner.base_scanner import BaseScanner


class EC2Scanner(BaseScanner):

    def __init__(self):
        super().__init__()
        self.ec2 = AWSConnector().get_client("ec2")

    def scan(self):
        """
        Run all EC2 security checks.
        """
        print("\nScanning EC2...\n")

        self.check_security_groups()
        self.check_public_ips()

        return self.findings

    def check_security_groups(self):
        """
        Detect SSH/RDP open to the world.
        """
        try:
            response = self.ec2.describe_security_groups()

            for group in response["SecurityGroups"]:

                group_name = group["GroupName"]

                print(f"Checking Security Group: {group_name}")

                for permission in group.get("IpPermissions", []):

                    from_port = permission.get("FromPort")
                    to_port = permission.get("ToPort")

                    for ip_range in permission.get("IpRanges", []):

                        cidr = ip_range.get("CidrIp")

                        if cidr != "0.0.0.0/0":
                            continue

                        if from_port == 22 and to_port == 22:
                            self.add_finding(
                                "EC2",
                                group_name,
                                "Critical",
                                "SSH Open to the Internet",
                                "Security Group allows SSH (22) from 0.0.0.0/0.",
                                "Restrict SSH access to trusted IP addresses."
                            )

                        elif from_port == 3389 and to_port == 3389:
                            self.add_finding(
                                "EC2",
                                group_name,
                                "Critical",
                                "RDP Open to the Internet",
                                "Security Group allows RDP (3389) from 0.0.0.0/0.",
                                "Restrict RDP access to trusted IP addresses."
                            )

        except ClientError as e:
            print(f"EC2 Error: {e}")

    def check_public_ips(self):
        """
        Detect EC2 instances with public IP addresses.
        """
        try:
            response = self.ec2.describe_instances()

            for reservation in response["Reservations"]:

                for instance in reservation["Instances"]:

                    if "PublicIpAddress" in instance:

                        self.add_finding(
                            "EC2",
                            instance["InstanceId"],
                            "Medium",
                            "Public IP Attached",
                            f"Instance has public IP {instance['PublicIpAddress']}.",
                            "Use private subnets when possible."
                        )

        except ClientError as e:
            print(f"EC2 Error: {e}")
