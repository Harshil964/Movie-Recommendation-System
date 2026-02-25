import pickle
from .tfidf_service import df, tfidf_matrix, TITLE_TO_IDX
from ..config import DF_PATH, INDICES_PATH, TFIDF_MATRIX_PATH, TFIDF_PATH
from .tfidf_service import build_title_to_idx_map

def load_pickles():
    global df, tfidf_matrix, TITLE_TO_IDX

    with open(DF_PATH, "rb") as f:
        df_obj = pickle.load(f)
    with open(INDICES_PATH, "rb") as f:
        indices_obj = pickle.load(f)
    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix_obj = pickle.load(f)
    # optional: vectorizer
    with open(TFIDF_PATH, "rb") as f:
        _ = pickle.load(f)

    df = df_obj
    tfidf_matrix = tfidf_matrix_obj
    TITLE_TO_IDX = build_title_to_idx_map(indices_obj)