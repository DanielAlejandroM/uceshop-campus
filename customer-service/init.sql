-- Script de base de datos idempotente

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(10),
    address VARCHAR(200)
);

INSERT INTO customers (id, name, email, phone, address) 
VALUES 
    (1, 'Gabriela Adriana Morales', 'gabrielam@uce.edu.ec', '0982207382', 'Manuela Cañizares, Valle de los Chillos'),
    (2, 'María Augusta Velasquez', 'mariav@uce.edu.ec', '0987654321', 'La Gasca, Santa Clara'),
    (3, 'Carlos Osvaldo Pérez', 'carlosp@uce.edu.ec', '0993887776', 'Foch y Juan Leoón Mera'),
    (4, 'Ana María López', 'anaml@uce.edu.ec', '0996542234', 'Cumbayá, Sector Universidad San Francisco'),
    (5, 'David Alexis Benítez', 'davidb@uce.edu.ec', '0983263865', 'El Recreo, Sur de Quito'),
    (6, 'Sofia Belén Torres', 'sofiat@uce.edu.ec', '0970894217', '6 de Diciembre y Colón'),
    (7, 'Luis Fernando Mullo', 'luism@uce.edu.ec', '0992626772', 'El Comité del Pueblo, Norte de Quito'),
    (8, 'Elena Vanesa Gomez', 'elenag@uce.edu.ec', '0982431880', 'Naciones Unidas y Shyris'),
    (9, 'Javier Armando Silva', 'javiers@uce.edu.ec', '0971976486', 'San Bartolo, Sur de Quito'),
    (10,'Daniel Alejandro Morocho', 'danielm@uce.edu.ec', '0987632342', 'El teleférico, La Comuna')
ON CONFLICT (id) DO NOTHING;

-- Sincroniza el contador de la secuencia serial con el mayor ID existente
SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));
