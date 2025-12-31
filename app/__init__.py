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
import logging

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

    # Par défaut, utiliser SQLite local (assure que SQLALCHEMY_DATABASE_URI
    # est toujours défini avant d'initialiser les extensions)
    os.makedirs(app.instance_path, exist_ok=True)
    database_path = os.path.join(app.instance_path, 'tasks.db')
    default_sqlite = f"sqlite:///{database_path}"
    app.config['SQLALCHEMY_DATABASE_URI'] = default_sqlite

    # Puis, si une URL distante est fournie, tenter une connexion rapide et
    # remplacer la config si la connexion réussit.
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    if database_url:
        try:
            engine = create_engine(database_url, connect_args={"connect_timeout": 3})
            conn = engine.connect()
            conn.close()
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
            logging.getLogger(__name__).info('Connected to remote DB; using DATABASE_URL')
        except sa_exc.OperationalError:
            logging.getLogger(__name__).warning(
                'Connexion à la base distante impossible, utilisation de SQLite local'
            )
        except Exception:
            logging.getLogger(__name__).warning(
                'Échec connexion DB (non-OperationalError), utilisation de SQLite local'
            )
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
