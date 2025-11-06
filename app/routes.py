"""
Routes et vues de l'application
Gère toutes les interactions utilisateur via des vues serveur
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task, User
from app.forms import TaskForm, LoginForm, RegisterForm, SearchForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

main = Blueprint('main', __name__)

def login_required(f):
    """
    Décorateur pour protéger les routes nécessitant une authentification
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function


@main.route('/')
def index():
    """
    Page d'accueil - affiche toutes les tâches
    Supporte le tri et la recherche
    """
    # Récupération des paramètres de recherche et tri
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'created_at')
    filter_status = request.args.get('status', 'all')
    
    # Construction de la requête de base
    query = Task.query
    
    # Filtrage par utilisateur si connecté
    if 'user_id' in session:
        query = query.filter_by(user_id=session['user_id'])
    else:
        # Mode sans authentification : afficher toutes les tâches sans user_id
        query = query.filter_by(user_id=None)
    
    # Recherche par titre ou description
    if search_query:
        query = query.filter(
            db.or_(
                Task.title.contains(search_query),
                Task.description.contains(search_query)
            )
        )
    
    # Filtrage par statut
    if filter_status == 'completed':
        query = query.filter_by(completed=True)
    elif filter_status == 'pending':
        query = query.filter_by(completed=False)
    
    # Tri des résultats
    if sort_by == 'title':
        query = query.order_by(Task.title)
    elif sort_by == 'due_date':
        query = query.order_by(Task.due_date.desc().nullslast())
    elif sort_by == 'status':
        query = query.order_by(Task.completed, Task.created_at.desc())
    else:  # par défaut : created_at
        query = query.order_by(Task.created_at.desc())
    
    tasks = query.all()
    
    # Formulaire de recherche
    search_form = SearchForm()
    
    return render_template('index.html', 
                         tasks=tasks, 
                         search_query=search_query,
                         sort_by=sort_by,
                         filter_status=filter_status,
                         search_form=search_form)


@main.route('/add', methods=['GET', 'POST'])
def add_task():
    """
    Ajouter une nouvelle tâche
    """
    form = TaskForm()
    
    if form.validate_on_submit():
        # Création de la nouvelle tâche
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            user_id=session.get('user_id')  # None si pas connecté
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Tâche ajoutée avec succès !', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_task.html', form=form)


@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    Modifier une tâche existante
    """
    task = Task.query.get_or_404(task_id)
    
    # Vérification des permissions si authentification activée
    if 'user_id' in session and task.user_id != session['user_id']:
        flash('Vous n\'avez pas la permission de modifier cette tâche.', 'danger')
        return redirect(url_for('main.index'))
    
    form = TaskForm(obj=task)
    
    if isinstance(task.due_date, str):
        try:
            task.due_date = datetime.fromisoformat(task.due_date)
        except ValueError:
            task.due_date = None

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data

        db.session.commit()
        
        flash('Tâche mise à jour avec succès !', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit_task.html', form=form, task=task)


@main.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Supprimer une tâche
    """
    task = Task.query.get_or_404(task_id)
    
    # Vérification des permissions si authentification activée
    if 'user_id' in session and task.user_id != session['user_id']:
        flash('Vous n\'avez pas la permission de supprimer cette tâche.', 'danger')
        return redirect(url_for('main.index'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Tâche supprimée avec succès !', 'success')
    return redirect(url_for('main.index'))


@main.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """
    Basculer le statut d'une tâche (complétée/non complétée)
    """
    task = Task.query.get_or_404(task_id)
    
    # Vérification des permissions si authentification activée
    if 'user_id' in session and task.user_id != session['user_id']:
        flash('Vous n\'avez pas la permission de modifier cette tâche.', 'danger')
        return redirect(url_for('main.index'))
    
    task.completed = not task.completed
    db.session.commit()
    
    status = 'complétée' if task.completed else 'marquée comme non complétée'
    flash(f'Tâche {status} !', 'success')
    
    return redirect(url_for('main.index'))


@main.route('/complete-all', methods=['POST'])
def complete_all_tasks():
    """
    Marquer toutes les tâches comme complétées
    """
    if 'user_id' in session:
        tasks = Task.query.filter_by(user_id=session['user_id'], completed=False).all()
    else:
        tasks = Task.query.filter_by(user_id=None, completed=False).all()
    
    for task in tasks:
        task.completed = True
    
    db.session.commit()
    
    flash(f'{len(tasks)} tâche(s) marquée(s) comme complétée(s) !', 'success')
    return redirect(url_for('main.index'))


# ========== Routes d'authentification (BONUS) ==========

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
    Inscription d'un nouvel utilisateur
    """
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Vérification si l'utilisateur existe déjà
        existing_user = User.query.filter(
            db.or_(
                User.username == form.username.data,
                User.email == form.email.data
            )
        ).first()
        
        if existing_user:
            flash('Ce nom d\'utilisateur ou email existe déjà.', 'danger')
            return render_template('register.html', form=form)
        
        # Création du nouvel utilisateur
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Connexion d'un utilisateur
    """
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bienvenue, {user.username} !', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    """
    Déconnexion de l'utilisateur
    """
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))
