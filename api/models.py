from pydantic import BaseModel, Field
from typing import Literal

Day = Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MealType = Literal["Breakfast", "Lunch", "Dinner", "Snack"]


class EntryIn(BaseModel):
    planId: int
    recipeId: int
    day: Day
    mealType: MealType
    servings: int = Field(ge=1)


class EntryUpdate(BaseModel):
    day: Day
    mealType: MealType
    servings: int = Field(ge=1)
    
class Ingredient(BaseModel):
    name: str
    measure: str = ""

#recipe class
class RecipeIn(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    category: str = Field(min_length=1)
    area: str = ""
    prepTime: int = Field(ge=0)
    calories: int = Field(ge=0)
    servings: int = Field(ge=1)
    ingredients: list[Ingredient] = []
    instructions: str = ""
    imageUrl: str = ""

class PlanIn(BaseModel):
    name: str = Field(min_length=1)
    startDate: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    notes: str = ""
    status: Literal["Active", "Archived"] = "Active"