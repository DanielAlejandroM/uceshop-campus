# Define la aplicación de FastAPI, el healthcheck y los endpoints HTTP

from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import get_db
from app.models import Customer, CustomerCreate, CustomerResponse

app = FastAPI(title="Customer Service", version="1.0.0")

# Exponer métricas para Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "customer-service"}

# Endpoint para listar TODOS los clientes
@app.get("/customers", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

# Endpoint para buscar un cliente por su ID
@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer

# Endpoint POST para crear un nuevo cliente
@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    new_customer = Customer(
        name=customer.name, 
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer