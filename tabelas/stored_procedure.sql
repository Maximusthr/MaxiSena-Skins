CREATE OR REPLACE PROCEDURE sp_aplicar_desconto_categoria(
    p_categoria VARCHAR, 
    p_percentual_desconto NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Atualiza o valor das skins reduzindo o percentual informado
    UPDATE skins
    SET valor = valor - (valor * (p_percentual_desconto / 100.0))
    WHERE categoria ILIKE p_categoria;
    
    COMMIT;
    
    RAISE NOTICE 'Desconto de %%% aplicado com sucesso na categoria %.', p_percentual_desconto, p_categoria;
END;
$$;

-- CALL sp_aplicar_desconto_categoria('Rifle', 15.0);