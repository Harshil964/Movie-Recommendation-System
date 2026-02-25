from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import home, search, tfidf, genre, health
from .services.pickles import load_pickles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    load_pickles()

# Include routers
app.include_router(home.router)
app.include_router(search.router)
app.include_router(tfidf.router)
app.include_router(genre.router)
app.include_router(health.router)
