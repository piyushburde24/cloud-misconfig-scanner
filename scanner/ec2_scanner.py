from scanner.aws_connector import AWSConnector
from scanner.base_scanner import BaseScanner


class EC2Scanner(BaseScanner):

    def __init__(self):

        super().__init__()

        self.ec2 = AWSConnector().get_client("ec2")

    def scan(self):

        print("\nScanning EC2...\n")

        self.check_security_groups()

        self.check_public_ips()

        return self.findings

    def check_security_groups(self):

        groups = self.ec2.describe_security_groups()[
            "SecurityGroups"
        ]

        for group in groups:

            for permission in group["IpPermissions"]:

                port = permission.get("FromPort")

                for ip in permission.get("IpRanges", []):

                    if ip["CidrIp"] != "0.0.0.0/0":

                        continue

                    if port == 22:

                        self.add_finding(
                            "EC2",
                            group["GroupName"],
                            "Critical",
                            "SSH Open",
                            "Port 22 open to everyone.",
                            "Restrict access."
                        )

                    elif port == 3389:

                        self.add_finding(
                            "EC2",
                            group["GroupName"],
                            "Critical",
                            "RDP Open",
                            "Port 3389 open to everyone.",
                            "Restrict access."
                        )

    def check_public_ips(self):

        reservations = self.ec2.describe_instances()[
            "Reservations"
        ]

        for reservation in reservations:

            for instance in reservation["Instances"]:

                if "PublicIpAddress" in instance:

                    self.add_finding(
                        "EC2",
                        instance["InstanceId"],
                        "Medium",
                        "Public IP Attached",
                        "Instance has a public IP.",
                        "Use a private subnet if possible."
                    )
