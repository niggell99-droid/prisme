"""
Script de population de la base de données avec des données de test.
À exécuter avec : python manage.py shell < populate_db.py

Ce script crée :
- 3 utilisateurs de test (auteurs + lecteurs)
- Catégories et tags pour le blog
- 8 articles de blog avec différents statuts
- Topics et threads pour le forum
- Projets/tutoriels
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from blog.models import Article, Category, Tag
from forum.models import Topic, Thread, Post
from projets.models import Projet, Tool
from utilisateurs.models import Profil

print("🌱 Démarrage de la population de la base de données...\n")

# ================== ÉTAPE 1 : CRÉER DES UTILISATEURS ==================
print("1️⃣ Création des utilisateurs...")

users_data = [
    {'username': 'alice', 'email': 'alice@prisme.local', 'first_name': 'Alice', 'last_name': 'Dupont'},
    {'username': 'bob', 'email': 'bob@prisme.local', 'first_name': 'Bob', 'last_name': 'Martin'},
    {'username': 'charlie', 'email': 'charlie@prisme.local', 'first_name': 'Charlie', 'last_name': 'Durand'},
]

users = {}
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
        }
    )
    if created:
        user.set_password('password123')  # Mot de passe de test
        user.save()
        print(f"  ✅ Utilisateur créé : {user.username}")
    else:
        print(f"  ℹ️  Utilisateur existe déjà : {user.username}")
    users[user_data['username']] = user

# Marquer les utilisateurs comme auteurs
for user in [users['alice'], users['bob']]:
    if hasattr(user, 'profil'):
        user.profil.is_author = True
        user.profil.save()
        print(f"  👤 {user.username} marqué comme auteur")

# ================== ÉTAPE 2 : CRÉER DES CATÉGORIES ==================
print("\n2️⃣ Création des catégories...")

categories_data = [
    {'name': 'Intelligence Artificielle', 'slug': 'ia'},
    {'name': 'Électronique', 'slug': 'electronique'},
    {'name': 'Robotique', 'slug': 'robotique'},
    {'name': 'Programmation', 'slug': 'programmation'},
]

categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name']}
    )
    if created:
        print(f"  ✅ Catégorie créée : {category.name}")
    else:
        print(f"  ℹ️  Catégorie existe déjà : {category.name}")
    categories[cat_data['slug']] = category

# ================== ÉTAPE 3 : CRÉER DES TAGS ==================
print("\n3️⃣ Création des tags...")

tags_data = [
    {'name': 'Python', 'slug': 'python'},
    {'name': 'Arduino', 'slug': 'arduino'},
    {'name': 'Machine Learning', 'slug': 'ml'},
    {'name': 'Web', 'slug': 'web'},
    {'name': 'IoT', 'slug': 'iot'},
]

tags = {}
for tag_data in tags_data:
    tag, created = Tag.objects.get_or_create(
        slug=tag_data['slug'],
        defaults={'name': tag_data['name']}
    )
    if created:
        print(f"  ✅ Tag créé : {tag.name}")
    else:
        print(f"  ℹ️  Tag existe déjà : {tag.name}")
    tags[tag_data['slug']] = tag

# ================== ÉTAPE 4 : CRÉER DES ARTICLES ==================
print("\n4️⃣ Création des articles...")

articles_data = [
    {
        'title': 'Introduction à Python pour les Débutants',
        'slug': 'intro-python-debutants',
        'excerpt': 'Découvrez les bases de Python, le langage idéal pour débuter en programmation.',
        'content': '<h2>Pourquoi Python ?</h2><p>Python est un langage de programmation simple et puissant...</p>',
        'category': 'programmation',
        'tags': ['python'],
        'is_published': True,
        'is_featured': True,
        'reading_time': 8,
        'author': users['alice'],
    },
    {
        'title': 'IoT avec Arduino : Capteurs de Température',
        'slug': 'iot-arduino-temperature',
        'excerpt': 'Créez un système IoT pour mesurer la température avec Arduino.',
        'content': '<h2>Mise en place</h2><p>Nous allons configurer un capteur DHT22 connecté à Arduino...</p>',
        'category': 'electronique',
        'tags': ['arduino', 'iot'],
        'is_published': True,
        'is_featured': False,
        'reading_time': 12,
        'author': users['bob'],
    },
    {
        'title': 'Machine Learning avec TensorFlow',
        'slug': 'ml-tensorflow-guide',
        'excerpt': 'Guide complet pour débuter avec TensorFlow et construire vos premiers modèles.',
        'content': '<h2>Installation</h2><p>Commencez par installer TensorFlow...</p>',
        'category': 'ia',
        'tags': ['python', 'ml'],
        'is_published': True,
        'is_featured': False,
        'reading_time': 15,
        'author': users['alice'],
    },
    {
        'title': 'Bras Robotique DIY - Partie 1',
        'slug': 'bras-robotique-diy-part1',
        'excerpt': 'Construisez votre propre bras robotique avec moteurs pas à pas.',
        'content': '<h2>Matériel nécessaire</h2><p>Pour ce projet, vous aurez besoin de...</p>',
        'category': 'robotique',
        'tags': ['arduino'],
        'is_published': True,
        'is_featured': False,
        'reading_time': 20,
        'author': users['bob'],
    },
    {
        'title': 'Django REST Framework : Créer une API',
        'slug': 'django-rest-api',
        'excerpt': 'Apprenez à créer une API REST avec Django et Django REST Framework.',
        'content': '<h2>Configuration</h2><p>Installez d\'abord le paquet...</p>',
        'category': 'programmation',
        'tags': ['python', 'web'],
        'is_published': True,
        'is_featured': False,
        'reading_time': 18,
        'author': users['alice'],
    },
    {
        'title': 'Capteurs pour Projets IoT',
        'slug': 'capteurs-iot',
        'excerpt': 'Comparaison des meilleurs capteurs pour vos projets IoT.',
        'content': '<h2>Types de Capteurs</h2><p>Découvrez les différents types de capteurs...</p>',
        'category': 'electronique',
        'tags': ['iot'],
        'is_published': True,
        'is_featured': False,
        'reading_time': 10,
        'author': users['bob'],
    },
    {
        'title': '[BROUILLON] Article en Cours - Vision par Ordinateur',
        'slug': 'vision-ordinateur-draft',
        'excerpt': 'Cet article est encore en brouillon.',
        'content': '<p>Contenu en cours de rédaction...</p>',
        'category': 'ia',
        'tags': ['ml'],
        'is_published': False,
        'is_featured': False,
        'reading_time': 0,
        'author': users['alice'],
    },
    {
        'title': 'Système de Serre Connectée avec IoT',
        'slug': 'serre-connectee-iot',
        'excerpt': 'Créez une serre intelligente qui mesure l\'humidité, la température et contrôle l\'arrosage.',
        'content': '<h2>Vue d\'ensemble</h2><p>Ce projet montre comment créer une serre intelligente...</p>',
        'category': 'iot',
        'tags': ['arduino', 'iot', 'python'],
        'is_published': True,
        'is_featured': False,
        'reading_time': 22,
        'author': users['bob'],
    },
]

articles_created = []
for article_data in articles_data:
    category_obj = categories.get(article_data['category'])
    if not category_obj:
        print(f"  ⚠️  Catégorie introuvable : {article_data['category']}")
        continue
    
    article, created = Article.objects.get_or_create(
        slug=article_data['slug'],
        defaults={
            'title': article_data['title'],
            'excerpt': article_data['excerpt'],
            'content': article_data['content'],
            'category': category_obj,
            'is_published': article_data['is_published'],
            'is_featured': article_data['is_featured'],
            'reading_time': article_data['reading_time'],
            'author': article_data['author'],
            'publication_date': timezone.now() - timedelta(days=len(articles_created)),
        }
    )
    
    if created:
        # Ajouter les tags
        for tag_slug in article_data['tags']:
            tag_obj = tags.get(tag_slug)
            if tag_obj:
                article.tags.add(tag_obj)
        
        status = "✅ Publié" if article_data['is_published'] else "📝 Brouillon"
        print(f"  {status}: {article.title}")
        articles_created.append(article)
    else:
        print(f"  ℹ️  Article existe déjà : {article.title}")

# ================== ÉTAPE 5 : CRÉER DES TOPICS FORUM ==================
print("\n5️⃣ Création des thèmes du forum...")

topics_data = [
    {'name': 'Questions Générales', 'slug': 'questions-generales', 'description': 'Posez vos questions sur l\'ingénierie, la programmation et les technologies.'},
    {'name': 'Projets & Tutoriels', 'slug': 'projets-tutoriels', 'description': 'Partagez vos projets, tutoriels et trouvez de l\'inspiration.'},
    {'name': 'Hardware & Électronique', 'slug': 'hardware', 'description': 'Discussions sur l\'électronique, Arduino, Raspberry Pi et autres composants.'},
    {'name': 'IA & Machine Learning', 'slug': 'ai-ml', 'description': 'Explorez l\'intelligence artificielle et le machine learning.'},
]

topics = {}
for topic_data in topics_data:
    topic, created = Topic.objects.get_or_create(
        slug=topic_data['slug'],
        defaults={
            'name': topic_data['name'],
            'description': topic_data['description'],
        }
    )
    if created:
        print(f"  ✅ Topic créé : {topic.name}")
    else:
        print(f"  ℹ️  Topic existe déjà : {topic.name}")
    topics[topic_data['slug']] = topic

# ================== ÉTAPE 6 : CRÉER DES THREADS & POSTS ==================
print("\n6️⃣ Création des threads et posts du forum...")

threads_data = [
    {
        'topic': 'questions-generales',
        'title': 'Comment débuter en programmation ?',
        'starter': users['charlie'],
        'posts': [
            {'author': users['alice'], 'content': 'Bonjour ! Je recommande de commencer par Python, c\'est simple et puissant.'},
            {'author': users['bob'], 'content': 'D\'accord ! Et puis il y a plein de ressources en ligne pour apprendre Python.'},
        ]
    },
    {
        'topic': 'projets-tutoriels',
        'title': 'Mon premier projet Arduino - Compteur automatique',
        'starter': users['bob'],
        'posts': [
            {'author': users['bob'], 'content': 'J\'ai terminé mon premier projet IoT : un compteur automatique avec Arduino !'},
            {'author': users['alice'], 'content': 'Génial ! Peux-tu partager le code sur GitHub ?'},
        ]
    },
    {
        'topic': 'hardware',
        'title': 'Quel capteur choisir pour mesurer l\'humidité ?',
        'starter': users['charlie'],
        'posts': [
            {'author': users['bob'], 'content': 'Le DHT22 est excellent pour l\'humidité et la température.'},
            {'author': users['alice'], 'content': 'Je préfère le BME680 car il mesure aussi la pression et la qualité de l\'air.'},
        ]
    },
    {
        'topic': 'ai-ml',
        'title': 'TensorFlow vs PyTorch - lequel choisir ?',
        'starter': users['alice'],
        'posts': [
            {'author': users['alice'], 'content': 'TensorFlow est plus populaire et a plus de ressources, PyTorch est plus flexible.'},
            {'author': users['bob'], 'content': 'Cela dépend de votre cas d\'usage. Les deux sont excellents !'},
        ]
    },
]

for thread_data in threads_data:
    topic_obj = topics.get(thread_data['topic'])
    if not topic_obj:
        print(f"  ⚠️  Topic introuvable : {thread_data['topic']}")
        continue
    
    thread, created = Thread.objects.get_or_create(
        slug=thread_data['title'].lower().replace(' ', '-')[:50],
        defaults={
            'title': thread_data['title'],
            'topic': topic_obj,
            'starter': thread_data['starter'],
        }
    )
    
    if created:
        print(f"  ✅ Thread créé : {thread.title}")
        
        # Créer les posts
        for post_data in thread_data['posts']:
            post, _ = Post.objects.get_or_create(
                thread=thread,
                author=post_data['author'],
                defaults={'content': post_data['content']}
            )
    else:
        print(f"  ℹ️  Thread existe déjà : {thread.title}")

# ================== ÉTAPE 7 : CRÉER DES OUTILS ==================
print("\n7️⃣ Création des outils/technologies...")

tools_data = [
    {'name': 'Python', 'slug': 'python'},
    {'name': 'Arduino', 'slug': 'arduino'},
    {'name': 'Raspberry Pi', 'slug': 'raspberrypi'},
    {'name': 'Django', 'slug': 'django'},
    {'name': 'TensorFlow', 'slug': 'tensorflow'},
]

tools = {}
for tool_data in tools_data:
    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={}
    )
    if created:
        print(f"  ✅ Outil créé : {tool.name}")
    else:
        print(f"  ℹ️  Outil existe déjà : {tool.name}")
    tools[tool_data['slug']] = tool

# ================== ÉTAPE 8 : CRÉER DES PROJETS ==================
print("\n8️⃣ Création des projets...")

projects_data = [
    {
        'title': 'Station Météo Connectée',
        'slug': 'station-meteo',
        'summary': 'Une station météo IoT complète qui mesure température, humidité et pression.',
        'content': '<h2>Objectif</h2><p>Construire une station météo connectée avec des capteurs Arduino...</p>',
        'difficulty': 'MOYEN',
        'duration': '2-3 jours',
        'author': users['bob'],
        'tools': ['arduino', 'raspberrypi'],
        'is_published': True,
    },
    {
        'title': 'Chatbot IA avec Python',
        'slug': 'chatbot-ia',
        'summary': 'Créez un chatbot intelligent avec NLP et TensorFlow.',
        'content': '<h2>Introduction</h2><p>Dans ce tutoriel, nous allons créer un chatbot simple...</p>',
        'difficulty': 'DIFFICILE',
        'duration': '1 semaine',
        'author': users['alice'],
        'tools': ['python', 'tensorflow'],
        'is_published': True,
    },
    {
        'title': 'API REST avec Django',
        'slug': 'api-rest-django',
        'summary': 'Apprenez à construire une API REST professionnelle avec Django.',
        'content': '<h2>Prérequis</h2><p>Vous devez connaître Django et Python...</p>',
        'difficulty': 'MOYEN',
        'duration': '3-4 jours',
        'author': users['alice'],
        'tools': ['django', 'python'],
        'is_published': True,
    },
    {
        'title': '[BROUILLON] Bras Robotique Intelligent',
        'slug': 'bras-robotique',
        'summary': 'Projet en cours : construire un bras robotique avec contrôle IA.',
        'content': '<p>Projet en cours de développement...</p>',
        'difficulty': 'EXPERT',
        'duration': '2 semaines',
        'author': users['bob'],
        'tools': ['arduino', 'python'],
        'is_published': False,
    },
]

for project_data in projects_data:
    projet, created = Projet.objects.get_or_create(
        slug=project_data['slug'],
        defaults={
            'title': project_data['title'],
            'summary': project_data['summary'],
            'content': project_data['content'],
            'difficulty': project_data['difficulty'],
            'duration': project_data['duration'],
            'author': project_data['author'],
            'is_published': project_data['is_published'],
        }
    )
    
    if created:
        # Ajouter les outils
        for tool_slug in project_data['tools']:
            tool_obj = tools.get(tool_slug)
            if tool_obj:
                projet.tools.add(tool_obj)
        
        status = "✅ Publié" if project_data['is_published'] else "📝 Brouillon"
        print(f"  {status}: {projet.title}")
    else:
        print(f"  ℹ️  Projet existe déjà : {projet.title}")

# ================== RÉSUMÉ ==================
print("\n" + "="*60)
print("✅ POPULATION DE LA BASE DE DONNÉES TERMINÉE !")
print("="*60)
print(f"\n📊 Statistiques :")
print(f"  • Utilisateurs : {User.objects.count()}")
print(f"  • Catégories : {Category.objects.count()}")
print(f"  • Tags : {Tag.objects.count()}")
print(f"  • Articles : {Article.objects.count()} (publiés: {Article.objects.filter(is_published=True).count()})")
print(f"  • Topics Forum : {Topic.objects.count()}")
print(f"  • Threads Forum : {Thread.objects.count()}")
print(f"  • Posts Forum : {Post.objects.count()}")
print(f"  • Outils : {Tool.objects.count()}")
print(f"  • Projets : {Projet.objects.count()} (publiés: {Projet.objects.filter(is_published=True).count()})")

print(f"\n🔐 Identifiants de test :")
for username in users_data:
    print(f"  • {username['username']} / password123")

print(f"\n🌐 URLs à visiter :")
print(f"  • http://localhost:8000/blog/ (articles)")
print(f"  • http://localhost:8000/forum/ (forum)")
print(f"  • http://localhost:8000/projets/ (projets)")
print(f"  • http://localhost:8000/admin/ (admin)")
print("\n")
