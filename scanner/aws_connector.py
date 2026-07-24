"""
AWS Connector
"""

import boto3
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
)

from config.config import Config


class AWSConnector:
    def __init__(self):
        self.region = Config.AWS_REGION

    def get_client(self, service_name: str):
        try:
            return boto3.client(
                service_name,
                region_name=self.region
            )

        except NoCredentialsError:
            raise RuntimeError("AWS credentials not found.")

        except PartialCredentialsError:
            raise RuntimeError("Incomplete AWS credentials.")

        except ClientError as e:
            raise RuntimeError(str(e))
