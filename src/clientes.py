from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Cliente

# Cria o Blueprint para as rotas de clientes
clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.get_json()
    
    # Objeto da nossa Classe (SQLAlchemy)
    novo_cliente = Cliente(
        nome=dados.get('nome'),
        cpf=dados.get('cpf'),
        email=dados.get('email'),
        cidade=dados.get('cidade'),
        telefone=dados.get('telefone'),
        torce_flamengo=dados.get('torce_flamengo', False),      # Se não enviarem, assume False
        assiste_one_piece=dados.get('assiste_one_piece', False) # Se não enviarem, assume False
    )
    
    try:
        # INSERT
        db.session.add(novo_cliente)
        db.session.commit()
        
        return jsonify({
            "mensagem": f"Cliente {novo_cliente.nome} cadastrado com sucesso!", 
            "id_cliente": novo_cliente.id_cliente
        }), 201
        
    except Exception as e:
        db.session.rollback()
        # Cpf em uso
        return jsonify({"erro": "Falha ao cadastrar. Verifique se o CPF já está em uso.", "detalhes": str(e)}), 400

@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    # "SELECT * FROM Clientes"
    clientes = Cliente.query.all()
    
    lista_retorno = []
    
    for c in clientes:
        # Dicionário para cada cliente
        lista_retorno.append({
            "id": c.id_cliente,
            "nome": c.nome,
            "cpf": c.cpf,
            "cidade": c.cidade,
            "flamenguista": c.torce_flamengo,
            "one_piece": c.assiste_one_piece
        })
        
    return jsonify(lista_retorno), 200

@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    # O Flask pega o <id> da URL e o SQLAlchemy busca no banco
    cliente = Cliente.query.get(id)
    
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado."}), 404
        
    dados = request.get_json()
    
    # Atualizamos apenas os campos que vieram no JSON
    # A função .get(chave, valor_padrao) mantém o dado antigo se não enviarem um novo
    cliente.nome = dados.get('nome', cliente.nome)
    cliente.cpf = dados.get('cpf', cliente.cpf)
    cliente.email = dados.get('email', cliente.email)
    cliente.cidade = dados.get('cidade', cliente.cidade)
    cliente.telefone = dados.get('telefone', cliente.telefone)
    cliente.torce_flamengo = dados.get('torce_flamengo', cliente.torce_flamengo)
    cliente.assiste_one_piece = dados.get('assiste_one_piece', cliente.assiste_one_piece)
    
    try:
        db.session.commit()
        return jsonify({"mensagem": f"Dados de {cliente.nome} atualizados com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao atualizar cliente.", "detalhes": str(e)}), 400

@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado."}), 404
        
    try:
        # Apaga o objeto e commita
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({"mensagem": f"Cliente {cliente.nome} (ID: {id}) deletado com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        # se o cliente tiver uma compra registrada:
        # o banco de dados NÃO deixa deletar ele (proteção de chave estrangeira).
        return jsonify({"erro": "Não foi possível deletar o cliente. Verifique se ele possui compras atreladas.", "detalhes": str(e)}), 400