import json
from typing import List
from dataclasses import asdict

from ..core.aws_client import AWSS3Client, AWSParameterStore
from . import (
    SSM_DATA_ENRICHMENT_IMDB_API_KEY, S3_DESTINATION_BUCKET, AWS_REGION_NAME
)
from ..exceptions.exceptions import catch_exception
from .utils import get_formatted_movies, get_imbd_api_resmpose, enrich_movie_with_api_data
from ..dataclasses.movies import Movie, EnrichedMovie


TOP10_MOVIES_FILE_NAME = 'Top10Movies.json'
API_ENDPOINT = 'http://www.omdbapi.com'

s3_client = AWSS3Client(service_name='s3', bucket_name=S3_DESTINATION_BUCKET)
ssm_client = AWSParameterStore(service_name='ssm', region_name=AWS_REGION_NAME)
imdb_api_key = ssm_client.get_parameter(parameter_name=SSM_DATA_ENRICHMENT_IMDB_API_KEY, is_secure=True)


@catch_exception
def data_enrichment_lambda_handler(event, context):
    if len(event.get("Records", [])) != 0:
        payload = json.loads(event.get("Records")[0]['body'])
        movies: List[Movie] = get_formatted_movies(payload['items'])
        enriched_movies = enrich_movies(movies)
        s3_client.create_file(
            file_content={'items': [asdict(movie) for movie in enriched_movies]}, file_name=TOP10_MOVIES_FILE_NAME
        )


def enrich_movies(movies: List[Movie]) -> List[EnrichedMovie]:
    enriched_movies: List[EnrichedMovie] = []
    for movie in movies:
        enriched_api_data = get_imbd_api_resmpose(
            api_endpoint=API_ENDPOINT, api_key=imdb_api_key, imdb_id=movie.id
        )
        enriched_movies.append(enrich_movie_with_api_data(movie=movie, enriched_api_data=enriched_api_data))
    return enriched_movies
