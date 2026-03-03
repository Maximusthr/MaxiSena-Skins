CREATE TABLE Skins ( 
    id_skins                      SERIAL,
    nome                          VARCHAR(40) NOT NULL,
    estado                        VARCHAR(40),
    raridade                      VARCHAR(40),
    pattern                       INTEGER,
    wear_rating                   FLOAT,

    PRIMARY KEY (id_skins)
);
