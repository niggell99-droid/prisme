import json
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_POST
from .models import Article, Category, Tag
from .ai_summary import generate_article_summary

# Enregistrement des modèles simples
admin.site.register(Category)
admin.site.register(Tag)

# Enregistrement du modèle Article avec personnalisation pour plus de professionnalisme
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date', 'is_published')
    list_filter = ('category', 'tags', 'is_published')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)} # Remplissage automatique du slug à partir du titre
    date_hierarchy = 'publication_date'

    # Fieldsets (organisation des champs dans la page d'edition)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content')
        }),
        ('Publication & Visibilite', {
            'fields': ('is_published', 'publication_date', 'featured_image', 'reading_time', 'video_status'),
            'classes': ('collapse',),
        })
    )

    class Media:
        js = ('blog/js/admin_article_summary.js',)
        css = {
            'all': ('blog/css/admin_article_summary.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'generate-summary/',
                self.admin_site.admin_view(self.generate_summary_endpoint),
                name='blog_article_generate_summary'
            ),
        ]
        return custom_urls + urls

    def generate_summary_endpoint(self, request):
        """Endpoint AJAX pour la génération du résumé par IA depuis l'admin."""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'}, status=405)

        if not (self.has_change_permission(request) or self.has_add_permission(request)):
            return JsonResponse({'success': False, 'error': 'Permission refusée.'}, status=403)

        # Récupération des données (JSON ou POST form-data)
        title = ''
        content = ''
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                title = data.get('title', '')
                content = data.get('content', '')
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Requête JSON invalide.'}, status=400)
        else:
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')

        try:
            summary = generate_article_summary(content=content, title=title)
            return JsonResponse({'success': True, 'summary': summary})
        except ValueError as val_err:
            return JsonResponse({'success': False, 'error': str(val_err)}, status=400)
        except Exception as exc:
            return JsonResponse({'success': False, 'error': f"Erreur Gemini : {str(exc)}"}, status=500)
