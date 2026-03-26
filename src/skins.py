from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Skin

# Blueprint para as rotas do estoque de skins
skins_bp = Blueprint('skins', __name__)

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
        estoque=dados.get('estoque', 0), # zero se nao definir
        fabricado_em_mari=dados.get('fabricado_em_mari', False)
    )
    
    try:
        db.session.add(nova_skin)
        db.session.commit()
        return jsonify({
            "mensagem": f"Skin {nova_skin.nome} cadastrada no estoque!", 
            "id_skins": nova_skin.id_skins
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao cadastrar a skin.", "detalhes": str(e)}), 400

@skins_bp.route('/skins', methods=['GET'])
def listar_skins():
    # Recupera o parâmetro 'ordem' da URL (Ex: /skins?ordem=crescente)
    ordem = request.args.get('ordem')
    
    # Inicia a consulta base
    query = Skin.query
    
    # Aplica a ordenação no banco de dados se o usuário pedir
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

@skins_bp.route('/skins/<int:id>', methods=['PUT'])
def atualizar_skin(id):
    skin = Skin.query.get(id)
    
    if not skin:
        return jsonify({"erro": "Skin não encontrada."}), 404
        
    dados = request.get_json()
    
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
        return jsonify({"mensagem": f"Skin {skin.nome} atualizada com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao atualizar a skin.", "detalhes": str(e)}), 400

@skins_bp.route('/skins/<int:id>', methods=['DELETE'])
def deletar_skin(id):
    skin = Skin.query.get(id)
    
    if not skin:
        return jsonify({"erro": "Skin não encontrada."}), 404
        
    try:
        db.session.delete(skin)
        db.session.commit()
        return jsonify({"mensagem": f"Skin {skin.nome} removida do estoque!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Não é possível deletar esta skin pois ela já faz parte de uma compra registrada.", "detalhes": str(e)}), 400