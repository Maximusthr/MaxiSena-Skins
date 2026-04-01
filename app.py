import os
from flask import Flask, request, jsonify
from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.seed import popular_banco_se_vazio

from src.database import db
from src.models import Cliente, Vendedor, Pagamento, Skin, Compra, ItemCompra

from src.clientes import clientes_bp

from src.clientes import clientes_bp
from src.skins import skins_bp
from src.vendedores import vendedores_bp
from src.compras import compras_bp
from src.pagamentos import pagamentos_bp 

load_dotenv()

app = Flask(__name__)

# Conexão com o banco com a URL do .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Vincula Flask ao bd
db.init_app(app)

# Flask-Migrate (gerenciar futuras alterações nas tabelas)
migrate = Migrate(app, db)

# blueprint no flask
app.register_blueprint(clientes_bp)
app.register_blueprint(skins_bp)
app.register_blueprint(vendedores_bp)
app.register_blueprint(pagamentos_bp)
app.register_blueprint(compras_bp)


@app.route('/', methods=['GET'])
def pagina_inicial():
    # O Flask vai procurar automaticamente dentro da pasta /templates
    return render_template('index.html')

#@app.route('/', methods=['GET'])
#def index():
    #return jsonify({"mensagem": "API do Mercado CS2 rodando com sucesso!"})

# Cria as tabelas automaticamente
with app.app_context():
    db.create_all()               
    popular_banco_se_vazio(db)    

@app.route('/login', methods=['POST'])
def fazer_login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')
    tipo_conta = dados.get('tipo')

    if not email or not senha or not tipo_conta:
        return jsonify({"erro": "Email, senha e tipo de conta são obrigatórios."}), 400

    if tipo_conta == 'cliente':
        usuario = Cliente.query.filter_by(email=email, senha=senha).first()
        if usuario:
            return jsonify({
                "mensagem": "Login aprovado!",
                "id": usuario.id_cliente,
                "nome": usuario.nome,
                "cpf": usuario.cpf,
                "role": "cliente"
            }), 200

    elif tipo_conta == 'vendedor':
        usuario = Vendedor.query.filter_by(email=email, senha=senha).first()
        if usuario:
            return jsonify({
                "mensagem": "Login admin aprovado!",
                "id": usuario.id_vendedor,
                "nome": usuario.nome,
                "role": "vendedor"
            }), 200

    return jsonify({"erro": "Credenciais inválidas!"}), 401

if __name__ == '__main__':
    app.run(debug=True)