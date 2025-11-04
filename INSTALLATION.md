# 🚀 Guide d'Installation Rapide

## Installation en 5 minutes

### 1️⃣ Prérequis
- Python 3.8 ou supérieur installé
- pip (gestionnaire de paquets Python)

Vérifiez votre version :
```bash
python --version
pip --version
```

---

### 2️⃣ Télécharger le projet

Téléchargez et décompressez le dossier `flask_task_manager` ou clonez-le depuis votre source.

---

### 3️⃣ Créer un environnement virtuel (RECOMMANDÉ)

**Sur Windows :**
```bash
cd flask_task_manager
python -m venv venv
venv\Scripts\activate
```

**Sur Linux/Mac :**
```bash
cd flask_task_manager
python3 -m venv venv
source venv/bin/activate
```

Vous verrez `(venv)` apparaître dans votre terminal.

---

### 4️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

Cette commande installera :
- Flask 3.0
- Flask-SQLAlchemy
- Flask-WTF
- WTForms
- email-validator

---

### 5️⃣ Lancer l'application

**Méthode 1 (recommandée) :**
```bash
python app.py
```

**Méthode 2 (avec Flask CLI) :**
```bash
flask run
```

---

### 6️⃣ Accéder à l'application

Ouvrez votre navigateur et allez sur :
```
http://127.0.0.1:5000
```

🎉 **C'est terminé !** Vous pouvez maintenant créer vos tâches.

---

## 🔄 Arrêter le serveur

Dans le terminal où le serveur tourne, appuyez sur :
```
Ctrl + C
```

---

## 🗄️ Base de données

La base de données SQLite est créée automatiquement dans :
```
flask_task_manager/app/database.db
```

**Pour réinitialiser la base de données :**
1. Arrêtez le serveur (Ctrl + C)
2. Supprimez le fichier `app/database.db`
3. Relancez l'application

---

## ❓ Problèmes courants

### Erreur : "ModuleNotFoundError: No module named 'flask'"
**Solution :** Vous n'avez pas installé les dépendances
```bash
pip install -r requirements.txt
```

### Erreur : "Address already in use" (Port 5000 occupé)
**Solution :** Changez le port dans `app.py` :
```python
app.run(debug=True, port=5001)  # Utilisez 5001 au lieu de 5000
```

### Erreur : "Permission denied" (Linux/Mac)
**Solution :** Utilisez `python3` au lieu de `python`
```bash
python3 app.py
```

### L'environnement virtuel ne s'active pas sur Windows
**Solution :** Autorisez l'exécution de scripts PowerShell :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📱 Mode sans authentification

Vous pouvez utiliser l'application **sans créer de compte** :
1. Allez directement sur http://127.0.0.1:5000
2. Créez vos tâches
3. Toutes les tâches sont visibles par tous

## 🔐 Mode avec authentification

Pour avoir vos tâches privées :
1. Cliquez sur **"Inscription"** dans le menu
2. Créez un compte
3. Connectez-vous
4. Vos tâches sont maintenant privées !

---

## 🎓 Premiers pas

### Créer votre première tâche
1. Cliquez sur **"Nouvelle Tâche"**
2. Entrez un titre (ex: "Faire les courses")
3. Ajoutez une description (optionnel)
4. Définissez une date limite (optionnel)
5. Cliquez sur **"Enregistrer"**

### Marquer une tâche comme terminée
Cliquez sur le cercle ⭕ à gauche de la tâche. Il deviendra vert ✅.

### Rechercher une tâche
Utilisez la barre de recherche en haut de la page d'accueil.

### Filtrer les tâches
Cliquez sur :
- **"Toutes"** : Toutes les tâches
- **"En cours"** : Seulement les tâches non terminées
- **"Terminées"** : Seulement les tâches complétées

---

## 🎨 Personnalisation

### Changer les couleurs
Éditez `app/static/css/style.css` ligne 9-13 :
```css
:root {
    --primary-color: #0d6efd;  /* Couleur principale */
    --success-color: #198754;  /* Succès */
    --warning-color: #ffc107;  /* Avertissement */
    --danger-color: #dc3545;   /* Danger */
}
```

### Changer le titre de l'application
Éditez `app/templates/base.html` ligne 30 :
```html
<a class="navbar-brand" href="{{ url_for('main.index') }}">
    <i class="bi bi-check2-square"></i> Votre Titre Personnalisé
</a>
```

---

## 📚 Documentation complète

Pour plus d'informations, consultez le fichier `README.md`.

---

**Besoin d'aide ?** Consultez la section **Dépannage** dans le README.md

**Bon développement ! 🚀**
