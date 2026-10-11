IF DB_ID('seguradora') IS NULL CREATE DATABASE seguradora;
GO
USE seguradora;
GO

DROP TABLE IF EXISTS apolice;
DROP TABLE IF EXISTS carro;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS marca;
GO

CREATE TABLE marca (
    id   INT PRIMARY KEY,
    nome VARCHAR(40) NOT NULL
);

CREATE TABLE cliente (
    id     INT PRIMARY KEY,
    nome   NVARCHAR(80) NOT NULL,
    cpf    VARCHAR(11) NOT NULL,
    cidade NVARCHAR(60)
);

CREATE TABLE carro (
    placa      VARCHAR(7) PRIMARY KEY,
    modelo     VARCHAR(40) NOT NULL,
    chassi     VARCHAR(20) NOT NULL,
    marca_id   INT REFERENCES marca (id),
    ano        INT,
    cor        VARCHAR(20),
    cliente_id INT REFERENCES cliente (id)
);

CREATE TABLE apolice (
    id          INT PRIMARY KEY,
    placa       VARCHAR(7) REFERENCES carro (placa),
    valor       DECIMAL(10, 2) NOT NULL,
    data_inicio DATE NOT NULL
);
GO

INSERT INTO marca VALUES
    (1, 'RENAULT'), (2, 'HYUNDAI'), (3, 'FIAT'), (4, 'FORD'), (5, 'GM'), (6, 'VOLKSWAGEN');

INSERT INTO cliente VALUES
    (1, N'Ana Souza',     '11111111111', N'Criciúma'),
    (2, N'Bruno Lima',    '22222222222', N'Florianópolis'),
    (3, N'Carla Pereira', '33333333333', N'Tubarão'),
    (4, N'Diego Martins', '44444444444', N'Içara');

INSERT INTO carro VALUES
    ('ALD3834', 'CLIO',      '34574215969', 1, 2011, 'BRANCO',  1),
    ('CCR8096', 'CRETA',     '88547875547', 2, 2020, 'BRANCO',  1),
    ('DLA3438', 'PUNTO',     '98823483434', 3, 2013, 'PRETO',   2),
    ('EEE1056', 'ECO SPORT', '56753453455', 4, 2020, 'AZUL',    2),
    ('FFR1234', 'PALIO',     '32383478747', 3, 2020, 'AMARELO', 3),
    ('GQY6753', 'S10',       '72004160549', 5, 2015, 'PRETO',   3),
    ('IAC8974', 'TIGUAN',    '77130757746', 6, 2020, 'AZUL',    4),
    ('JIE0952', 'PASSAT',    '87493270405', 6, 2016, 'CINZA',   4);

INSERT INTO apolice VALUES
    (1, 'ALD3834', 1850.00, '2024-01-10'),
    (2, 'CCR8096', 2790.50, '2024-02-15'),
    (3, 'DLA3438', 1620.00, '2024-03-01'),
    (4, 'EEE1056', 2310.75, '2024-03-20'),
    (5, 'FFR1234', 1980.00, '2024-04-05'),
    (6, 'GQY6753', 3150.00, '2024-05-12'),
    (7, 'IAC8974', 3890.90, '2024-06-01'),
    (8, 'JIE0952', 3420.00, '2024-06-18');
GO
