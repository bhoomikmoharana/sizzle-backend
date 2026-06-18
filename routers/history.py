from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import History

router = APIRouter(tags=["History"])


@router.post("/recipes/{recipe_id}/use")
def use_recipe(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    history = History(
        user_id=user_id,
        recipe_id=recipe_id
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "message": "Recipe added to history",
        "history": history
    }


@router.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(
        History.user_id == user_id
    ).all()

    return history