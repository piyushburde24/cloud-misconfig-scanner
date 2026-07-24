"""
Scanner Manager

Runs all enabled scanners and combines their findings.
"""

from scanner.s3_scanner import S3Scanner
from scanner.iam_scanner import IAMScanner
from scanner.ec2_scanner import EC2Scanner


class ScannerManager:

    def __init__(self):
        self.scanners = [
            S3Scanner(),
            IAMScanner(),
            EC2Scanner(),
        ]

    def run(self):

        findings = []

        for scanner in self.scanners:

            findings.extend(scanner.scan())

        return findings
