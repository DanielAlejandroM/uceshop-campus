# Define la aplicación de FastAPI, el healthcheck y los endpoints HTTP

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import get_db
from app.models import Customer, CustomerResponse

app = FastAPI(title="Customer Service", version="1.0.0")

# Exponer métricas para Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "customer-service"}

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer