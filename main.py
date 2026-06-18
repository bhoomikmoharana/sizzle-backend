from fastapi import FastAPI

from database import Base, engine
from routers import pantry, recipes, history, auth

app = FastAPI(
    title="Sizzle Backend",
    description="AI-powered cooking recipe generator",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# routers
app.include_router(pantry.router)
app.include_router(recipes.router)
app.include_router(history.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "Sizzle AI Backend"
    }