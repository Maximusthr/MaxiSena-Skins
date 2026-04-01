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
    
    RAISE NOTICE 'Desconto de %%% aplicado com sucesso na categoria %.', p_percentual_desconto, p_categoria;
END;
$$;

-- CALL sp_aplicar_desconto_categoria('Rifle', 15.0);


CREATE OR REPLACE PROCEDURE sp_reajuste_mercado()
LANGUAGE plpgsql
AS $$
DECLARE
    skin_atual RECORD; 
    novo_preco NUMERIC;
BEGIN
    FOR skin_atual IN SELECT * FROM skins LOOP
        novo_preco := skin_atual.valor;

        -- alta demanda e pouca oferta
        IF skin_atual.raridade IN ('Extraordinario', 'Contrabandeado', 'Oculto', 'Covert', 'Secreto', 'Contraband') AND skin_atual.estoque < 3 THEN
            novo_preco := skin_atual.valor * 1.10; 
            
        -- queima de estoque
        ELSIF skin_atual.raridade IN ('Consumidor', 'Industrial', 'Militar', 'Restrito', 'Mil-Spec', 'Restricted') AND skin_atual.estoque > 8 THEN
            novo_preco := skin_atual.valor * 0.90; 
        END IF;

        IF novo_preco != skin_atual.valor THEN
            UPDATE skins SET valor = novo_preco WHERE id_skins = skin_atual.id_skins;
        END IF;

    END LOOP;
    
END;
$$;

-- CALL sp_reajuste_mercado()