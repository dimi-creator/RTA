# 📝 Gestionnaire de Tâches - Application Flask

Une application web complète de gestion de tâches construite avec **Flask** et **Jinja2**, sans framework frontend. Interface moderne avec **Bootstrap 5**.

---

## ✨ Fonctionnalités

### Fonctionnalités de base
- ✅ **Créer** une tâche avec titre, description et date limite (optionnelle)
- ✏️ **Modifier** une tâche existante
- 🗑️ **Supprimer** une tâche
- ☑️ **Marquer** comme complétée ou non complétée
- 📋 **Afficher** la liste de toutes les tâches
- 🔄 **Trier** par date de création, titre, date limite ou statut
- 🔍 **Rechercher** dans les tâches (titre et description)
- 📊 **Statistiques** : Total, En cours, Terminées

### Fonctionnalités bonus
- 🔐 **Authentification** complète (inscription, connexion, déconnexion)
- 👤 **Gestion multi-utilisateurs** (chaque utilisateur a ses propres tâches)
- 🎯 **Filtres** : Toutes / En cours / Terminées
- ⚡ **Action groupée** : Marquer toutes les tâches comme terminées
- ⏰ **Détection des tâches en retard**
- 🎨 **Interface responsive** et moderne
- 🛡️ **Protection CSRF** sur tous les formulaires

---

## 📁 Structure du projet

```
flask_task_manager/
│
├── app/
│   ├── __init__.py           # Factory de l'application
│   ├── models.py             # Modèles de données (User, Task)
│   ├── routes.py             # Routes et vues
│   ├── forms.py              # Formulaires Flask-WTF
│   │
│   ├── templates/
│   │   ├── base.html         # Template de base
│   │   ├── index.html        # Page d'accueil / Liste des tâches
│   │   ├── add_task.html     # Ajouter une tâche
│   │   ├── edit_task.html    # Modifier une tâche
│   │   ├── login.html        # Connexion
│   │   └── register.html     # Inscription
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Styles personnalisés
│   │   └── js/
│   │       └── script.js     # JavaScript léger
│   │
│   └── database.db           # Base de données SQLite (créée automatiquement)
│
├── app.py                    # Point d'entrée de l'application
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation
```

---

## 🚀 Installation et lancement

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étape 1 : Cloner ou télécharger le projet

```bash
cd flask_task_manager
```

### Étape 2 : Créer un environnement virtuel (recommandé)

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Initialiser la base de données

La base de données est créée automatiquement au premier lancement. Pas d'action supplémentaire nécessaire !

### Étape 5 : Lancer l'application

```bash
python app.py
```

Ou avec Flask CLI :

```bash
flask run
```

### Étape 6 : Accéder à l'application

Ouvrez votre navigateur et accédez à :

```
http://127.0.0.1:5000
```

---

## 🎯 Utilisation

### Mode sans authentification
- Accédez directement à la page d'accueil
- Créez, modifiez et supprimez des tâches
- Toutes les tâches sont partagées (pas de séparation par utilisateur)

### Mode avec authentification
1. Cliquez sur **"Inscription"** dans la navigation
2. Créez un compte avec nom d'utilisateur, email et mot de passe
3. Connectez-vous avec vos identifiants
4. Vos tâches sont maintenant privées et liées à votre compte

### Fonctionnalités principales

#### Créer une tâche
1. Cliquez sur **"Nouvelle Tâche"** ou le bouton **"+"**
2. Remplissez le titre (obligatoire)
3. Ajoutez une description (optionnelle)
4. Définissez une date limite (optionnelle)
5. Cliquez sur **"Enregistrer"**

#### Modifier une tâche
1. Cliquez sur **"Modifier"** sur une tâche
2. Modifiez les informations
3. Sauvegardez les changements

#### Marquer comme terminée
- Cliquez sur le cercle ⭕ à gauche de la tâche
- Ou utilisez le bouton dans la page de modification

