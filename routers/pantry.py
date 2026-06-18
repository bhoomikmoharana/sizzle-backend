from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import PantryItem
from schemas import PantryCreate

router = APIRouter(prefix="/pantry", tags=["Pantry"])


@router.post("")
def add_pantry_item(item: PantryCreate, db: Session = Depends(get_db)):
    new_item = PantryItem(
        user_id=item.user_id,
        ingredient_name=item.ingredient_name
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/{user_id}")
def get_pantry(user_id: int, db: Session = Depends(get_db)):
    items = db.query(PantryItem).filter(PantryItem.user_id == user_id).all()
    return items