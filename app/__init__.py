"""
Application Factory pour Flask
Initialise l'application Flask avec toutes ses extensions
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy import create_engine
from sqlalchemy import exc as sa_exc

# Initialisation des extensions
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    """
    Factory pour créer et configurer l'application Flask
    """
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config['SECRET_KEY'] =  os.getenv('SECRET_KEY', 'fallback_dev_key')

    database_url = os.getenv('DATABASE_URL')

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql://", 1
        )

    # Si une URL est fournie, tenter de se connecter d'abord (timeout court),
    # sinon basculer sur SQLite local pour le développement.
    tried_database_url = None
    if database_url:
        tried_database_url = database_url
        try:
            engine = create_engine(database_url, connect_args={"connect_timeout": 3})
            conn = engine.connect()
            conn.close()
        except sa_exc.OperationalError:
            print(
                "[warning] Connexion à la base distante impossible, bascule vers SQLite local"
            )
            database_url = None
        except Exception:
            print(
                "[warning] Échec connexion DB (non-OperationalError), bascule vers SQLite local"
            )
            database_url = None

    # Fallback vers une base SQLite locale pour le développement
    if not database_url:
        os.makedirs(app.instance_path, exist_ok=True)
        database_path = os.path.join(app.instance_path, 'tasks.db')
        database_url = f"sqlite:///{database_path}"

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation des extensions avec l'application
    db.init_app(app)
    csrf.init_app(app)
    
    # Enregistrement des routes
    from app.routes import main
    app.register_blueprint(main)
    
    # Création des tables de la base de données
    with app.app_context():
        db.create_all()
    
    return app
