import os


AWS_REGION_NAME: str = os.environ.get('AWS_CAT_PROJECT_REGION_NAME', None)
S3_SOURCE_BUCKET: str = os.environ.get('S3_SOURCE_BUCKET_CAT', None)
S3_DESTINATION_BUCKET: str = os.environ.get('S3_DESTINATION_BUCKET_CAT', None)
SSM_DATA_ENRICHMENT_IMDB_API_KEY: str = os.environ.get('SSM_DATA_ENRICHMENT_IMDB_API_KEY', None)
SNS_ARN_MOVIE_TOPIC: str = os.environ.get('SNS_ARN_MOVIE_TOPIC', None)
