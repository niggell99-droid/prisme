from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profil

# Ce décorateur relie la fonction au signal 'post_save' du modèle User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return # Ignore si l'objet est importé via loaddata
    if created:
        # Si un nouvel utilisateur est créé (created=True), créez un profil vide
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        return
    # À chaque sauvegarde d'utilisateur, sauvegarde également le profil lié
    # (Nécessaire pour le formulaire d'édition)
    if hasattr(instance, 'profil'):
        instance.profil.save()