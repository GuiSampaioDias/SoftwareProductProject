'''
Lembrando ... quem digita .... erra

CREATE TABLE tbl_produto 
( 
    produto_id     BIGINT       NOT NULL   AUTO_INCREMENT, 
    NomeDoProduto  VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL, 
    litros         FLOAT(5,2)       NULL, 
    Peso_kg        FLOAT(6,2)       NULL,
    Preço          FLOAT(5,2)   NOT NULL, 
    Descrição      VARCHAR(45),
    Ingredientes   VARCHAR(45), 
    PRIMARY KEY (produto_id)
);

'''

