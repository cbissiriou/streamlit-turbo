# 🚀 StreamlitTurbo PRO

> **Template professionnel production-ready pour applications Streamlit**
> **Économise des jours de développement sur chaque projet** ⏱️

Template enterprise avec authentification, base de données, monitoring, CI/CD et bien plus.

## ✨ Fonctionnalités PRO

### 🔐 Authentification
- ✅ Google OAuth natif (via `st.login()`)
- ✅ Gestion des sessions sécurisée
- ✅ Système de rôles et permissions (user, admin)
- ✅ Décorateurs d'authentification (`@require_auth`, `@require_role`)

### 🗄️ Base de Données
- ✅ SQLModel (ORM moderne basé sur Pydantic)
- ✅ Support SQLite (dev) et PostgreSQL (prod)
- ✅ Migrations Alembic intégrées
- ✅ Modèles prêts (User, ActivityLog, DataEntry)

### 📊 Monitoring & Analytics
- ✅ Logging structuré (structlog)
- ✅ Tracking des actions utilisateurs
- ✅ Analytics intégrés
- ✅ Dashboard admin avec statistiques

### 🚀 DevOps & CI/CD
- ✅ GitHub Actions (tests + deploy automatique)
- ✅ Docker + docker-compose
- ✅ Pre-commit hooks (Ruff, security checks)
- ✅ Tests automatisés (pytest + coverage)

### 🎨 Interface Moderne
- ✅ Navigation top moderne (sans sidebar)
- ✅ 4 thèmes professionnels
- ✅ Composants réutilisables (charts Plotly)
- ✅ Design responsive

### 📦 Outils Modernes
- ✅ **uv** - Gestionnaire de dépendances ultra-rapide
- ✅ **just** - Task runner avec 25+ commandes
- ✅ **Ruff** - Linter et formatter Python moderne
- ✅ **pyproject.toml** - Configuration centralisée

## 🚦 Démarrage Rapide en 5 Minutes

