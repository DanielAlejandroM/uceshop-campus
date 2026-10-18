# Define la tabla SQLAlchemy y los esquemas Pydantic para validación de datos

from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from app.database import Base

# Modelo de Base de Datos
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Esquema Pydantic para respuesta de API
class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True