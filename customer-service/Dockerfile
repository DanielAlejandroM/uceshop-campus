# Imagen optimizada, ligera y con un usuario no-root por seguridad

# Imagen base
FROM python:3.11-slim

# Crear usuario no-root por seguridad
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Asignar permisos al usuario no-root
RUN chown -R appuser:appuser /app
# Forzar al contenedor a ejecutar el proceso como Non-root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]