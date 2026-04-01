from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Skin
from sqlalchemy import text

# Cria o Blueprint para as rotas do stock de skins
skins_bp = Blueprint('skins', __name__)

# CREATE skins
@skins_bp.route('/skins', methods=['POST'])
def cadastrar_skin():
    dados = request.get_json()
    
    nova_skin = Skin(
        tipo=dados.get('tipo'),
        nome=dados.get('nome'),
        categoria=dados.get('categoria'),
        valor=dados.get('valor'),
        estado=dados.get('estado'),
        raridade=dados.get('raridade'),
        pattern=dados.get('pattern'),
        wear_rating=dados.get('wear_rating'),
        estoque=dados.get('estoque', 0), # Começa com zero se não for definido
        fabricado_em_mari=dados.get('fabricado_em_mari', False)
    )
    
    try:
        db.session.add(nova_skin)
        db.session.commit()
        return jsonify({
            "mensagem": f"Skin '{nova_skin.nome}' cadastrada no stock com sucesso!", 
            "id_skins": nova_skin.id_skins
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao cadastrar a skin.", "detalhes": str(e)}), 400

# READ skins
@skins_bp.route('/skins', methods=['GET'])
def listar_skins():
    # Recupera o parâmetro 'ordem' da URL (Ex: /skins?ordem=crescente)
    ordem = request.args.get('ordem')
    
    # Inicia a consulta base
    query = Skin.query
    
    # Aplica a ordenação no banco de dados consoante o pedido do utilizador
    if ordem == 'crescente':
        query = query.order_by(Skin.valor.asc())
    elif ordem == 'decrescente':
        query = query.order_by(Skin.valor.desc())
        
    skins = query.all()
    
    lista_retorno = []
    for s in skins:
        lista_retorno.append({
            "id": s.id_skins,
            "tipo": s.tipo,
            "nome": s.nome,
            "categoria": s.categoria,
            "valor": s.valor,
            "estado": s.estado,
            "raridade": s.raridade,
            "pattern": s.pattern,
            "wear_rating": s.wear_rating,
            "estoque": s.estoque,
            "fabricado_em_mari": s.fabricado_em_mari
        })
        
    return jsonify(lista_retorno), 200

# UPDATE skins
@skins_bp.route('/skins/<int:id>', methods=['PUT'])
def atualizar_skin(id):
    skin = Skin.query.get(id)
    
    if not skin:
        return jsonify({"erro": "Skin não encontrada."}), 404
        
    dados = request.get_json()
    
    # Atualiza apenas os campos que foram enviados no JSON
    skin.tipo = dados.get('tipo', skin.tipo)
    skin.nome = dados.get('nome', skin.nome)
    skin.categoria = dados.get('categoria', skin.categoria)
    skin.valor = dados.get('valor', skin.valor)
    skin.estado = dados.get('estado', skin.estado)
    skin.raridade = dados.get('raridade', skin.raridade)
    skin.pattern = dados.get('pattern', skin.pattern)
    skin.wear_rating = dados.get('wear_rating', skin.wear_rating)
    skin.estoque = dados.get('estoque', skin.estoque)
    skin.fabricado_em_mari = dados.get('fabricado_em_mari', skin.fabricado_em_mari)
    
    try:
        db.session.commit()
        return jsonify({"mensagem": f"Skin '{skin.nome}' atualizada com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao atualizar a skin.", "detalhes": str(e)}), 400

# DELETE skins
@skins_bp.route('/skins/<int:id>', methods=['DELETE'])
def deletar_skin(id):
    skin = Skin.query.get(id)
    
    if not skin:
        return jsonify({"erro": "Skin não encontrada."}), 404
        
    try:
        db.session.delete(skin)
        db.session.commit()
        return jsonify({"mensagem": f"Skin '{skin.nome}' removida do stock!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "erro": "Não é possível eliminar esta skin pois ela já faz parte de uma compra registada (Integridade Referencial).", 
            "detalhes": str(e)
        }), 400

# Filtrar skins
@skins_bp.route('/skins/filtrar', methods=['GET'])
def filtrar_skins():
    # filtro por: nome, faixa de preço, categoria e se foram fabricados em Mari
    nome_pesquisa = request.args.get('nome')
    categoria = request.args.get('categoria')
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    
    # Como booleanos em URL vêm como string ('true', 'false'), fazemos esta conversão
    fabricado_mari_str = request.args.get('mari')
    fabricado_mari = None
    if fabricado_mari_str is not None:
        fabricado_mari = fabricado_mari_str.lower() == 'true'

    query = Skin.query

    # Aplica os filtros de forma dinâmica (apenas se o utilizador os enviou na URL)
    if nome_pesquisa:
        query = query.filter(Skin.nome.ilike(f"%{nome_pesquisa}%"))
    if categoria:
        query = query.filter(Skin.categoria.ilike(f"%{categoria}%"))
    if preco_min is not None:
        query = query.filter(Skin.valor >= preco_min)
    if preco_max is not None:
        query = query.filter(Skin.valor <= preco_max)
    if fabricado_mari is not None:
        query = query.filter(Skin.fabricado_em_mari == fabricado_mari)

    skins = query.all()
    
    lista_retorno = []
    for s in skins:
        lista_retorno.append({
            "id": s.id_skins,
            "nome": s.nome,
            "categoria": s.categoria,
            "valor": s.valor,
            "estoque": s.estoque,
            "fabricado_em_mari": s.fabricado_em_mari
        })
        
    return jsonify(lista_retorno), 200

# Estoque baixo
@skins_bp.route('/skins/estoque-baixo', methods=['GET'])
def verificar_estoque_baixo():
    # "Caso seja um funcionário usando o sistema, ele deve poder filtrar pelos 
    # produtos que possuem menos que 5 unidades disponíveis."
    skins_em_alerta = Skin.query.filter(Skin.estoque < 5).all()
    
    lista_retorno = []
    for s in skins_em_alerta:
        lista_retorno.append({
            "id": s.id_skins,
            "nome": s.nome,
            "estoque": s.estoque,
            "alerta": "STOCK CRÍTICO"
        })
        
    return jsonify({
        "total_itens_em_alerta": len(lista_retorno), 
        "produtos": lista_retorno
    }), 200


# desconto
@skins_bp.route('/aplicar-desconto', methods=['POST'])
def aplicar_desconto():
    dados = request.get_json()
    categoria = dados.get('categoria')
    percentual = dados.get('percentual')
    
    if not categoria or percentual is None:
        return jsonify({"erro": "Categoria e percentual são obrigatórios."}), 400
        
    try:
        # AQUI A MÁGICA ACONTECE: O Python manda o banco executar a Procedure!
        query = text("CALL sp_aplicar_desconto_categoria(:cat, :perc)")
        db.session.execute(query, {"cat": categoria, "perc": percentual})
        db.session.commit()
        
        return jsonify({"mensagem": f"Sucesso! Desconto de {percentual}% aplicado na categoria {categoria}."}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao executar a Procedure.", "detalhes": str(e)}), 500