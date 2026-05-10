"""
Management command pour remplir la base de données avec des données de test.
Utilisation : python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from blog.models import Article, Category, Tag
from forum.models import Topic, Thread, Post
from projets.models import Projet, Tool
from utilisateurs.models import Profil


class Command(BaseCommand):
    help = 'Remplit la base de donnees avec des donnees de test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n--- Demarrage de la population de la base de donnees ---\n'))

        # ================== ETAPE 1 : CREER DES UTILISATEURS ==================
        self.stdout.write('1. Creation des utilisateurs...')

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
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  OK - Utilisateur cree : {user.username}')
            else:
                self.stdout.write(f'  INFO - Utilisateur existe deja : {user.username}')
            users[user_data['username']] = user

        # Marquer les utilisateurs comme auteurs
        for user in [users['alice'], users['bob']]:
            if hasattr(user, 'profil'):
                user.profil.is_author = True
                user.profil.save()
                self.stdout.write(f'  INFO - {user.username} marque comme auteur')

        # ================== ETAPE 2 : CREER DES CATEGORIES ==================
        self.stdout.write('\n2. Creation des categories...')

        categories_data = [
            {'name': 'Intelligence Artificielle', 'slug': 'ia'},
            {'name': 'Electronique', 'slug': 'electronique'},
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
                self.stdout.write(f'  OK - Categorie creee : {category.name}')
            else:
                self.stdout.write(f'  INFO - Categorie existe deja : {category.name}')
            categories[cat_data['slug']] = category

        # ================== ETAPE 3 : CREER DES TAGS ==================
        self.stdout.write('\n3. Creation des tags...')

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
                self.stdout.write(f'  OK - Tag cree : {tag.name}')
            else:
                self.stdout.write(f'  INFO - Tag existe deja : {tag.name}')
            tags[tag_data['slug']] = tag

        # ================== ETAPE 4 : CREER DES ARTICLES ==================
        self.stdout.write('\n4. Creation des articles...')

        articles_data = [
            {
                'title': 'Introduction a Python pour les Debutants',
                'slug': 'intro-python-debutants',
                'excerpt': 'Decouvrez les bases de Python, le langage ideal pour debuter en programmation.',
                'content': '<h2>Pourquoi Python ?</h2><p>Python est un langage de programmation simple et puissant...</p>',
                'category': 'programmation',
                'tags': ['python'],
                'is_published': True,
                'is_featured': True,
                'reading_time': 8,
                'author': users['alice'],
            },
            {
                'title': 'IoT avec Arduino : Capteurs de Temperature',
                'slug': 'iot-arduino-temperature',
                'excerpt': 'Creez un systeme IoT pour mesurer la temperature avec Arduino.',
                'content': '<h2>Mise en place</h2><p>Nous allons configurer un capteur DHT22 connecte a Arduino...</p>',
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
                'excerpt': 'Guide complet pour debuter avec TensorFlow et construire vos premiers modeles.',
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
                'excerpt': 'Construisez votre propre bras robotique avec moteurs pas a pas.',
                'content': '<h2>Materiel necessaire</h2><p>Pour ce projet, vous aurez besoin de...</p>',
                'category': 'robotique',
                'tags': ['arduino'],
                'is_published': True,
                'is_featured': False,
                'reading_time': 20,
                'author': users['bob'],
            },
            {
                'title': 'Django REST Framework : Creer une API',
                'slug': 'django-rest-api',
                'excerpt': 'Apprenez a creer une API REST avec Django et Django REST Framework.',
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
                'content': '<h2>Types de Capteurs</h2><p>Decouvrez les differents types de capteurs...</p>',
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
                'content': '<p>Contenu en cours de redaction...</p>',
                'category': 'ia',
                'tags': ['ml'],
                'is_published': False,
                'is_featured': False,
                'reading_time': 0,
                'author': users['alice'],
            },
            {
                'title': 'Systeme de Serre Connectee avec IoT',
                'slug': 'serre-connectee-iot',
                'excerpt': 'Creez une serre intelligente qui mesure l\'humidite, la temperature et controle l\'arrosage.',
                'content': '<h2>Vue d\'ensemble</h2><p>Ce projet montre comment creer une serre intelligente...</p>',
                'category': 'electronique',
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
                self.stdout.write(self.style.WARNING(f'  ERREUR - Categorie introuvable : {article_data["category"]}'))
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
                for tag_slug in article_data['tags']:
                    tag_obj = tags.get(tag_slug)
                    if tag_obj:
                        article.tags.add(tag_obj)

                status = 'Publie' if article_data['is_published'] else 'Brouillon'
                self.stdout.write(f'  OK - [{status}] {article.title}')
                articles_created.append(article)
            else:
                self.stdout.write(f'  INFO - Article existe deja : {article.title}')

        # ================== ETAPE 5 : CREER DES TOPICS FORUM ==================
        self.stdout.write('\n5. Creation des themes du forum...')

        topics_data = [
            {'name': 'Questions Generales', 'slug': 'questions-generales', 'description': 'Posez vos questions sur l\'ingenierie, la programmation et les technologies.'},
            {'name': 'Projets & Tutoriels', 'slug': 'projets-tutoriels', 'description': 'Partagez vos projets, tutoriels et trouvez de l\'inspiration.'},
            {'name': 'Hardware & Electronique', 'slug': 'hardware', 'description': 'Discussions sur l\'electronique, Arduino, Raspberry Pi et autres composants.'},
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
                self.stdout.write(f'  OK - Topic cree : {topic.name}')
            else:
                self.stdout.write(f'  INFO - Topic existe deja : {topic.name}')
            topics[topic_data['slug']] = topic

        # ================== ETAPE 6 : CREER DES THREADS & POSTS ==================
        self.stdout.write('\n6. Creation des threads et posts du forum...')

        threads_data = [
            {
                'topic': 'questions-generales',
                'title': 'Comment debuter en programmation ?',
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
                    {'author': users['bob'], 'content': 'J\'ai termine mon premier projet IoT : un compteur automatique avec Arduino !'},
                    {'author': users['alice'], 'content': 'Genial ! Peux-tu partager le code sur GitHub ?'},
                ]
            },
            {
                'topic': 'hardware',
                'title': 'Quel capteur choisir pour mesurer l\'humidite ?',
                'starter': users['charlie'],
                'posts': [
                    {'author': users['bob'], 'content': 'Le DHT22 est excellent pour l\'humidite et la temperature.'},
                    {'author': users['alice'], 'content': 'Je prefere le BME680 car il mesure aussi la pression et la qualite de l\'air.'},
                ]
            },
            {
                'topic': 'ai-ml',
                'title': 'TensorFlow vs PyTorch - lequel choisir ?',
                'starter': users['alice'],
                'posts': [
                    {'author': users['alice'], 'content': 'TensorFlow est plus populaire et a plus de ressources, PyTorch est plus flexible.'},
                    {'author': users['bob'], 'content': 'Cela depend de votre cas d\'usage. Les deux sont excellents !'},
                ]
            },
        ]

        for thread_data in threads_data:
            topic_obj = topics.get(thread_data['topic'])
            if not topic_obj:
                self.stdout.write(self.style.WARNING(f'  ERREUR - Topic introuvable : {thread_data["topic"]}'))
                continue

            thread_slug = thread_data['title'].lower().replace(' ', '-')[:50]
            thread, created = Thread.objects.get_or_create(
                slug=thread_slug,
                defaults={
                    'title': thread_data['title'],
                    'topic': topic_obj,
                    'starter': thread_data['starter'],
                }
            )

            if created:
                self.stdout.write(f'  OK - Thread cree : {thread.title}')

                for post_data in thread_data['posts']:
                    post, _ = Post.objects.get_or_create(
                        thread=thread,
                        author=post_data['author'],
                        defaults={'content': post_data['content']}
                    )
            else:
                self.stdout.write(f'  INFO - Thread existe deja : {thread.title}')

        # ================== ETAPE 7 : CREER DES OUTILS ==================
        self.stdout.write('\n7. Creation des outils/technologies...')

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
                self.stdout.write(f'  OK - Outil cree : {tool.name}')
            else:
                self.stdout.write(f'  INFO - Outil existe deja : {tool.name}')
            tools[tool_data['slug']] = tool

        # ================== ETAPE 8 : CREER DES PROJETS ==================
        self.stdout.write('\n8. Creation des projets...')

        projects_data = [
            {
                'title': 'Station Meteo Connectee',
                'slug': 'station-meteo',
                'summary': 'Une station meteo IoT complete qui mesure temperature, humidite et pression.',
                'content': '<h2>Objectif</h2><p>Construire une station meteo connectee avec des capteurs Arduino...</p>',
                'difficulty': 'MOYEN',
                'duration': '2-3 jours',
                'author': users['bob'],
                'tools': ['arduino', 'raspberrypi'],
                'is_published': True,
            },
            {
                'title': 'Chatbot IA avec Python',
                'slug': 'chatbot-ia',
                'summary': 'Creez un chatbot intelligent avec NLP et TensorFlow.',
                'content': '<h2>Introduction</h2><p>Dans ce tutoriel, nous allons creer un chatbot simple...</p>',
                'difficulty': 'DIFFICILE',
                'duration': '1 semaine',
                'author': users['alice'],
                'tools': ['python', 'tensorflow'],
                'is_published': True,
            },
            {
                'title': 'API REST avec Django',
                'slug': 'api-rest-django',
                'summary': 'Apprenez a construire une API REST professionnelle avec Django.',
                'content': '<h2>Prerequis</h2><p>Vous devez connaitre Django et Python...</p>',
                'difficulty': 'MOYEN',
                'duration': '3-4 jours',
                'author': users['alice'],
                'tools': ['django', 'python'],
                'is_published': True,
            },
            {
                'title': '[BROUILLON] Bras Robotique Intelligent',
                'slug': 'bras-robotique',
                'summary': 'Projet en cours : construire un bras robotique avec controle IA.',
                'content': '<p>Projet en cours de developpement...</p>',
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
                for tool_slug in project_data['tools']:
                    tool_obj = tools.get(tool_slug)
                    if tool_obj:
                        projet.tools.add(tool_obj)

                status = 'Publie' if project_data['is_published'] else 'Brouillon'
                self.stdout.write(f'  OK - [{status}] {projet.title}')
            else:
                self.stdout.write(f'  INFO - Projet existe deja : {projet.title}')

        # ================== RESUME ==================
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('POPULATION DE LA BASE DE DONNEES TERMINEE !'))
        self.stdout.write(self.style.SUCCESS('='*60))

        self.stdout.write(f'\nStatistiques :')
        self.stdout.write(f'  - Utilisateurs : {User.objects.count()}')
        self.stdout.write(f'  - Categories : {Category.objects.count()}')
        self.stdout.write(f'  - Tags : {Tag.objects.count()}')
        self.stdout.write(f'  - Articles : {Article.objects.count()} (publies: {Article.objects.filter(is_published=True).count()})')
        self.stdout.write(f'  - Topics Forum : {Topic.objects.count()}')
        self.stdout.write(f'  - Threads Forum : {Thread.objects.count()}')
        self.stdout.write(f'  - Posts Forum : {Post.objects.count()}')
        self.stdout.write(f'  - Outils : {Tool.objects.count()}')
        self.stdout.write(f'  - Projets : {Projet.objects.count()} (publies: {Projet.objects.filter(is_published=True).count()})')

        self.stdout.write(f'\nIdentifiants de test :')
        self.stdout.write(f'  - alice / password123')
        self.stdout.write(f'  - bob / password123')
        self.stdout.write(f'  - charlie / password123')

        self.stdout.write(f'\nURLs a visiter :')
        self.stdout.write(f'  - http://localhost:8000/blog/ (articles)')
        self.stdout.write(f'  - http://localhost:8000/forum/ (forum)')
        self.stdout.write(f'  - http://localhost:8000/projets/ (projets)')
        self.stdout.write(f'  - http://localhost:8000/admin/ (admin)')
        self.stdout.write('')
