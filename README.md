# Prisme

**Prisme** est un média numérique spécialisé dans le domaine de l'ingénierie et des technologies. Il offre une plateforme complète pour découvrir des articles, explorer des projets techniques et échanger via un forum communautaire interactif.

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

---

## 🎯 Fonctionnalités Clés

- **Blog & Actualités** : Gestion d'articles catégorisés avec éditeur de texte riche (CKEditor 5).
- **Portfolio de Projets** : Démonstration de projets d'ingénierie incluant des galeries d'images et des fiches techniques.
- **Forum Communautaire** : Espace d'échange avec des discussions (threads), un système de "pin" pour mettre en avant les sujets, et des statistiques d'engagement.
- **Espace Utilisateur** : Système de profils personnalisés avec gestion d'avatars et authentification sociale (Google, Facebook, Apple).
- **Interface & Design** : Support complet du mode sombre (Dark Mode), design responsive et optimisé pour le web moderne.
- **Stockage Cloud** : Intégration de Supabase Storage pour la gestion sécurisée et rapide des médias (images et vidéos).

## 📚 Documentation Détaillée

Pour comprendre le projet en profondeur, nous avons préparé des documentations spécifiques dans le dossier `/docs` :

- [**Architecture & Structure du Code**](./docs/architecture.md) : Découvrez comment le projet est architecturé (Core, Blog, Projets, Forum, Utilisateurs).
- [**Déploiement & Production**](./docs/deployment.md) : Apprenez comment configurer et déployer le projet sur une plateforme de production (ex: Render).
- [**Licence**](./docs/license.md) : Informations détaillées sur la licence du projet (CC0 1.0 Universal).

## 🚀 Installation & Développement Local

Suivez ces instructions pour installer et faire tourner le projet sur votre machine locale.

### Prérequis
- Python 3.10 ou supérieur
- Pip et Virtualenv

### 1. Cloner le dépôt

```bash
git clone https://github.com/niggell99-droid/prisme.git
cd polymat-project
```

### 2. Créer et activer l'environnement virtuel

**Sur Windows :**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Sur macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement

Créez un fichier `.env` à la racine du projet et ajoutez vos variables :

```env
DJANGO_SECRET_KEY=votre_cle_secrete_django
DJANGO_DEBUG=True

# Supabase (pour la gestion des images/médias - optionnel en local)
SUPABASE_URL=votre_url_supabase
SUPABASE_ANON_KEY=votre_cle_supabase
```
*Note : Si les clés Supabase ne sont pas fournies en développement, le projet utilisera par défaut le stockage de fichiers local (`/media/`).*

### 5. Base de données & Migrations

```bash
python manage.py migrate
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```
L'application est maintenant accessible sur `http://127.0.0.1:8000/`.

---

## 📄 Licence

Ce projet est sous licence **CC0 1.0 Universal (Creative Commons Zero)**, ce qui signifie qu'il appartient au domaine public. Vous êtes libre de copier, modifier, distribuer et exécuter l'œuvre, même à des fins commerciales, sans demander d'autorisation préalable. 

Pour plus de détails, consultez le fichier [LICENSE](./LICENSE) ou [docs/license.md](./docs/license.md).
