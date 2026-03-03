CREATE TABLE Skins ( 
    id_skins                      SERIAL,
    nome                          VARCHAR(40) NOT NULL,
    estado                        VARCHAR(40),
    raridade                      VARCHAR(40),
    pattern                       INTEGER,
    wear_rating                   FLOAT,

    PRIMARY KEY (id_skins)
);
CREATE TABLE Clientes ( 
    id_cliente                    SERIAL,
    nome                          VARCHAR(40) NOT NULL,
    cpf                           VARCHAR(15) UNIQUE NOT NULL,
    email                         VARCHAR(40) NOT NULL,
    cidade                        VARCHAR(40) NOT NULL,
    telefone                      VARCHAR(15) NOT NULL,

    PRIMARY KEY (id_cliente)
);