from typing import List, Dict, Optional
import requests
import logging

from ..dataclasses.movies import Movie, EnrichedMovie, Rating

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_formatted_movies(movies: List[Movie]):
    return [
        Movie(
            id=movie.get('id'), rank=int(movie.get('rank')) if movie.get('rank') else 0, title=movie.get('title'),
            fullTitle=movie.get('fullTitle'), year=int(movie.get('year')) if movie.get('year') else None,
            image=movie.get('image'), crew=movie.get('crew'), imDbRating=float(movie.get('imDbRating')),
            imDbRatingCount=movie.get('imDbRatingCount')
        ) for movie in movies
    ]


def get_imbd_api_resmpose(api_endpoint: str, api_key: str, imdb_id: str):
    url = f'{api_endpoint}/?i={imdb_id}&apikey={api_key}'
    response = requests.get(url=url)
    if 200 <= response.status_code <= 299:
        return response.json()
    else:
        logger.info(response)


def enrich_movie_with_api_data(movie: Movie, enriched_api_data: Optional[Dict]) -> EnrichedMovie:
    enriched_movie = EnrichedMovie(
        id=movie.id, rank=movie.rank, title=movie.title, fullTitle=movie.fullTitle, year=movie.year,
        image=movie.image, crew=movie.crew, imDbRating=movie.imDbRating, imDbRatingCount=movie.imDbRatingCount
    )
    if enriched_api_data:
        enriched_movie.rated = enriched_api_data.get('Rated')
        enriched_movie.released = enriched_api_data.get('Released')
        enriched_movie.runtime = enriched_api_data.get('Runtime')
        enriched_movie.genre = enriched_api_data.get('Genre')
        enriched_movie.director = enriched_api_data.get('Director')
        enriched_movie.writer = enriched_api_data.get('Writer')
        enriched_movie.actors = enriched_api_data.get('Actors')
        enriched_movie.plot = enriched_api_data.get('Plot')
        enriched_movie.language = enriched_api_data.get('Language')
        enriched_movie.country = enriched_api_data.get('Country')
        enriched_movie.awards = enriched_api_data.get('Awards')
        enriched_movie.poster = enriched_api_data.get('Poster')
        enriched_movie.ratings = get_enriched_ratings(enriched_api_data.get('Ratings'))
        enriched_movie.meta_score = enriched_api_data.get('Metascore')
        enriched_movie.imdb_rating = enriched_api_data.get('imdbRating')
        enriched_movie.imdb_votes = enriched_api_data.get('imdbVotes')
        enriched_movie.type = enriched_api_data.get('Type')
        enriched_movie.dvd = enriched_api_data.get('DVD')
        enriched_movie.box_office = enriched_api_data.get('BoxOffice')
        enriched_movie.production = enriched_api_data.get('Production')
        enriched_movie.website = enriched_api_data.get('Website')
        enriched_movie.response = enriched_api_data.get('Response')
    return enriched_movie


def get_enriched_ratings(ratings: Optional[List]) -> List:
    return [Rating(Source=rating.get('Source'), Value=rating.get('Value')) for rating in ratings]
