# Déploiement en Production

Le projet Prisme est configuré pour être déployé facilement sur une plateforme cloud (PaaS) comme **Render**, **Heroku** ou **Railway**, en utilisant Gunicorn pour servir l'application Django.

## 🛠️ Stack de Production
- **Serveur Web** : Gunicorn (`gunicorn`)
- **Fichiers Statiques** : Whitenoise (sert les fichiers CSS, JS avec cache).
- **Base de données** : PostgreSQL (connectée via `DATABASE_URL`).
- **Médias** : Supabase Storage (connectée via les clés de l'API Supabase).

---

## 📦 Fichiers Clés de Déploiement

### 1. `build.sh`
Un script shell utilisé par le service cloud (comme Render) lors de l'étape de construction (Build) pour préparer l'environnement :
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques (CSS, JS) dans un dossier pour Whitenoise
python manage.py collectstatic --no-input

# Appliquer automatiquement les migrations de base de données
python manage.py migrate
```

### 2. `Procfile`
Ce fichier indique à l'hébergeur la commande exacte à exécuter pour démarrer l'application.
```text
web: gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
```

### 3. `runtime.txt`
Spécifie la version exacte de Python requise pour garantir la compatibilité (actuellement Python 3.x selon configuration).

---

## 🔐 Variables d'Environnement Obligatoires (Production)

Dans les paramètres de votre service cloud (Render, Heroku, etc.), vous devez configurer les variables d'environnement suivantes :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Clé secrète Django (ne pas la partager). | `django-insecure-xxx...` |
| `DJANGO_DEBUG` | Doit être strictement `False` en production. | `False` |
| `DATABASE_URL` | L'URL de connexion à la base de données PostgreSQL. | `postgres://user:pass@host/db` |
| `ALLOWED_HOSTS` | Liste des domaines autorisés séparés par une virgule. | `.onrender.com,prisme-media.com` |
| `SUPABASE_URL` | L'URL de l'API de votre projet Supabase. | `https://xxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | La clé d'API publique (anon) de Supabase. | `eyJhbGciOiJIUzI1Ni...` |

---

## 🚀 Étapes de Déploiement sur Render (Exemple)

1. Connectez votre dépôt GitHub à Render (Web Service).
2. Paramétrez l'environnement en `Python`.
3. Commande de Build (`Build Command`) : `./build.sh`
4. Commande de lancement (`Start Command`) : `gunicorn config.wsgi` (géré par Render)
5. Allez dans l'onglet **Environment** et ajoutez toutes les variables du tableau ci-dessus.
6. Cliquez sur **Deploy**.

> **Note de sécurité** : Assurez-vous que l'URL racine configurée pour Allauth correspond bien au domaine final pour que la connexion via Google/Apple/Facebook fonctionne correctement.
