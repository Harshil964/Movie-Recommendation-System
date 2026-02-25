from typing import Optional
from ..config import TMDB_IMG_500

def _norm_title(title: str) -> str:
    return str(title).strip().lower()

def make_img_url(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    return f"{TMDB_IMG_500}{path}"