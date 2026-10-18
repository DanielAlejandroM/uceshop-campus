# Define la tabla SQLAlchemy y los esquemas Pydantic para validación de datos

from typing import Optional
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from app.database import Base

# Modelo de Base de Datos
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)


# Esquema Pydantic para crear cliente (body - POST)
class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

# Esquema Pydantic para respuesta (GET y POST)
class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True