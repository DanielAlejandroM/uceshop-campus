from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric
from pydantic import BaseModel
from app.database import Base

# Modelo de Base de Datos (SQLAlchemy)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=False)

# Esquema Pydantic para crear producto (Body del POST)
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str

# Esquema Pydantic para respuesta (GET y POST)
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str

    class Config:
        from_attributes = True