#### Supprimer une tâche
- Cliquez sur **"Supprimer"** (confirmation demandée)

#### Rechercher et filtrer
- Utilisez la barre de recherche en haut
- Filtrez par statut : **Toutes** / **En cours** / **Terminées**
- Triez par : Date de création, Titre, Date limite, Statut

#### Actions groupées
- Cliquez sur **"Tout marquer comme terminé"** pour terminer toutes les tâches en attente

---

## 🛠️ Technologies utilisées

### Backend
- **Flask 3.0** - Framework web Python
- **Flask-SQLAlchemy** - ORM pour la base de données
- **Flask-WTF** - Gestion des formulaires et CSRF
- **SQLite** - Base de données légère
- **Werkzeug** - Hachage de mots de passe

### Frontend
- **Jinja2** - Moteur de templates
- **Bootstrap 5.3** - Framework CSS
- **Bootstrap Icons** - Icônes
- **JavaScript Vanilla** - Améliorations UX légères

---

## 📊 Modèles de données

### User (Utilisateur)
```python
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password: String (Hashed)
- created_at: DateTime
- tasks: Relationship (One-to-Many)
```

### Task (Tâche)
```python
- id: Integer (Primary Key)
- title: String (Required)
- description: Text (Optional)
- completed: Boolean (Default: False)
- created_at: DateTime
- due_date: DateTime (Optional)
- user_id: Integer (Foreign Key)
```

---

## 🔒 Sécurité

- ✅ **Protection CSRF** sur tous les formulaires (Flask-WTF)
- ✅ **Hachage des mots de passe** avec Werkzeug
- ✅ **Validation des formulaires** côté serveur
- ✅ **Sessions sécurisées** avec clé secrète
- ✅ **Permissions** : Les utilisateurs ne peuvent modifier que leurs propres tâches

---

## 🎨 Personnalisation

### Modifier les couleurs
Éditez `/app/static/css/style.css` :

```css
:root {
    --primary-color: #0d6efd;  /* Couleur principale */
    --success-color: #198754;  /* Succès */
    --warning-color: #ffc107;  /* Avertissement */
    --danger-color: #dc3545;   /* Danger */
}
```

### Modifier la clé secrète
Dans `/app/__init__.py`, changez :

```python
app.config['SECRET_KEY'] = 'votre-nouvelle-cle-secrete'
```

---

## 📝 Notes importantes

### Base de données
- La base de données SQLite `database.db` est créée automatiquement dans `/app/`
- Pour réinitialiser : Supprimez `database.db` et relancez l'application

### Mode développement vs Production
- Le mode `debug=True` est activé pour le développement
- **Pour la production**, désactivez le mode debug et utilisez un serveur WSGI (Gunicorn, uWSGI)

### Limitations
- SQLite est adapté pour le développement, utilisez PostgreSQL/MySQL en production
- Pas de pagination (toutes les tâches sont chargées)
- Pas de récupération de mot de passe (fonctionnalité bonus à implémenter)

---

## 🐛 Dépannage

### Erreur : "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erreur : "Address already in use"
Un autre processus utilise le port 5000. Changez le port :
```python
app.run(debug=True, port=5001)
```

### Base de données corrompue
Supprimez `app/database.db` et relancez l'application.

---

## 📄 Licence

Ce projet est fourni à titre éducatif. Vous êtes libre de l'utiliser et de le modifier.

---

## 👨‍💻 Auteur

Créé avec ❤️ en utilisant Flask et Bootstrap

---

## 🚀 Améliorations futures possibles

- [ ] Pagination des tâches
- [ ] Catégories et tags pour les tâches
- [ ] Priorités (haute, moyenne, basse)
- [ ] Notifications par email
- [ ] Export PDF/CSV
- [ ] Mode sombre
- [ ] API REST optionnelle
- [ ] Tests unitaires
- [ ] Déploiement Docker

---

**Bon développement ! 🎉**
