-- Script de base de datos idempotente para Órdenes
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

-- Registros de prueba iniciales
INSERT INTO orders (id, customer_id, status, total) 
VALUES (1, 1, 'COMPLETED', 22.00)
ON CONFLICT (id) DO NOTHING;

INSERT INTO order_items (id, order_id, product_id, quantity, unit_price)
VALUES 
    (1, 1, 1, 1, 2.00),   -- 1 Cuaderno universitario ($2.00)
    (2, 1, 5, 1, 20.00)   -- 1 Mochila ($20.00)
ON CONFLICT (id) DO NOTHING;

-- Sincronización de secuencias
SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));
SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));