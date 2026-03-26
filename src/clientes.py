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