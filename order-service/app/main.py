import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import get_db
from app.models import Order, OrderItem, OrderCreate, OrderResponse

app = FastAPI(title="Order Service", version="1.0.0")

Instrumentator().instrument(app).expose(app)

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://customer-service:8000")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8001")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}

@app.get("/orders", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Órden no encontrada")
    return order

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # 1. Validar si el cliente existe llamando a customer-service
    with httpx.Client() as client:
        try:
            cust_resp = client.get(f"{CUSTOMER_SERVICE_URL}/customers/{order_data.customer_id}")
            if cust_resp.status_code == 404:
                raise HTTPException(status_code=400, detail="El cliente especificado no existe")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Customer Service no disponible")

    # 2. Validar productos y calcular el total llamando a product-service
    total_order = 0.0
    items_to_create = []

    with httpx.Client() as client:
        for item in order_data.items:
            try:
                prod_resp = client.get(f"{PRODUCT_SERVICE_URL}/products/{item.product_id}")
                if prod_resp.status_code == 404:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"El producto con ID {item.product_id} no existe"
                    )
                
                product = prod_resp.json()
                if product["stock"] < item.quantity:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Stock insuficiente para el producto '{product['name']}'"
                    )

                unit_price = float(product["price"])
                total_order += unit_price * item.quantity

                items_to_create.append({
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": unit_price
                })
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail="Product Service no disponible")

    # 3. Guardar la orden en la base de datos
    new_order = Order(
        customer_id=order_data.customer_id,
        status="COMPLETED",
        total=total_order
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 4. Guardar los ítems de la orden
    for item_data in items_to_create:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order