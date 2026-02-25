import httpx
from fastapi import HTTPException
from typing import Dict, Any, List, Optional
from ..config import TMDB_API_KEY
from ..utils.helpers import make_img_url
from ..models.tmdb import TMDBMovieCard, TMDBMovieDetails

async def tmdb_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    q = dict(params)
    q["api_key"] = TMDB_API_KEY

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(f"https://api.themoviedb.org/3{path}", params=q)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"TMDB request error: {type(e).__name__} | {repr(e)}")

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"TMDB error {r.status_code}: {r.text}")

    return r.json()

async def tmdb_cards_from_results(results: List[dict], limit: int = 20) -> List[TMDBMovieCard]:
    out = []
    for m in (results or [])[:limit]:
        out.append(TMDBMovieCard(
            tmdb_id=int(m["id"]),
            title=m.get("title") or m.get("name") or "",
            poster_url=make_img_url(m.get("poster_path")),
            release_date=m.get("release_date"),
            vote_average=m.get("vote_average"),
        ))
    return out

async def tmdb_movie_details(movie_id: int) -> TMDBMovieDetails:
    data = await tmdb_get(f"/movie/{movie_id}", {"language": "en-US"})
    return TMDBMovieDetails(
        tmdb_id=int(data["id"]),
        title=data.get("title") or "",
        overview=data.get("overview"),
        release_date=data.get("release_date"),
        poster_url=make_img_url(data.get("poster_path")),
        backdrop_url=make_img_url(data.get("backdrop_path")),
        genres=data.get("genres", []) or [],
    )

async def tmdb_search_movies(query: str, page: int = 1) -> Dict[str, Any]:
    return await tmdb_get("/search/movie", {"query": query, "include_adult": "false", "language": "en-US", "page": page})

async def tmdb_search_first(query: str) -> Optional[dict]:
    data = await tmdb_search_movies(query, page=1)
    results = data.get("results", [])
    return results[0] if results else None