import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.database import db
from src.models import Cliente, Vendedor, Pagamento, Skin, Compra, ItemCompra

from src.clientes import clientes_bp

from src.clientes import clientes_bp
from src.skins import skins_bp

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

# --- ROTAS DE TESTE ---

@app.route('/', methods=['GET'])
def index():
    return jsonify({"mensagem": "API do Mercado CS2 rodando com sucesso!"})

# --- INICIALIZAÇÃO DO BANCO ---
# Este bloco cria as tabelas automaticamente assim que o app rodar pela primeira vez
with app.app_context():
    db.create_all()
    print("Tabelas sincronizadas com sucesso no banco de dados!")

if __name__ == '__main__':
    app.run(debug=True)