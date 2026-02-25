from fastapi import APIRouter, Query
from typing import List
from ..models.tmdb import TMDBMovieCard
from ..services.tmdb_service import tmdb_movie_details, tmdb_get, tmdb_cards_from_results

router = APIRouter()

@router.get("/recommend/genre", response_model=List[TMDBMovieCard])
async def recommend_genre(tmdb_id: int = Query(...), limit: int = Query(18, ge=1, le=50)):
    """Return popular movies from the first genre of the given TMDB movie"""
    details = await tmdb_movie_details(tmdb_id)
    if not details.genres:
        return []

    genre_id = details.genres[0]["id"]
    discover = await tmdb_get("/discover/movie", {"with_genres": genre_id, "language": "en-US", "sort_by": "popularity.desc", "page": 1})
    cards = await tmdb_cards_from_results(discover.get("results", []), limit=limit)
    return [c for c in cards if c.tmdb_id != details.tmdb_id]