# Architecture du Projet Prisme

Prisme est conçu avec le framework **Django** en suivant le patron de conception **MVT** (Model-View-Template). Le projet est structuré en plusieurs applications (apps) indépendantes qui gèrent chacune un domaine fonctionnel spécifique.

## 🧱 Structure des Applications (Apps)

### 1. `core`
L'application centrale du projet. Elle gère la configuration générale et les pages transverses :
- **Modèles** : Gère souvent le routage de base.
- **Vues** : Gère la page d'accueil (`HomeView`), la barre de recherche globale, et les pages statiques (Mentions légales, Contact, Plan du site).
- **Templates & Statique** : Contient le layout principal (`base.html`, `header.html`, `footer.html`) ainsi que le dossier `assets/` où résident tous les fichiers CSS globaux extraits de la refonte, les images, et le JavaScript.

### 2. `blog`
L'application dédiée à la publication d'articles.
- **Modèles** : `Category`, `Article`.
- **Fonctionnalités** : Utilise **django-ckeditor-5** pour fournir un éditeur de texte riche sécurisé à l'administration, avec support d'images uploadées directement sur Supabase.

### 3. `projets`
L'application de présentation de réalisations et portfolios techniques.
- **Modèles** : `Projet`, `ProjectImage` (pour les galeries), `Tool` (pour les badges de technologies).
- **Fonctionnalités** : Présentation détaillée avec gestion de méta-données (durée, lien github, lien live) et galeries fluides.

### 4. `forum`
L'espace communautaire interactif.
- **Modèles** : `Topic` (Catégories du forum), `Thread` (Sujets de discussion créés par les utilisateurs), `Post` (Réponses).
- **Fonctionnalités** : Suivi du nombre de vues, épinglage de sujets (pinning), pagination, flux d'actualités et intégration de widgets vidéos pour les streams "Live".

### 5. `utilisateurs`
L'application de gestion des comptes et de l'authentification.
- **Modèles** : `Profil` (relié avec un `OneToOneField` au modèle `User` natif de Django). Gère l'avatar et la bio.
- **Authentification** : Utilise le package **django-allauth** pour gérer l'inscription, la connexion standard et la connexion sociale (OAuth Google, Facebook, Apple).

---

## 💾 Gestion des Médias et Données

### Base de Données
- **Développement** : Base de données légère `SQLite3` (par défaut).
- **Production** : Configuration via `dj_database_url` pour se connecter à une base de données **PostgreSQL**.

### Stockage (Images & Vidéos)
Prisme utilise **Supabase Storage** pour un hébergement robuste des fichiers uploadés par les utilisateurs et les administrateurs (images d'articles, galeries de projets, avatars).
- **Dépôt** : Le package `django-supabase-storage` remplace le système de fichiers par défaut via `STORAGES` dans `settings.py`.
- **Mécanisme** : Lorsque la variable `.env` `SUPABASE_URL` est présente, tout téléchargement (via l'admin ou CKEditor) est uploadé directement dans le bucket Supabase "media".

---

## 🎨 Design & Interface

L'interface est construite avec du **CSS Vanilla** modulaire. Chaque application dispose de son propre fichier CSS pour une séparation des préoccupations :
- `style.css` (variables CSS, typographie, layout global)
- `blog.css`, `project.css`, `forum.css`, `auth.css`, `comments.css`, `pages.css`
- **Dark Mode** : Implémenté nativement via des variables CSS (ex: `var(--background)`, `var(--text)`) basculées par une logique JavaScript via un bouton toggle et sauvegardées dans le `localStorage`.
- **Admin** : L'interface d'administration Django a été remplacée par **django-unfold**, offrant une expérience utilisateur basée sur Tailwind CSS, beaucoup plus moderne que l'admin natif.
