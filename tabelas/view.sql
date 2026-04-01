CREATE OR REPLACE VIEW vw_relatorio_vendas AS
SELECT 
    c.id_compra,
    TO_CHAR(c.data_compra, 'DD/MM/YYYY HH24:MI') AS data_venda,
    cl.nome AS nome_cliente,
    v.nome AS nome_vendedor,
    p.forma_pagamento,
    p.status_confirmacao,
    c.valor_total AS valor_pago
FROM compras c
JOIN clientes cl ON c.id_cliente = cl.id_cliente
JOIN vendedores v ON c.id_vendedor = v.id_vendedor
JOIN pagamentos p ON c.id_pagamento = p.id_pagamento
ORDER BY c.data_compra DESC;

-- SELECT * FROM vw_relatorio_vendas;

CREATE OR REPLACE VIEW vw_estoque_critico AS
SELECT 
    id_skins,
    nome,
    tipo,
    categoria,
    estoque,
    valor
FROM skins
WHERE estoque < 5
ORDER BY estoque ASC;

-- SELECT * FROM vw_estoque_critico;