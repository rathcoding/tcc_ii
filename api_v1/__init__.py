import os
from flask import Flask
from flask_cors import CORS

from .extensions import db, migrate, scheduler
from .routes import identifica
from .services import carga_cnh, treina_modelos

# Esta função é chamada quando iniciado o servidor.
def create_app():
    app = Flask(__name__)
    CORS(app)

    # """
    # BANCO DE DADOS:
    # """
    print("Conectando ao banco de dados...", end=' ')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    print("OK")

    # """
    # MIGRATIONS:
    # """
    print("Iniciando migrações...", end=' ')
    migrate.init_app(app, db)
    print("OK")

    # """
    # ROTAS:
    # """
    print("Registrando rotas...", end=' ')
    app.register_blueprint(hello)
    app.register_blueprint(identifica)
    print("OK")

    # """
    # SERVIÇOS DE CARGA DE IMAGENS E TREINAMENTO DE MODELOS:
    # """
    print("Iniciando scheduler...", end=' ')
    scheduler.init_app(app)
    scheduler.api_enabled = False
    scheduler.start()
    print("OK")


    return app
