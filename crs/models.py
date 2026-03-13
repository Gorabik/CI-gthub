from sqlalchemy import Column, Integer, String, Text
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    minutes = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Recipe(id={self.id}, name='{self.name}', views={self.views})>"

