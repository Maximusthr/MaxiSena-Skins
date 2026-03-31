-- filtros da loja
CREATE INDEX idx_skins_categoria ON skins(categoria);

-- busca por nome das skins
-- 
CREATE INDEX idx_skins_nome ON skins(nome);

-- Chaves Estrangeiras
CREATE INDEX idx_compras_cliente ON compras(id_cliente);
CREATE INDEX idx_compras_vendedor ON compras(id_vendedor);

-- data da compra (relatório mensal do vendedor
CREATE INDEX idx_compras_data ON compras(data_compra);

-- EXPLAIN ANALYZE SELECT * FROM skins WHERE categoria = 'Rifle';