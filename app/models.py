"""
Modèles de données pour l'application
Définit la structure de la base de données
"""
from app import db
from datetime import datetime

class User(db.Model):
    """
    Modèle pour les utilisateurs
    Gère l'authentification et les relations avec les tâches
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec les tâches
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    """
    Modèle pour les tâches
    Stocke toutes les informations relatives à une tâche
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Clé étrangère vers l'utilisateur (optionnel si authentification activée)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def is_overdue(self):
        """
        Vérifie si la tâche est en retard
        """
        if self.due_date and not self.completed:
            return datetime.utcnow() > self.due_date
        return False
