# Script de base de datos idempotente


CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO customers (id, name, email) 
VALUES (1, 'Daniel Morocho', 'daniel@uce.edu.ec')
ON CONFLICT (id) DO NOTHING;