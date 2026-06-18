from pydantic import BaseModel


class PantryCreate(BaseModel):
    user_id: int
    ingredient_name: str


class SuggestRequest(BaseModel):
    user_id: int
    ingredients: list[str]


class RecipeCreate(BaseModel):
    user_id: int
    title: str
    ingredients_used: str
    extra_ingredients: str
    steps: str
    cook_time: str
    difficulty: str
    
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str