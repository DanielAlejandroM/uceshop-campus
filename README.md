# UCEShop Campus - Microservicios

Proyecto de arquitectura distribuida (Database-per-Service) implementado para la materia de Computación en la Nube.

## Arquitectura
El sistema se compone de tres microservicios independientes:
1. **Customer Service:** Gestión de clientes (PostgreSQL).
2. **Product Service:** Gestión del catálogo de productos (PostgreSQL).
3. **Order Service:** Orquestador que valida HTTP y calcula totales (PostgreSQL).

## Stack Tecnológico
- **Backend:** Python 3.11, FastAPI, SQLAlchemy.
- **Infraestructura Local:** Docker, Docker Compose v3.9.
- **Mensajería & Monitoreo:** RabbitMQ, Prometheus, Grafana.
- **Cloud (AWS):** EC2, Auto Scaling Group (ASG), Application Load Balancer (ALB), API Gateway.

## Instrucciones de Ejecución Local
*(Se añadirán los comandos de Docker Compose una vez finalizada la configuración).*