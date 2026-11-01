from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Projet
from blog.models import Category
from core.forms import CommentForm

def projet_list(request):
    # Recupere tous les projets publies, tries par date
    all_projets = Projet.objects.filter(is_published=True).order_by('-publication_date')

    context = {
        'projets': all_projets,
        'title': 'Tous les Projets & Tutoriels',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'projets/list.html', context)

def projet_detail(request, slug):
    # Recupere le projet par son slug et s'assure qu'il est publie (sinon 404)
    projet = get_object_or_404(Projet, slug=slug, is_published=True)

    # Fetch comments
    comments = projet.comments.filter(is_active=True).order_by('created_at')
    
    # Instantiate form
    comment_form = CommentForm()

    context = {
        'projet': projet,
        'all_categories': Category.objects.all(),
        'comments': comments,
        'comment_form': comment_form,
        # La galerie est disponible via projet.images.all dans le template
    }
    return render(request, 'projets/detail.html', context)

@login_required
def submit_projet(request):
    """Vue pour la page de soumission d'un projet."""
    context = {
        'title': 'Soumettre un projet',
        'all_categories': Category.objects.all(),
    }
    return render(request, 'projets/submit.html', context)
