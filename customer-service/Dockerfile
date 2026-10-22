FROM python:3.11-slim

# Se crea el usuario no-root 
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Se asigna permisos al usuario no-root
RUN chown -R appuser:appuser /app
# Fuerza al contenedor a ejecutar el proceso como Non-root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]