-- Script de base de datos idempotente para Productos
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL,
    category VARCHAR(50) NOT NULL
);

INSERT INTO products (id, name, description, price, stock, category) 
VALUES 
    (1, 'Cuaderno Universitario', 'Cuaderno de 100 hojas a cuadros con logo UCE', 2.00, 800, 'Papeles y escritura'),
    (2, 'Esferográfico Azul', 'Esferográfico de punta fina de color azul', 0.50, 1000, 'Papeles y escritura'),
    (3, 'Esferográfico Negro', 'Esferográfico de punta fina de color negro', 0.50, 1000, 'Papeles y escritura'),
    (4, 'Carpeta de archivos', 'Carpeta anillada A4', 0.60, 100, 'Papeles y escritura'),
    (5, 'Mochila', 'Mochila ergonómica con compartimento para laptop con el logo UCE', 20.00, 50, 'Accesorios'),
    (6, 'Termo Metálico', 'Termo de acero inoxidable de 1 litro con el logo UCE', 10.00, 80, 'Accesorios'),
    (7, 'Memoria USB', 'Pendrive USB de 16GB de capacidad', 10.00, 100, 'Tecnología'),
    (8, 'Calculadora Científica', 'Calculadora con funciones avanzadas', 18.50, 50, 'Tecnología'),
    (9, 'Cable USB', 'Cable de datos y carga tipo C', 7.00, 50, 'Tecnología'),
    (10, 'Agua purificada', 'Agua embotellada de 1 litro', 0.80, 100, 'Bebidas y alimentos')
ON CONFLICT (id) DO NOTHING;

-- Sincronizar el contador de la secuencia SERIAL con el mayor ID existente (10)
SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));