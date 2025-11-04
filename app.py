"""
Point d'entrée de l'application Flask
Lance le serveur de développement
"""
from app import create_app

# Création de l'application
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Gestionnaire de Tâches - Application Flask")
    print("=" * 60)
    print("\n📍 Accédez à l'application sur : http://127.0.0.1:5000")
    print("📝 Pour arrêter le serveur : Ctrl + C")
    print("\nℹ️  Mode développement activé avec rechargement automatique\n")
    print("=" * 60)
    
    # Lancement du serveur en mode développement
    app.run(debug=True, host='0.0.0.0', port=5000)
