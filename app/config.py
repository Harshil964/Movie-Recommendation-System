import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY missing. Put it in .env")

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_500 = "https://image.tmdb.org/t/p/w500"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DF_PATH = os.path.join(BASE_DIR, "../data/df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "../data/indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "../data/tfidf_matrix.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "../data/tfidf.pkl")