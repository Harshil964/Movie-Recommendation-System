from fastapi import APIRouter, Query, HTTPException
from typing import List
from ..services.tfidf_service import tfidf_recommend_titles

router = APIRouter()

@router.get("/recommend/tfidf")
async def recommend_tfidf(title: str = Query(..., min_length=1), top_n: int = Query(10, ge=1, le=50)):
    """Return local TF-IDF recommendations for a title"""
    recs = tfidf_recommend_titles(title, top_n=top_n)
    return [{"title": t, "score": s} for t, s in recs]