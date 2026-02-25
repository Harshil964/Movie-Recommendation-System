from fastapi import APIRouter, Query, HTTPException
from typing import List
from ..models.tmdb import TMDBMovieCard
from ..services.tmdb_service import tmdb_get, tmdb_cards_from_results

router = APIRouter()

@router.get("/home", response_model=List[TMDBMovieCard])
async def home(category: str = Query("popular"), limit: int = Query(24, ge=1, le=50)):
    try:
        if category == "trending":
            data = await tmdb_get("/trending/movie/day", {"language": "en-US"})
            return await tmdb_cards_from_results(data.get("results", []), limit=limit)
        if category not in {"popular", "top_rated", "upcoming", "now_playing"}:
            raise HTTPException(status_code=400, detail="Invalid category")
        data = await tmdb_get(f"/movie/{category}", {"language": "en-US", "page": 1})
        return await tmdb_cards_from_results(data.get("results", []), limit=limit)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Home route failed: {e}")