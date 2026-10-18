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
    (1, 'Cuaderno Universitario UCE', 'Cuaderno de 100 hojas a cuadros con logo UCE', 2.50, 150, 'Papelería'),
    (2, 'Esferográfico Azul', 'Bolígrafo de tinta seca punto mediano', 0.50, 300, 'Papelería'),
    (3, 'Mochila Ergonómica', 'Mochila acolchada con compartimento para laptop 15.6"', 35.00, 40, 'Accesorios'),
    (4, 'Termo Metálico UCE', 'Termo de acero inoxidable de 750ml para bebidas frías/calientes', 12.00, 80, 'Accesorios'),
    (5, 'Calculadora Científica', 'Calculadora con 240 funciones avanzadas', 18.50, 25, 'Electrónica'),
    (6, 'Memoria USB 64GB', 'Pendrive USB 3.0 de alta velocidad', 10.00, 60, 'Electrónica'),
    (7, 'Camiseta Facultativa', 'Camiseta 100% algodón de la Facultad de Ingeniería', 15.00, 50, 'Ropa'),
    (8, 'Taza Cerámica UCE', 'Taza institucional para café de 11oz', 5.00, 90, 'Hogar'),
    (9, 'Organizador de Escritorio', 'Set de malla metálica para lápices y documentos', 8.50, 35, 'Papelería'),
    (10, 'Mouse Inalámbrico', 'Mouse óptico ergonómico USB 2.4GHz', 11.00, 45, 'Electrónica')
ON CONFLICT (id) DO NOTHING;

-- Sincronizar el contador de la secuencia SERIAL con el mayor ID existente (10)
SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));