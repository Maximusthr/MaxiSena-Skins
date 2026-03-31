from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Pagamento

pagamentos_bp = Blueprint('pagamentos', __name__)

# Atualizar o status do pagamento
@pagamentos_bp.route('/pagamentos/<int:id>/status', methods=['PATCH'])
def atualizar_status_pagamento(id):
    pagamento = Pagamento.query.get(id)
    
    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado."}), 404
        
    dados = request.get_json()
    novo_status = dados.get('status_confirmacao', '').capitalize() # Deixa a primeira letra maiúscula
    
    status_validos = ['Pendente', 'Confirmado', 'Cancelado']
    
    if novo_status not in status_validos:
        return jsonify({"erro": f"Status inválido. Escolha entre: {', '.join(status_validos)}"}), 400
        
    pagamento.status_confirmacao = novo_status
    
    try:
        db.session.commit()
        return jsonify({
            "mensagem": "Status do pagamento atualizado com sucesso!",
            "forma_pagamento": pagamento.forma_pagamento,
            "novo_status": pagamento.status_confirmacao
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao atualizar pagamento.", "detalhes": str(e)}), 400

# Listar Pagamentos
@pagamentos_bp.route('/pagamentos', methods=['GET'])
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    
    lista_retorno = []
    for p in pagamentos:
        lista_retorno.append({
            "id": p.id_pagamento,
            "forma_pagamento": p.forma_pagamento,
            "status_confirmacao": p.status_confirmacao
        })
        
    return jsonify(lista_retorno), 200

# Atualizar pagamento completo (Status ou Forma)
@pagamentos_bp.route('/pagamentos/<int:id>', methods=['PUT'])
def atualizar_pagamento_completo(id):
    pagamento = Pagamento.query.get(id)
    
    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado."}), 404
        
    dados = request.get_json()
    
    # Validações de alteração do Status
    if 'status_confirmacao' in dados:
        # .capitalize() para não quebrar na validação
        novo_status = str(dados['status_confirmacao']).strip().capitalize()
        status_validos = ['Pendente', 'Confirmado', 'Cancelado']
        
        if novo_status not in status_validos:
            return jsonify({"erro": f"Status inválido. Use: {status_validos}"}), 400
            
        pagamento.status_confirmacao = novo_status

    # Validações de alteração da Forma de Pagamento
    if 'forma_pagamento' in dados:
        nova_forma = str(dados['forma_pagamento']).strip().capitalize()
        formas_validas = ['Cartao', 'Boleto', 'Pix', 'Berries']
        
        if nova_forma not in formas_validas:
             return jsonify({"erro": f"Forma de pagamento inválida. Use: {formas_validas}"}), 400
             
        pagamento.forma_pagamento = nova_forma
        
    # SALVAR NO BANCO
    try:
        db.session.commit()
        return jsonify({
            "mensagem": f"Pagamento ID {pagamento.id_pagamento} atualizado com sucesso!",
            "status_atual": pagamento.status_confirmacao,
            "forma_atual": pagamento.forma_pagamento
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao atualizar o pagamento.", "detalhes": str(e)}), 500