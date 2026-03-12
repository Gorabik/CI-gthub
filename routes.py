import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from database import engine, Base, get_db
from models import Recipe
from scheme import (
    RecipeDetail,
    RecipeCreated,
    RecipeCreate, RecipeListItem
)


@asynccontextmanager
async def lifespan():
    """Создает таблицы при старте."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database created")
    yield
    await engine.dispose()
    print("Connection closed")


app = FastAPI(
    title="Recipe Service API",
    description="API for recipes cooking ",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/recipes", response_model=list[RecipeListItem],
    summary="Получить список всех рецептов",
    description="Возвращает отсортированный список всех рецептов")
async def list_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Recipe).order_by(desc(Recipe.views), asc(Recipe.minutes))
    )
    return result.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail,
    summary="Получить рецепт по ID",
    description="Возвращает указанный рецепт")
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    recipe = await db.get(Recipe, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)

    return recipe


@app.post("/recipes", response_model=RecipeDetail, status_code=201, summary="Создание рецепта",
    description="Создаем рецепт с данными пользователя")
async def create_recipe(recipe_data: RecipeCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Recipe).where(Recipe.name == recipe_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Recipe already exists")

    new_recipe = Recipe(
        name=recipe_data.name,
        minutes=recipe_data.minutes,
        ingredients=recipe_data.ingredients,
        description=recipe_data.description,
        views=0
    )

    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)

    return RecipeCreated(
        id=new_recipe.id,
        message="Recipe add"
    )

if __name__ == '__main__':
    uvicorn.run('routes:app', reload=True)