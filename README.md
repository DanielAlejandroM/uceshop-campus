# UCEShop Campus — Arquitectura de Microservicios
**UCEShop Campus** una mini tienda e-commerce para vender artículos institucionales de la UCE, desarrollada como Caso Práctico de Titulación para la **Universidad Central del Ecuador** (Carrera de Ingenieria en Sistemas de Información).

La arquitectura está basada en microservicios independientes creados con **FastAPI (Python)**, aplicando el patrón **Database-per-Service** sobre motores **PostgreSQL**, comunicación híbrida (Síncrona HTTP/REST y Asíncrona Orientada a Eventos con **RabbitMQ**) y monitoreo en tiempo real instrumentado con **Prometheus** y **Grafana**. El despliegue de producción se realizó en la nube de **Amazon Web Services (AWS)** mediante **Amazon ECR, EC2, Auto Scaling Group (ASG), Application Load Balancer (ALB) y Amazon API Gateway**.

## Stack Tecnológico
- **Backend:** Python 3.11, FastAPI, SQLAlchemy.
- **Infraestructura Local:** Docker, Docker Compose v3.9.
- **Mensajería & Monitoreo:** RabbitMQ, Prometheus, Grafana.
- **Cloud (AWS):** EC2, Auto Scaling Group (ASG), Application Load Balancer (ALB), API Gateway.

### Ejecutar con Docker Compose

**Clonar el repositorio**
git clone https://github.com/DanielAlejandroM/uceshop-campus.git
   cd uceshop-campus

**Construir y ejecutar los servicios**
**Construir imágenes y levantar servicios**
   docker-compose up --build

**Ejecutar en segundo plano**
   docker-compose up -d --build

**verificar servicios activos**
   docker-compose ps

**para ver datos por consola**
customers
   docker exec -it customer-db psql -U postgres -d customersdb -c "SELECT * FROM customers;"
products
   docker exec -it product-db psql -U postgres -d productsdb -c "SELECT * FROM products;"
orders
   docker exec -it order-db psql -U postgres -d ordersdb -c "SELECT * FROM order_items;"

## Arquitectura del Sistema

El stack se compone de 9 contenedores interconectados en una red Docker privada:
1. Customer Service (puerto`:8000`)
2. Product Service (puerto`:8001`)
3. Order Service (puerto`:8002`).  
4. RabbitMQ Broker (`:5672`, UI `:15672`): int de mensajes para el procesamiento asíncrono
5. Prometheus (`:9090`) recoleccta métricas (cada 5s) a través de los endpoints `/metrics` de los microservicios.
6. Grafana (`:3000`): interfaz visual para la veer métricas
Persistencia aislada
7. `customersdb` (PostgreSQL - Puerto interno `5432`)
8. `productsdb` (PostgreSQL - Puerto interno `5432`) escucha eventos AMQP de RabbitMQ
9. `ordersdb` (PostgreSQL - Puerto interno `5432`) hace validaciones síncronas HTTP con los otros dos microservicios y publica eventos hacia RabbitMQ.

## Flujo Completo de Integración (Cliente ➔ Producto ➔ Pedido)

### En herramienta como POSTMAN probar los health y las consutlas Get de customers, y por id de customers
http://localhost:8000/health
http://localhost:8000/customers
http://localhost:8000/customers/1

### para POST en consumers
{
    "name": "Pablo Miguel Nuñez",
    "email": "pablon@uce.edu.ec",
    "phone": "0983247852",
    "address": "Cotocollao, Norte de Quito"
}

### En POSTMAN probar los health y las consutlas Get de products, y por id de products
http://localhost:8001/health
http://localhost:8001/products
http://localhost:8001/products/1

### para POST en consumers
{
    "name": "Gaseosa",
    "description": "Coca-cola de 0.5 litros",
    "price": 0.60,
    "stock": 10,
    "category": "Bebidas y alimentos"
}

### En POSTMAN probar los health y las consutlas Get de products, y por id de orders
http://localhost:8002/health
http://localhost:8002/orders
http://localhost:8001/orders/1

### Petición Entrante (POST /orders)
El cliente (desde Postman o la API pública) envía una solicitud de creación de orden a `order-service` indicando el `customer_id` y la lista de ítems (`product_id` y `quantity`):

{
  "customer_id": 10,
  "items": [
    {
      "product_id": 5,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 2
    },
    {
      "product_id": 8,
      "quantity": 2
    }
  ]
}

### Acceso a interfaces y documentación iteractiva
- RabbitMQ Management Console: http://localhost:15672 (Credenciales: guest / guest)

- Prometheus Web UI: http://localhost:9090

- Grafana Dashboards: http://localhost:3000 (Credenciales: admin / admin)


### Despliegue en Amazon Web Services
- Amazon ECR: Compilación y etiquetado (tagging) de las imágenes Docker de los tres microservicios, almacenándolas en repositorios privados de ECR.

- AWS EC2 & Launch Templates: Creación de una plantilla de lanzamiento (Launch Template) configurada con UserData para la autenticación en ECR y el arranque automático del stack mediante docker-compose.prod.yml.

- Auto Scaling Group (ASG) & ALB: Enlace a un Application Load Balancer público con tres Target Groups orientados a los puertos 8000, 8001 y 8002, garantizando auto-reparación (self-healing) y balanceo de carga.

- Amazon API Gateway: Configuración de un punto de entrada unificado (HTTP API) enrutando el tráfico externo hacia el DNS del ALB.

### Creado por: Daniel Alejandro Morocho - Estudiante egresado de la carrera de Ingeniería en Sistemas de la Universidad Central del Ecuador