### Prérequis
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) installé (`pip install uv`)
- [just](https://github.com/casey/just) installé (optionnel mais recommandé)
- [Copier](https://copier.readthedocs.io/) installé (`pip install copier` ou `uv tool install copier`)
- Compte GitHub (pour héberger votre projet)

### Installation depuis ZIP (recommandé)

**StreamlitTurbo PRO est distribué au format ZIP pour vous permettre de créer votre propre repository privé.**

```bash
# 1. Télécharger le ZIP depuis votre espace formation
# Lien fourni dans votre accès à la formation

# 2. Dézipper l'archive
unzip streamlit-turbo-pro.zip
cd streamlit-turbo-pro

# 3. Créer un nouveau repository GitHub
# Aller sur https://github.com/new
# Créer un repo (public ou privé selon votre choix)
# NE PAS initialiser avec README, .gitignore ou licence (déjà inclus)

# 4. Initialiser git et pousser vers votre repo
git init
git add .
git commit -m "Initial commit - StreamlitTurbo PRO"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/VOTRE-REPO.git
git push -u origin main

# 5. Utiliser Copier pour créer votre projet à partir de ce template
cd ..
copier copy streamlit-turbo-pro mon-nouveau-projet

# Copier vous posera quelques questions :
# - Nom du projet
# - Description
# - Votre nom d'auteur
# - Votre email
# etc.

# 6. Entrer dans votre nouveau projet
cd mon-nouveau-projet

# 7. Setup automatique complet
just setup

# 8. Lancer l'application
just run
```

**Alternative : Cloner directement depuis votre repo GitHub**

Une fois que vous avez poussé le template sur GitHub (étapes 1-4 ci-dessus) :

```bash
# 1. Cloner votre repo template
git clone https://github.com/VOTRE-USERNAME/streamlit-turbo-pro.git

# 2. Utiliser Copier
copier copy streamlit-turbo-pro mon-nouveau-projet
cd mon-nouveau-projet

# 3. Setup et lancement
just setup
just run
```

**Installation Simple (sans Copier)**

Si vous ne voulez pas utiliser Copier :

```bash
# 1. Dézipper et entrer dans le dossier
unzip streamlit-turbo-pro.zip
cd streamlit-turbo-pro

# 2. Setup automatique complet (avec just)
just setup

# 3. Lancer l'application
just run
```

**Alternative sans just :**
```bash
# Setup manuel
uv venv --python 3.12
uv sync

# Lancer l'app
uv run streamlit run main.py
```

L'application sera disponible sur `http://localhost:8501`

### Configuration de l'authentification (optionnel)

Pour activer l'authentification Google OAuth :

1. Créer un projet sur [Google Cloud Console](https://console.cloud.google.com)
2. Configurer OAuth 2.0 credentials
3. Copier `.streamlit/secrets.toml.example` vers `.streamlit/secrets.toml`
4. Remplir avec vos credentials Google

Voir la [documentation complète](https://docs.streamlit.io/develop/tutorials/authentication/google)

## 📁 Structure du Projet

```
ultimate-streamlit-template/
├── main.py                           # Point d'entrée (navigation moderne)
├── src/streamlit_template/           # Code source
│   ├── auth/                         # 🔐 Authentification
│   │   ├── session.py                # Gestion sessions
│   │   └── decorators.py             # @require_auth, @require_role
│   ├── database/                     # 🗄️ Base de données
│   │   ├── models.py                 # Modèles SQLModel
│   │   ├── engine.py                 # Connexion DB
│   │   └── migrations/               # Alembic migrations
│   ├── monitoring/                   # 📊 Monitoring
│   │   ├── logger.py                 # Logging structuré
│   │   └── analytics.py              # Tracking utilisateurs
│   ├── components/                   # 🎨 Composants UI
│   │   ├── charts.py                 # Graphiques Plotly
│   │   ├── header.py, footer.py      # Layout
│   │   └── ...
│   ├── pages/                        # 📄 Pages app
│   │   ├── home.py                   # Accueil
│   │   ├── analytics.py              # Dashboard
│   │   ├── settings.py               # Paramètres
│   │   └── admin.py                  # Admin (PRO)
│   ├── core/                         # ⚙️ Core
│   └── utils/                        # 🛠️ Utilitaires
├── tests/                            # ✅ Tests
│   ├── unit/                         # Tests unitaires
│   ├── integration/                  # Tests d'intégration
│   └── conftest.py                   # Fixtures pytest
├── .github/workflows/                # 🤖 CI/CD
│   ├── ci.yml                        # Tests automatiques
│   └── deploy.yml                    # Déploiement auto
├── docker/                           # 🐳 Docker
│   ├── Dockerfile                    # Image production
│   └── docker-compose.yml            # Stack complète
├── .streamlit/                       # ⚙️ Config Streamlit
│   ├── config.toml                   # 4 thèmes
│   └── secrets.toml.example          # Template secrets
├── data/                             # 📊 Données
├── justfile                          # 📋 Task runner
├── pyproject.toml                    # 📦 Configuration
├── .pre-commit-config.yaml           # 🔍 Hooks
└── requirements.txt                  # 📥 Déploiement
```

## ⚡ Commandes Just

Le template inclut un `justfile` avec 25+ commandes pour automatiser les tâches :

### Commandes Principales
```bash
just setup              # Setup complet du projet
just run                # Lancer l'application
just dev                # Mode développement (auto-reload)
just help               # Voir toutes les commandes
```

### Qualité du Code
```bash
just format             # Formater avec Ruff
just lint               # Vérifier la qualité
just check              # Format + Lint
just typecheck          # Vérification des types
just pre-commit         # Lancer pre-commit hooks
```

### Tests
```bash
just test               # Tous les tests
just test-cov           # Tests avec coverage HTML
just test-unit          # Tests unitaires uniquement
just test-integration   # Tests d'intégration
```

### Base de Données
```bash
just db-migrate "msg"   # Créer une migration
just db-upgrade         # Appliquer les migrations
just db-downgrade       # Revenir en arrière
just db-history         # Voir l'historique
```

### Docker
```bash
just docker-build       # Build l'image
just docker-up          # Lancer stack complète (App + PostgreSQL + Adminer)
just docker-down        # Arrêter les conteneurs
just docker-logs        # Voir les logs
```

### Dépendances
```bash
just add PACKAGE        # Ajouter une dépendance
just add-dev PACKAGE    # Ajouter une dépendance de dev
just sync               # Synchroniser
just requirements       # Générer requirements.txt
```

## 🧩 Pages Disponibles

- **🏠 Accueil** - Page publique + dashboard utilisateur (authentification optionnelle)
- **📊 Analytics** - Visualisations Plotly, KPIs, export données (authentification requise)
- **⚙️ Paramètres** - Profil utilisateur, préférences, informations (authentification requise)
- **🛡️ Admin** - Gestion utilisateurs, stats globales, base de données (rôle admin requis)

## 🚀 Déploiement

### Sur Streamlit Community Cloud

1. **Préparez le déploiement**
   ```bash
   just requirements
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Déployez sur Streamlit Cloud**
   - Connectez votre repo GitHub sur [share.streamlit.io](https://share.streamlit.io)
   - Sélectionnez `main.py` comme point d'entrée
   - Configurez les secrets dans l'interface Streamlit Cloud
   - Déployez !

### Avec Docker

```bash
# Build et lancer
just docker-build
just docker-up

# L'app sera disponible sur http://localhost:8501
# PostgreSQL sur localhost:5432
# Adminer (DB UI) sur http://localhost:8080
```

### Variables d'Environnement / Secrets

Configurez dans `.streamlit/secrets.toml` :
- Credentials Google OAuth
- URL base de données
- Configuration monitoring
- Liste des emails admin

Voir `.streamlit/secrets.toml.example` pour le template complet.

## 🧪 Tests

Suite de tests complète avec pytest :

```bash
# Lancer tous les tests avec coverage
just test-cov

# Tests unitaires (auth, database, monitoring)
just test-unit

# Tests d'intégration (pages)
just test-integration
```

**Coverage actuel :** Tests pour auth, database, monitoring, et pages.

## 🎨 Thèmes

4 thèmes professionnels disponibles dans `.streamlit/config.toml` :

- **Blue (Corporate)** - Thème professionnel par défaut
- **Dark (Spotify)** - Thème sombre moderne
- **Light (Eclair)** - Thème clair élégant
- **Green (Nature)** - Thème nature moderne

Décommentez le thème désiré dans le fichier de configuration.

## 📚 Documentation

- **README.md** - Ce fichier (guide complet)
- **CLAUDE.md** - Guide pour Claude Code
- **justfile** - Liste des commandes (`just help`)
- [Documentation Streamlit](https://docs.streamlit.io)
- [Documentation uv](https://github.com/astral-sh/uv)
- [Documentation just](https://github.com/casey/just)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push sur la branche (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

## 📞 Support & Contact

- 📧 **Email** : gael.penessot@gmail.com
- 💼 **LinkedIn** : [Gaël Penessot](https://www.linkedin.com/in/gael-penessot/)
- 🐛 **Issues** : [GitHub Issues](https://github.com/gpenessot/ultimate-streamlit-template/issues)

## 📝 Licence

MIT License - Libre d'utilisation et de modification

**Créé avec ❤️ par [Gaël Penessot](https://www.mes-formations-data.fr)**

---

⭐ **Ce template vous aide ?** Donnez-lui une étoile sur GitHub !

## 📦 Version

**v1.0.0** - StreamlitTurbo PRO - Production Ready
