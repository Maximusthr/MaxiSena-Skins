CREATE TABLE Skins ( 
    id_skins                      SERIAL,
    nome                          VARCHAR(40) NOT NULL,
    valor                         FLOAT NOT NULL,
    estado                        VARCHAR(40) NOT NULL,
    raridade                      VARCHAR(40) NOT NULL,
    pattern                       INTEGER NOT NULL,
    wear_rating                   FLOAT NOT NULL,

    PRIMARY KEY (id_skins)
);
CREATE TABLE Clientes ( 
    id_cliente                    SERIAL,
    nome                          VARCHAR(40) NOT NULL,
    cpf                           VARCHAR(15) UNIQUE NOT NULL,
    email                         VARCHAR(40) NOT NULL ,
    cidade                        VARCHAR(40) NOT NULL ,
    telefone                      VARCHAR(15) NOT NULL,

    PRIMARY KEY (id_cliente)
);
CREATE TABLE Compras (
    id_compra                     SERIAL,
    id_cliente                    INTEGER NOT NULL,
    id_skins                      INTEGER NOT NULL,
    data_compra                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_final                   FLOAT NOT NULL, 

    PRIMARY KEY (id_compra),
    FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente),
    FOREIGN KEY (id_skins) REFERENCES Skins (id_skins)
);