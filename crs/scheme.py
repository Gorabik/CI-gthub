from pydantic import BaseModel, Field, ConfigDict
class RecipeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    minutes: int = Field(..., ge=1, le=1440)
    ingredients: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)

class RecipeCreate(RecipeBase):
    pass


class RecipeListItem(BaseModel):
    id: int
    name: str
    views: int
    minutes: int
    model_config = ConfigDict(from_attributes=True)


class RecipeDetail(RecipeBase):
    id: int
    views: int
    model_config = ConfigDict(from_attributes=True)


class RecipeCreated(BaseModel):
    id: int
    message: str
