from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Compra, ItemCompra, Skin, Cliente, Vendedor, Pagamento
from datetime import datetime

compras_bp = Blueprint('compras', __name__)

# CREATE venda
@compras_bp.route('/compras', methods=['POST'])
def registrar_compra():
    dados = request.get_json()

    # Extrai os blocos do JSON enviado pelo Postman
    id_cliente = dados.get('id_cliente')
    id_vendedor = dados.get('id_vendedor')
    dados_pagamento = dados.get('pagamento') # Dicionário: {"forma": "Pix", "status": "Confirmado"}
    itens_comprados = dados.get('itens')     # Lista: [{"id_skin": 1, "quantidade": 2}]

    formas_validas = ['cartão', 'cartao', 'boleto', 'pix', 'berries']
    status_validos = ['pendente', 'confirmado', 'cancelado']
    
    forma_enviada = dados_pagamento.get('forma_pagamento', '').lower()
    status_enviado = dados_pagamento.get('status_confirmacao', '').lower()

    if forma_enviada not in formas_validas:
        return jsonify({"erro": f"Forma de pagamento inválida. Aceitamos apenas: {', '.join(formas_validas)}"}), 400
        
    if status_enviado not in status_validos:
        return jsonify({"erro": "Status de pagamento inválido. Use: Pendente, Confirmado ou Cancelado."}), 400

    # Garante que o payload não veio vazio ou faltando partes
    if not all([id_cliente, id_vendedor, dados_pagamento, itens_comprados]):
        return jsonify({"erro": "Payload invalido. Envie id_cliente, id_vendedor, pagamento e itens."}), 400

    try:
        # Cliente + Vendedor
        cliente = Cliente.query.get(id_cliente)
        vendedor = Vendedor.query.get(id_vendedor)

        if not cliente or not vendedor:
            return jsonify({"erro": "Cliente ou Vendedor nao encontrado no sistema."}), 404

        subtotal = 0.0
        novos_itens = []

        # carrinho (Itens e Estoque)
        for item in itens_comprados:
            skin = Skin.query.get(item['id_skin'])
            quantidade = item.get('quantidade', 0)

            if not skin:
                raise ValueError(f"A skin de ID {item['id_skin']} nao existe.")
            if quantidade <= 0:
                raise ValueError("A quantidade comprada deve ser maior que zero.")
            
            # sem estoque = sem compra
            if skin.estoque < quantidade:
                raise ValueError(f"Estoque insuficiente para a skin '{skin.nome}'. Disponivel: {skin.estoque}.")

            # compra efetuada
            skin.estoque -= quantidade
            preco_unitario = skin.valor
            subtotal += (preco_unitario * quantidade)

            # relacionamento do item
            novo_item = ItemCompra(skin=skin, quantidade=quantidade, preco_unitario=preco_unitario)
            novos_itens.append(novo_item)

        # desconto cumulativo
        desconto_percentual = 0.0
        if cliente.torce_flamengo:
            desconto_percentual += 0.10
        if cliente.assiste_one_piece:
            desconto_percentual += 0.10
        if cliente.cidade.strip().lower() == 'sousa':
            desconto_percentual += 0.10

        valor_final = subtotal * (1 - desconto_percentual)

        # pagamento
        novo_pagamento = Pagamento(
            forma_pagamento=dados_pagamento.get('forma_pagamento', 'Berries'),
            status_confirmacao=dados_pagamento.get('status_confirmacao', 'Pendente')
        )
        db.session.add(novo_pagamento)
        db.session.flush() # Manda pro banco gerar o ID, mas não commita definitivamente ainda 

        # compra
        nova_compra = Compra(
            id_cliente=cliente.id_cliente,
            id_vendedor=vendedor.id_vendedor,
            id_pagamento=novo_pagamento.id_pagamento,
            valor_total=valor_final
        )
        data_personalizada = dados.get('data_compra')
        
        if data_personalizada:
            try:
                # Converte o texto "2026-04-15 10:00:00" para o formato que o banco entende
                nova_compra.data_compra = datetime.strptime(data_personalizada, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                db.session.rollback()
                return jsonify({"erro": "Formato de data inválido. Use AAAA-MM-DD HH:MM:SS"}), 400
        
        # lista de itens na compra
        nova_compra.itens.extend(novos_itens)
        db.session.add(nova_compra)

        # tudo salvo (Pagamento, Compra, Itens e Baixa de Estoque)
        db.session.commit()

        return jsonify({
            "mensagem": "Compra registrada com sucesso!",
            "id_compra": nova_compra.id_compra,
            "resumo": {
                "subtotal": round(subtotal, 2),
                "desconto_aplicado": f"{int(desconto_percentual * 100)}%",
                "valor_final_pago": round(valor_final, 2)
            }
        }), 201

    except ValueError as ve:
        # falta de estoque
        db.session.rollback()
        return jsonify({"erro": "Regra de negocio violada.", "detalhes": str(ve)}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha critica no servidor.", "detalhes": str(e)}), 500