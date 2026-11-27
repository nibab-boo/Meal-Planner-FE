from collections import Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import RecipeIn, PlanIn,EntryIn,EntryUpdate
import data

app = FastAPI(title = "Meal Planner API")

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

# Shown on /docs, so readers see which errors each route can return
NOT_FOUND = {404: {"description": "Not found"}}
ENTRY_ERRORS = {404: {"description": "Plan, recipe or entry not found"},
                409: {"description": "Same recipe already in this plan, day and meal slot"}}
def found_or_404(item, doc: str):
    if item is None:
        raise HTTPException(status_code=404,detail= f"{doc} not found" )
    return item


#-------------------------Recipes--------------------------------------
@app.get("/recipes")
def list_recipes():
    return data.load("recipes")
    


@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    return found_or_404(data.get_one("recipes",recipe_id),"Recipe")

@app.post("/recipes")
def create_recipe(body: RecipeIn):
    return data.create("recipes", body.model_dump())


@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id:int,body: RecipeIn):
    old_item = data.update("recipes",recipe_id, body.model_dump())
    return found_or_404(old_item,"recipe")

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    if not data.delete_recipe(recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")


#-------------------------Plans--------------------------------------
@app.get("/plans")
def list_plan():
    return data.load("plans")


@app.get("/plans/{plan_id}")
def get_plan(plan_id: int):
    return found_or_404(data.get_one("plans", plan_id),"plan")

@app.post("/plans",status_code=201)
def create_plan(body: PlanIn):
    return data.create("plans",body.model_dump() )


@app.put("/plans/{plan_id}")
def update_plan(plan_id:int,body:PlanIn):
    return found_or_404(data.update("plans",plan_id,body.model_dump()),"Plan")

@app.delete("/plans/{plan_id}",status_code=204)
def delete_plan(plan_id:int):
    if not data.delete_plan(plan_id):
        raise HTTPException(status_code=404, detail="Plan not found")


#-------------------------Entries--------------------------------------
@app.get("/entries")
def list_entries():
    return data.load("plan_entries")


@app.get("/plans/{plan_id}/entries")
def get_plan_entries(plan_id: int):
    found_or_404(data.get_one("plans", plan_id), "Plan")
    return data.entries_for("planId", plan_id)

@app.get("/recipes/{recipe_id}/entries")
def get_recipe_entries(recipe_id: int):
    found_or_404(data.get_one("recipes", recipe_id), "Recipe")
    return data.entries_for("recipeId", recipe_id)

@app.post("/entries", status_code=201)
def create_entry(body: EntryIn):
    # Rule 1, referential integrity: both must exist
    found_or_404(data.get_one("plans", body.planId), "Plan")
    found_or_404(data.get_one("recipes", body.recipeId), "Recipe")

    # Rule 2, no duplicates
    if data.is_duplicate(body.planId, body.recipeId, body.day, body.mealType):
        raise HTTPException(
            status_code=409,
            detail=f"This recipe is already in that plan on {body.day} {body.mealType}.",
        )

    return data.create("plan_entries", body.model_dump())


@app.put("/entries/{entry_id}")
def update_entry(entry_id: int, body: EntryUpdate):
    # 1. The entry must exist. Keep it, because we need its planId and recipeId.
    entry = found_or_404(data.get_one("plan_entries", entry_id), "Entry")

    # 2. Integrity: the plan or recipe might have been deleted in the meantime
    found_or_404(data.get_one("plans", entry["planId"]), "Plan")
    found_or_404(data.get_one("recipes", entry["recipeId"]), "Recipe")

    # 3. No duplicates: OLD plan + recipe, NEW day + slot, and ignore this entry itself
    if data.is_duplicate(entry["planId"], entry["recipeId"], body.day, body.mealType,
                         ignore_id=entry_id):
        raise HTTPException(
            status_code=409,
            detail=f"That recipe is already in this plan on {body.day} {body.mealType}.",
        )

    return data.update("plan_entries", entry_id, body.model_dump())


@app.delete("/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int):
    if not data.delete("plan_entries", entry_id):
        raise HTTPException(status_code=404, detail="Entry not found")

    #-------------------------Dashboard--------------------------------------
@app.get("/stats")
def stats():
    recipes = data.load("recipes")
    plans = data.load("plans")
    entries = data.load("plan_entries")

    recent = sorted(recipes, key=lambda r: r["id"], reverse=True)[:5]
    titles = {r["id"]: r["title"] for r in recipes}

    use_counts = Counter(e["recipeId"] for e in entries if e["recipeId"] in titles)
    most_used = [{"id": rid, "title": titles[rid], "count": n}
                 for rid, n in use_counts.most_common(5)]

    categories = Counter(r["category"] for r in recipes)
    return {
    "totalRecipes": len(recipes),
    "totalPlans": len(plans),
    "totalEntries": len(entries),
    "activePlans": sum(1 for p in plans if p["status"] == "Active"),
    "recentRecipes": [
        {"id": r["id"], "title": r["title"], "category": r["category"],
            "prepTime": r["prepTime"], "calories": r["calories"]}
        for r in recent
    ],
    "mostUsed": most_used,
    "categoryBreakdown": [{"category": c, "count": n}
                            for c, n in categories.most_common()],
    }    