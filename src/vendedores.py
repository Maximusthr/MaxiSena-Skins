from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Vendedor

# Cria o Blueprint para as rotas de vendedores
vendedores_bp = Blueprint('vendedores', __name__)

@vendedores_bp.route('/vendedores', methods=['POST'])
def cadastrar_vendedor():
    dados = request.get_json()
    
    # garantir que o nome foi enviado
    if 'nome' not in dados or not dados['nome'].strip():
        return jsonify({"erro": "O nome do vendedor é obrigatorio."}), 400

    novo_vendedor = Vendedor(
        nome=dados.get('nome')
    )
    
    try:
        db.session.add(novo_vendedor)
        db.session.commit()
        return jsonify({
            "mensagem": f"Vendedor(a) {novo_vendedor.nome} cadastrado(a) com sucesso!", 
            "id_vendedor": novo_vendedor.id_vendedor
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao cadastrar o vendedor.", "detalhes": str(e)}), 400

@vendedores_bp.route('/vendedores', methods=['GET'])
def listar_vendedores():
    vendedores = Vendedor.query.all()
    
    lista_retorno = []
    for v in vendedores:
        lista_retorno.append({
            "id": v.id_vendedor,
            "nome": v.nome
        })
        
    return jsonify(lista_retorno), 200

@vendedores_bp.route('/vendedores/<int:id>', methods=['PUT'])
def atualizar_vendedor(id):
    vendedor = Vendedor.query.get(id)
    
    if not vendedor:
        return jsonify({"erro": "Vendedor nao encontrado."}), 404
        
    dados = request.get_json()
    
    # Atualiza o nome se ele for enviado no JSON
    vendedor.nome = dados.get('nome', vendedor.nome)
    
    try:
        db.session.commit()
        return jsonify({"mensagem": f"Dados do vendedor(a) atualizados para: {vendedor.nome}!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao atualizar o vendedor.", "detalhes": str(e)}), 400

@vendedores_bp.route('/vendedores/<int:id>', methods=['DELETE'])
def deletar_vendedor(id):
    vendedor = Vendedor.query.get(id)
    
    if not vendedor:
        return jsonify({"erro": "Vendedor nao encontrado."}), 404
        
    try:
        db.session.delete(vendedor)
        db.session.commit()
        return jsonify({"mensagem": f"Vendedor(a) {vendedor.nome} removido(a) do sistema!"}), 200
        
    except Exception as e:
        db.session.rollback()
        # se o vendedor já registrou alguma venda, o banco bloqueia a exclusão!
        return jsonify({"erro": "Nao eh possivel deletar este vendedor pois ele ja possui vendas registradas.", "detalhes": str(e)}), 400
    

# READ
@vendedores_bp.route('/vendedores/<int:id>/relatorio', methods=['GET'])
def relatorio_vendedor(id):
    vendedor = Vendedor.query.get(id)
    
    if not vendedor:
        return jsonify({"erro": "Vendedor não encontrado."}), 404

    # Pega os parâmetros da URL para filtrar por data (Ex: ?mes=3&ano=2026)
    # Se o usuário não passar, o default será None
    mes_filtro = request.args.get('mes', type=int)
    ano_filtro = request.args.get('ano', type=int)

    compras_filtradas = []
    total_arrecadado = 0.0

    # backref 'compras' traz todas as vendas que este vendedor já fez
    for compra in vendedor.compras:
        
        # Lógica de Filtro: Se o gerente pediu um mês/ano específico, 
        # nós ignoramos as compras que não batem com a data.
        if mes_filtro and compra.data_compra.month != mes_filtro:
            continue
        if ano_filtro and compra.data_compra.year != ano_filtro:
            continue

        # Soma ao caixa do vendedor
        total_arrecadado += compra.valor_total
        
        # Monta o resumo daquela venda específica
        compras_filtradas.append({
            "id_compra": compra.id_compra,
            "data": compra.data_compra.strftime("%d/%m/%Y %H:%M"),
            "valor_da_venda": round(compra.valor_total, 2),
            "id_cliente": compra.id_cliente,
            "status_pagamento": compra.pagamento.status_confirmacao
        })

    # relatório completo
    return jsonify({
        "vendedor": vendedor.nome,
        "filtros_aplicados": {
            "mes": mes_filtro if mes_filtro else "Todos",
            "ano": ano_filtro if ano_filtro else "Todos"
        },
        "resumo_financeiro": {
            "quantidade_de_vendas": len(compras_filtradas),
            "total_arrecadado": round(total_arrecadado, 2)
        },
        "detalhes_das_vendas": compras_filtradas
    }), 200