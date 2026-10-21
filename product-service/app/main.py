import threading
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import get_db
from app.models import Product, ProductCreate, ProductResponse
from app.consumer import start_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lanzar el consumidor de RabbitMQ en un hilo secundario al iniciar el servicio
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    yield

app = FastAPI(title="Product Service", version="1.0.0", lifespan=lifespan)

# Exponer métricas para Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "product-service"}

# Endpoint para listar TODOS los productos
@app.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Endpoint para consultar un producto por su ID
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

# Endpoint POST para crear un nuevo producto
@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product