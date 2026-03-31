import os
from flask import Flask, jsonify
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

# Cria as tabelas automaticamente assim que o app rodar pela primeira vez
with app.app_context():
    db.create_all()               # Cria as tabelas se não existirem
    popular_banco_se_vazio(db)    # Injeta os dados se estiver vazio

if __name__ == '__main__':
    app.run(debug=True)