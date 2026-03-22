from src.database import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    cpf = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    torce_flamengo = db.Column(db.Boolean, default=False)
    assiste_one_piece = db.Column(db.Boolean, default=False)

    # Cliente tem várias compras
    compras = db.relationship('Compra', backref='cliente', lazy=True)

class Vendedor(db.Model):
    __tablename__ = 'vendedores'
    
    id_vendedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)

    # Vendedor faz várias vendas (aponta para tabela compra)
    compras = db.relationship('Compra', backref='vendedor', lazy=True)

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    
    id_pagamento = db.Column(db.Integer, primary_key=True)
    forma_pagamento = db.Column(db.String(20), nullable=False)
    status_confirmacao = db.Column(db.String(20), nullable=False)

    # Um pagamento pertence a uma compra (1:1)
    compra = db.relationship('Compra', backref='pagamento', uselist=False, lazy=True)

class Skin(db.Model):
    __tablename__ = 'skins'
    
    id_skins = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(40), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(40), nullable=False)
    raridade = db.Column(db.String(40), nullable=False)
    pattern = db.Column(db.Integer, nullable=False)
    wear_rating = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    fabricado_em_mari = db.Column(db.Boolean, default=False)

    # Uma skin pode estar em vários itens de compra
    itens_compra = db.relationship('ItemCompra', backref='skin', lazy=True)

class Compra(db.Model):
    __tablename__ = 'compras'
    
    id_compra = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('vendedores.id_vendedor'), nullable=False)
    id_pagamento = db.Column(db.Integer, db.ForeignKey('pagamentos.id_pagamento'), nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False)

    # Uma compra tem vários itens
    itens = db.relationship('ItemCompra', backref='compra_associada', lazy=True, cascade="all, delete-orphan")

class ItemCompra(db.Model):
    __tablename__ = 'itens_compra'
    
    id_item = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compras.id_compra', ondelete='CASCADE'), nullable=False)
    id_skins = db.Column(db.Integer, db.ForeignKey('skins.id_skins'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)