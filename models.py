from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


class PantryItem(Base):
    __tablename__ = "pantry_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    ingredient_name = Column(String)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String)
    ingredients_used = Column(Text)
    extra_ingredients = Column(Text)
    steps = Column(Text)
    cook_time = Column(String)
    difficulty = Column(String)


class History(Base):
    __tablename__ = "recipe_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)