from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Recipe
from schemas import RecipeCreate, SuggestRequest
from services.ai_service import generate_recipes

router = APIRouter(tags=["Recipes"])


@router.post("/suggest")
def suggest_recipes(data: SuggestRequest):
    try:
        return generate_recipes(data.ingredients)
    except Exception as e:
        return {
            "error": "AI service error",
            "details": str(e)
        }


@router.post("/recipes/save")
def save_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(**recipe.model_dump())

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


@router.get("/recipes/{user_id}")
def get_saved_recipes(user_id: int, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(Recipe.user_id == user_id).all()
    return recipes