DROP TABLE IF EXISTS Itens_Compra;
DROP TABLE IF EXISTS Compras;
DROP TABLE IF EXISTS Pagamentos;
DROP TABLE IF EXISTS Vendedores;
DROP TABLE IF EXISTS Skins;
DROP TABLE IF EXISTS Clientes;

CREATE TABLE Clientes ( 
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(40) NOT NULL,
    cpf VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(40) NOT NULL,
    cidade VARCHAR(40) NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    torce_flamengo BOOLEAN DEFAULT FALSE,
    assiste_one_piece BOOLEAN DEFAULT FALSE
);

CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nome VARCHAR(40) NOT NULL,
    
);

CREATE TABLE Pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    forma_pagamento VARCHAR(20) NOT NULL, -- 'Cartao', 'Boleto', 'Pix', 'Berries'
    status_confirmacao VARCHAR(20) NOT NULL -- 'Pendente', 'Confirmado', 'Cancelado'
);

CREATE TABLE Skins ( 
    id_skins SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    nome VARCHAR(40) NOT NULL,
    categoria VARCHAR(40) NOT NULL,
    valor FLOAT NOT NULL,
    estado VARCHAR(40) NOT NULL,
    raridade VARCHAR(40) NOT NULL,
    pattern INTEGER NOT NULL,
    wear_rating FLOAT NOT NULL,
    estoque INTEGER NOT NULL CHECK (estoque >= 0), -- Não pode ficar negativo
    fabricado_em_mari BOOLEAN DEFAULT FALSE
);

CREATE TABLE Compras (
    id_compra SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_vendedor INTEGER NOT NULL,
    id_pagamento INTEGER NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total FLOAT NOT NULL, 

    FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente),
    FOREIGN KEY (id_vendedor) REFERENCES Vendedores (id_vendedor),
    FOREIGN KEY (id_pagamento) REFERENCES Pagamentos (id_pagamento)
);

CREATE TABLE Itens_Compra (
    id_item SERIAL PRIMARY KEY,
    id_compra INTEGER NOT NULL,
    id_skins INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario FLOAT NOT NULL, -- Guarda o preço do dia, caso a skin mude de valor depois

    FOREIGN KEY (id_compra) REFERENCES Compras (id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_skins) REFERENCES Skins (id_skins)
);