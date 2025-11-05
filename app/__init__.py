"""
Application Factory pour Flask
Initialise l'application Flask avec toutes ses extensions
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

# Initialisation des extensions
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    """
    Factory pour créer et configurer l'application Flask
    """
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config['SECRET_KEY'] = 'votre-cle-secrete-super-securisee-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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
