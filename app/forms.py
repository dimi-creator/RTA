"""
Formulaires Flask-WTF
Gère la validation et la protection CSRF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class TaskForm(FlaskForm):
    """
    Formulaire pour créer/modifier une tâche
    """
    title = StringField('Titre', 
                       validators=[DataRequired(message='Le titre est obligatoire'), 
                                 Length(max=200, message='Le titre est trop long')])
    
    description = TextAreaField('Description', 
                               validators=[Length(max=1000, message='La description est trop longue')])
    
    due_date = DateTimeLocalField('Date limite (optionnelle)', 
                                 format='%Y-%m-%dT%H:%M',
                                 validators=[Optional()])
    
    submit = SubmitField('Enregistrer')


class SearchForm(FlaskForm):
    """
    Formulaire de recherche
    """
    search = StringField('Rechercher', validators=[Length(max=100)])


class LoginForm(FlaskForm):
    """
    Formulaire de connexion
    """
    username = StringField('Nom d\'utilisateur', 
                          validators=[DataRequired(message='Le nom d\'utilisateur est obligatoire')])
    
    password = PasswordField('Mot de passe', 
                           validators=[DataRequired(message='Le mot de passe est obligatoire')])
    
    submit = SubmitField('Se connecter')


class RegisterForm(FlaskForm):
    """
    Formulaire d'inscription
    """
    username = StringField('Nom d\'utilisateur', 
                          validators=[
                              DataRequired(message='Le nom d\'utilisateur est obligatoire'),
                              Length(min=3, max=80, message='Entre 3 et 80 caractères')
                          ])
    
    email = StringField('Email', 
                       validators=[
                           DataRequired(message='L\'email est obligatoire'),
                           Email(message='Email invalide')
                       ])
    
    password = PasswordField('Mot de passe', 
                           validators=[
                               DataRequired(message='Le mot de passe est obligatoire'),
                               Length(min=6, message='Au moins 6 caractères')
                           ])
    
    confirm_password = PasswordField('Confirmer le mot de passe', 
                                   validators=[
                                       DataRequired(message='Veuillez confirmer le mot de passe'),
                                       EqualTo('password', message='Les mots de passe ne correspondent pas')
                                   ])
    
    submit = SubmitField('S\'inscrire')
