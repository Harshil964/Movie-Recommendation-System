from fastapi import APIRouter, Query, HTTPException
from typing import List
from ..models.recs import SearchBundleResponse, TFIDFRecItem
from ..services.tmdb_service import tmdb_search_first, tmdb_movie_details, tmdb_get, tmdb_cards_from_results
from ..services.tfidf_service import tfidf_recommend_titles
from ..services.movie_card_service import attach_tmdb_card_by_title

router = APIRouter()

@router.get("/tmdb/search")
async def tmdb_search(query: str = Query(..., min_length=1), page: int = Query(1, ge=1, le=10)):
    """Return raw TMDB results for search suggestions or grids"""
    return await tmdb_get("/search/movie", {"query": query, "include_adult": "false", "language": "en-US", "page": page})

@router.get("/movie/id/{tmdb_id}")
async def movie_details_route(tmdb_id: int):
    """Return detailed TMDB movie info"""
    return await tmdb_movie_details(tmdb_id)

@router.get("/movie/search", response_model=SearchBundleResponse)
async def search_bundle(
    query: str = Query(..., min_length=1),
    tfidf_top_n: int = Query(12, ge=1, le=30),
    genre_limit: int = Query(12, ge=1, le=30),
):
    """Bundle: movie details + TFIDF + genre recommendations"""
    best = await tmdb_search_first(query)
    if not best:
        raise HTTPException(status_code=404, detail=f"No TMDB movie found for query: {query}")

    tmdb_id = int(best["id"])
    details = await tmdb_movie_details(tmdb_id)

    # 1) TF-IDF recommendations
    tfidf_items: List[TFIDFRecItem] = []
    recs = []
    try:
        recs = tfidf_recommend_titles(details.title, top_n=tfidf_top_n)
    except Exception:
        try:
            recs = tfidf_recommend_titles(query, top_n=tfidf_top_n)
        except Exception:
            recs = []

    for title, score in recs:
        card = await attach_tmdb_card_by_title(title)
        tfidf_items.append(TFIDFRecItem(title=title, score=score, tmdb=card))

    # 2) Genre recommendations (first genre)
    genre_recs: List = []
    if details.genres:
        genre_id = details.genres[0]["id"]
        discover = await tmdb_get("/discover/movie", {"with_genres": genre_id, "language": "en-US", "sort_by": "popularity.desc", "page": 1})
        cards = await tmdb_cards_from_results(discover.get("results", []), limit=genre_limit)
        genre_recs = [c for c in cards if c.tmdb_id != details.tmdb_id]

    return SearchBundleResponse(
        query=query,
        movie_details=details,
        tfidf_recommendations=tfidf_items,
        genre_recommendations=genre_recs
    )