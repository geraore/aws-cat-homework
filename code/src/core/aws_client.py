from typing import Optional, Dict
from functools import lru_cache
from boto3 import client
import json

from ..exceptions.custom_exceptions import BadRegionError, NoServiceTypeError, NoBucketName
from . import AWS_NO_REGION_SERVICES_NAME


class AWSClient:
    def __init__(self, service_name: str, region_name: Optional[str] = None):
        self.service_name = service_name
        self.region_name = region_name
        self.__check_region_and_service_correctness()
        self.__set_client()

    def __check_region_and_service_correctness(self):
        if not self.service_name:
            raise NoServiceTypeError
        elif self.region_name and self.service_name in AWS_NO_REGION_SERVICES_NAME:
            raise BadRegionError(
                service_type=self.service_name,
                message=f'Service {self.service_name}'
            )
        elif not self.region_name and self.service_name not in AWS_NO_REGION_SERVICES_NAME:
            raise BadRegionError(
                service_type=self.service_name,
                message=f'Service {self.service_name}'
            )

    def __set_client(self):
        if self.service_name not in AWS_NO_REGION_SERVICES_NAME:
            self._client = client(
                service_name=self.service_name, region_name=self.region_name
            )
        else:
            self._client = client(
                service_name=self.service_name
            )


class AWSS3Client(AWSClient):

    def __init__(self, service_name: str, bucket_name: str):
        super().__init__(service_name)
        if not bucket_name:
            raise NoBucketName('Bucket not set in the AWS S3 client')
        self.__bucket_name = bucket_name

    def get_file(self, file_name: str) -> str:
        s3_object = self._client.get_object(Bucket=self.__bucket_name, Key=file_name)
        return s3_object['Body'].read().decode('utf-8') if 'Body' in s3_object else {}

    def create_file(self, file_content: Dict, file_name: str):
        self._client.put_object(
            Body=json.dumps(file_content).encode(),
            Bucket=self.__bucket_name,
            Key=file_name
        )


class AWSParameterStore(AWSClient):

    def __init__(self, service_name: str, region_name: str):
        super().__init__(service_name, region_name)

    @lru_cache
    def get_parameter(self, parameter_name: str, is_secure: bool = False) -> str:
        response = self._client.get_parameter(
            Name=parameter_name, WithDecryption=is_secure
        )
        return response['Parameter']['Value'] if response['Parameter'] else ""


class AWSSNSClient(AWSClient):

    def __init__(self, service_name: str, region_name: str, sns_arn: str, number_of_workers: int = 1):
        super().__init__(service_name, region_name)
        self.__sns_arn = sns_arn
        self.__parallel_workers = number_of_workers

    def publish(self, message: dict) -> Optional[dict]:
        response: dict = self._client.publish(
            TargetArn=self.__sns_arn,
            Message=json.dumps({
                'default': json.dumps(message, indent=4, sort_keys=True, default=str)
            }),
            MessageStructure='json'
        )
        return response or None
