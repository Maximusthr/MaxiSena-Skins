from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Vendedor
from sqlalchemy import text  

# Cria o Blueprint para as rotas de vendedores
vendedores_bp = Blueprint('vendedores', __name__)

@vendedores_bp.route('/vendedores', methods=['POST'])
def cadastrar_vendedor():
    dados = request.get_json()
    
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not all([nome, email, senha]):
        return jsonify({"erro": "O nome, email e senha do vendedor são obrigatórios."}), 400

    novo_vendedor = Vendedor(
        nome=nome,
        email=email,
        senha=senha
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
        return jsonify({"erro": "Falha ao cadastrar o vendedor. Verifique se o e-mail já existe.", "detalhes": str(e)}), 400

@vendedores_bp.route('/vendedores', methods=['GET'])
def listar_vendedores():
    vendedores = Vendedor.query.all()
    
    lista_retorno = []
    for v in vendedores:
        lista_retorno.append({
            "id": v.id_vendedor,
            "nome": v.nome,
            "email": v.email
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
    vendedor.email = dados.get('email', vendedor.email) 
    vendedor.senha = dados.get('senha', vendedor.senha) 
    
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

@vendedores_bp.route('/relatorio-geral', methods=['GET'])
def relatorio_geral_view():
    try:
        query = text("SELECT * FROM vw_relatorio_vendas")
        resultado = db.session.execute(query).mappings().all()
        
        # Monta a lista para o Front-end
        lista_relatorio = []
        for linha in resultado:
            lista_relatorio.append({
                "id_compra": linha['id_compra'],
                "data_venda": linha['data_venda'],
                "nome_cliente": linha['nome_cliente'],
                "nome_vendedor": linha['nome_vendedor'],
                "forma_pagamento": linha['forma_pagamento'],
                "status_confirmacao": linha['status_confirmacao'],
                "valor_pago": float(linha['valor_pago']) 
            })
            
        return jsonify(lista_relatorio), 200
        
    except Exception as e:
        return jsonify({"erro": "Falha ao consultar a View no banco de dados.", "detalhes": str(e)}), 500
    

@vendedores_bp.route('/estoque-critico', methods=['GET'])
def estoque_critico_view():
    try:
        # Chama a View criada diretamente no PostgreSQL
        query = text("SELECT * FROM vw_estoque_critico")
        resultado = db.session.execute(query).mappings().all()
        
        # Monta a lista formatada para o Front-end
        lista_estoque = []
        for linha in resultado:
            lista_estoque.append({
                "id_skins": linha['id_skins'], # Se a sua coluna de ID no banco chamar apenas 'id', troque aqui para linha['id']
                "nome": linha['nome'],
                "tipo": linha['tipo'],
                "categoria": linha['categoria'],
                "estoque": linha['estoque'],
                "valor": float(linha['valor']) # Garante que o valor decimal do banco vá como float para o JSON
            })
            
        return jsonify(lista_estoque), 200
        
    except Exception as e:
        return jsonify({
            "erro": "Falha ao consultar a View de estoque crítico no banco de dados.", 
            "detalhes": str(e)
        }), 500
    
@vendedores_bp.route('/reajuste-mercado', methods=['POST'])
def reajuste_mercado():
    try:
        query = text("CALL sp_reajuste_mercado()")
        db.session.execute(query)
        db.session.commit()
        
        return jsonify({"mensagem": "Reajuste de mercado concluído! Preços atualizados conforme oferta e demanda."}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao rodar o algoritmo de reajuste.", "detalhes": str(e)}), 500