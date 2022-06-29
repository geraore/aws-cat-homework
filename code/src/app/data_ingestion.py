from typing import List
from dataclasses import asdict
import json

from .utils import get_formatted_movies
from ..core.aws_client import AWSS3Client, AWSSNSClient
from . import SNS_ARN_MOVIE_TOPIC, S3_SOURCE_BUCKET, AWS_REGION_NAME
from ..exceptions.exceptions import catch_exception
from ..dataclasses.movies import Movie


TOP250_MOVIES_FILE_NAME = 'Top250Movies.json'

s3_client = AWSS3Client(service_name='s3', bucket_name=S3_SOURCE_BUCKET)
sns_client = AWSSNSClient(service_name='sns', region_name=AWS_REGION_NAME, sns_arn=SNS_ARN_MOVIE_TOPIC)


@catch_exception
def data_ingestion_lambda_handler(event, context):
    top_250_movies = json.loads(s3_client.get_file(file_name=TOP250_MOVIES_FILE_NAME))
    movies: List[Movie] = get_formatted_movies(top_250_movies['items'])
    top_tem_movies = sorted(movies, reverse=True)[0:10]
    sns_client.publish(message={'items': [asdict(movie) for movie in top_tem_movies]})


