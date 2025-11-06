/**
 * Script JavaScript pour améliorer l'expérience utilisateur
 * Fonctionnalités légères sans framework
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================================
    // Auto-fermeture des messages flash
    // ==================================
    const alerts = document.querySelectorAll('.alert:not(.alert-dismissible)');
    alerts.forEach(alert => {
        // Fermer automatiquement après 5 secondes
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    
    // ==================================
    // Confirmation avant suppression
    // ==================================
    const deleteButtons = document.querySelectorAll('button[onclick*="confirm"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    
    // ==================================
    // Animation au survol des cartes
    // ==================================
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
    
    
    // ==================================
    // Validation de formulaire côté client
    // ==================================
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Vérifier les champs requis
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                
            }
        });
    });
    
    
    // ==================================
    // Focus automatique sur le premier champ
    // ==================================
    const firstInput = document.querySelector('form input[type="text"], form input[type="email"]');
    if (firstInput) {
        firstInput.focus();
    }
    
    
    // ==================================
    // Compteur de caractères pour textarea
    // ==================================
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('small');
            counter.className = 'form-text text-muted';
            counter.textContent = `0 / ${maxLength} caractères`;
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                const length = this.value.length;
                counter.textContent = `${length} / ${maxLength} caractères`;
                
                if (length > maxLength * 0.9) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            });
        }
    });
    
    
    // ==================================
    // Smooth scroll pour les ancres
    // ==================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    
    // ==================================
    // Afficher le nombre de tâches filtrées
    // ==================================
    const taskCount = document.querySelectorAll('.task-card').length;
    const countBadge = document.querySelector('.badge.bg-primary');
    if (countBadge && taskCount > 0) {
        countBadge.textContent = taskCount;
    }
    
    
    // ==================================
    // Recherche instantanée (optionnel)
    // ==================================
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase();
            
            // Délai de 300ms avant de filtrer
            searchTimeout = setTimeout(() => {
                const cards = document.querySelectorAll('.task-card');
                cards.forEach(card => {
                    const title = card.querySelector('.card-title').textContent.toLowerCase();
                    const description = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
                    
                    if (title.includes(query) || description.includes(query)) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }, 300);
        });
    }
    
    
    // ==================================
    // Tooltip Bootstrap (si nécessaire)
    // ==================================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    
    // ==================================
    // Console log pour debug
    // ==================================
    console.log('✅ Application de gestion de tâches chargée avec succès !');
    console.log(`📊 ${taskCount} tâche(s) affichée(s)`);
});
