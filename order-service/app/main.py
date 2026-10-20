import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import get_db
from app.models import Order, OrderItem, OrderCreate, OrderResponse, OrderItemResponse

app = FastAPI(title="Order Service", version="1.0.0")

Instrumentator().instrument(app).expose(app)

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://customer-service:8000")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8001")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}

#funcion auxiliar para enriquecer la orden con nombres mediante peticiones HTTP
def enrich_order_data(order: Order, client: httpx.Client) -> OrderResponse:
    # 1. Consultar el nombre del cliente en Customer Service
    customer_name = "Desconocido"
    try:
        c_resp = client.get(f"{CUSTOMER_SERVICE_URL}/customers/{order.customer_id}")
        if c_resp.status_code == 200:
            customer_name = c_resp.json().get("name", "Desconocido")
    except httpx.RequestError:
        pass

    # 2. Consultar el nombre de cada producto en Product Service
    enriched_items = []
    for item in order.items:
        product_name = "Desconocido"
        try:
            p_resp = client.get(f"{PRODUCT_SERVICE_URL}/products/{item.product_id}")
            if p_resp.status_code == 200:
                product_name = p_resp.json().get("name", "Desconocido")
        except httpx.RequestError:
            pass

        enriched_items.append(
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=product_name,
                quantity=item.quantity,
                unit_price=float(item.unit_price)
            )
        )

    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        customer_name=customer_name,
        status=order.status,
        total=float(order.total),
        created_at=order.created_at,
        items=enriched_items
    )


@app.get("/orders", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    with httpx.Client() as client:
        return [enrich_order_data(order, client) for order in orders]

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Órden no encontrada")
    with httpx.Client() as client:
        return enrich_order_data(order, client)

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # 1. Validar cliente por HTTP
    customer_name = ""
    with httpx.Client() as client:
        try:
            cust_resp = client.get(f"{CUSTOMER_SERVICE_URL}/customers/{order_data.customer_id}")
            if cust_resp.status_code == 404:
                raise HTTPException(status_code=400, detail="El cliente especificado no existe")
            customer_name = cust_resp.json().get("name", "")
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
                    "product_name": product["name"],
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

    # Devuelve la orden construida con los nombres incluidos
    with httpx.Client() as client:
        return enrich_order_data(new_order, client)