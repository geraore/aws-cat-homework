from datetime import date
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass(order=True)
class Movie:
    sort_index: int = field(init=False, repr=False)
    id: Optional[str] = None
    rank: Optional[int] = None
    title: Optional[str] = None
    fullTitle: Optional[str] = None
    year: Optional[int] = None
    image: Optional[str] = None
    crew: Optional[str] = None
    imDbRating: Optional[float] = None
    imDbRatingCount: Optional[str] = None

    def __post_init__(self):
        self.sort_index = self.imDbRating


@dataclass
class Rating:
    Source: str
    Value: str


@dataclass
class EnrichedMovie(Movie):
    rated: Optional[str] = None
    released: Optional[str] = None
    runtime: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    writer: Optional[str] = None
    actors: Optional[str] = None
    plot: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    awards: Optional[str] = None
    poster: Optional[str] = None
    ratings: Optional[List[Rating]] = None
    meta_score: Optional[int] = None
    imdb_rating: Optional[float] = None
    imdb_votes: Optional[int] = None
    type: Optional[str] = None
    dvd: Optional[date] = None
    box_office: Optional[str] = None
    production: Optional[str] = None
    website: Optional[str] = None
    response: Optional[bool] = None
