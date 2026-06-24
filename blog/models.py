from django.db import models
from django.contrib.auth.models import User # On utilise le modèle User natif de Django
from django.urls import reverse 
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from core.models import Comment

# 1. Modèle pour les Catégories
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories" # Correction pour l'affichage dans l'Admin

    def __str__(self):
        return self.name

# 2. Modèle pour les Tags
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
# Choix pour le champ video
VIDEO_STATUS_CHOICES = [
    ('NONE', 'Pas de video'),
    ('PLANNED', 'Video planifiee'),
    ('RECORDER', 'Video enregistree'),
    ('PUBLISHED', 'video publiee'),
]


# 3. Modèle principal pour l'Article
class Article(models.Model):
    # Informations de base
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True) # ID pour l'URL
    excerpt = models.TextField(blank=True, help_text="Résumé ou accroche pour la page d'accueil")
    # CKEditor5Field for rich text editing
    content = CKEditor5Field('Contenu de l\'article', config_name='extends')

    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE) # L'auteur
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) # Catégorie principale (SET_NULL permet de ne pas supprimer l'article si la catégorie est supprimée)
    tags = models.ManyToManyField(Tag, blank=True) # Multiples tags
    comments = GenericRelation(Comment)

    # Médias
    featured_image = models.ImageField(upload_to='article_images/', blank=True, null=True)

    # Horodatage et statut
    publication_date = models.DateTimeField(
        default=timezone.now, # DÉFINIT LA VALEUR PAR DÉFAUT
        verbose_name="Date de publication",
        help_text="Définissez la date/heure future pour une publication planifiée."
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # is_featured = models.BooleanField(default=False, help_text="Afficher sur la page d'accueil (Hero)")
    is_featured = models.BooleanField(default=False, verbose_name="Mis en avant sur la page d'accueil")

    reading_time = models.IntegerField(
        default=0,
        verbose_name="Temps de lecture (minutes)",
        help_text="Estimez le temps de lecture de l'article."
    )

    video_status = models.CharField(
        max_length=10,
        choices=VIDEO_STATUS_CHOICES,
        default='NONE',
        verbose_name="statut video d'accompagnement",
        help_text="Indique si une video est associee ou prevue pour cet article."
    )

    class Meta:
        ordering = ['-publication_date'] # Les articles sont triés par date de publication décroissante

    def __str__(self):
        return self.title
    
    def get_content_type_id(self):
        """Retourne l'ID du ContentType pour le modèle Article (utilisé par le système de commentaires)."""
        return ContentType.objects.get_for_model(self).pk

    def get_absolute_url(self):
        """
        Retourne l'URL canonique pour un objet Article donné, 
        en utilisant le 'slug' comme identifiant dans l'URL.
        """
        # 'article_detail' sera le nom de notre URL (voir point 8.3)
        return reverse('blog:article_detail', kwargs={'slug': self.slug})