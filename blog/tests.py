from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Article, Category


class BlogPaginationTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='tester', password='pass')
		self.category = Category.objects.create(name='Test', slug='test')

		# Create 15 published articles
		for i in range(15):
			Article.objects.create(
				title=f'Article {i}',
				slug=f'article-{i}',
				excerpt='ex',
				content='contenu',
				author=self.user,
				category=self.category,
				publication_date=timezone.now(),
				is_published=True
			)

	def test_article_list_pagination_first_page(self):
		url = reverse('blog:article_list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		articles = response.context['articles']
		# Should be a Page object with 10 items on first page
		self.assertEqual(len(articles.object_list), 10)

	def test_article_list_pagination_second_page(self):
		url = reverse('blog:article_list') + '?page=2'
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		articles = response.context['articles']
		# Remaining 5 articles on second page
		self.assertEqual(len(articles.object_list), 5)


import json
from unittest.mock import patch, MagicMock
from django.test import override_settings
from .ai_summary import clean_html_content, generate_article_summary


class ArticleAISummaryTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser(
			username='admin_user',
			email='admin@example.com',
			password='adminpassword'
		)
		self.category = Category.objects.create(name='Tech', slug='tech')

	def test_clean_html_content(self):
		html_sample = "<p>Bonjour <strong>le monde</strong> &amp; bienvenue.</p><p><br></p>"
		cleaned = clean_html_content(html_sample)
		self.assertEqual(cleaned, "Bonjour le monde & bienvenue.")

	def test_generate_article_summary_short_content_raises_error(self):
		with self.assertRaises(ValueError):
			generate_article_summary("<p>Trop court</p>")

	@override_settings(GEMINI_API_KEY='')
	def test_generate_article_summary_missing_api_key(self):
		long_text = "<p>" + "Contenu de test pour l'article. " * 10 + "</p>"
		with patch.dict('os.environ', {}, clear=True):
			with self.assertRaises(ValueError):
				generate_article_summary(long_text)

	@override_settings(GEMINI_API_KEY='fake-test-key')
	@patch('google.generativeai.GenerativeModel')
	def test_generate_article_summary_success(self, mock_model_cls):
		mock_instance = MagicMock()
		mock_response = MagicMock()
		mock_response.text = '"Un résumé captivant généré par Gemini."'
		mock_instance.generate_content.return_value = mock_response
		mock_model_cls.return_value = mock_instance

		long_text = "<p>" + "Contenu de l'article avec beaucoup de mots. " * 5 + "</p>"
		summary = generate_article_summary(long_text, title="Titre Test")
		self.assertEqual(summary, "Un résumé captivant généré par Gemini.")

	@override_settings(GEMINI_API_KEY='fake-test-key')
	@patch('blog.ai_summary.generate_article_summary')
	def test_article_save_auto_generates_summary_when_excerpt_empty(self, mock_summary_fn):
		mock_summary_fn.return_value = "Résumé automatique pour nouveau post."
		
		article = Article(
			title="Nouvel Article Sans Résumé",
			slug="nouvel-article-sans-resume",
			excerpt="", # Laissé vide
			content="<p>Voici un contenu détaillé rédigé pour cet article de test.</p>",
			author=self.user,
			category=self.category,
		)
		article.save()

		# L'excerpt doit avoir été rempli automatiquement
		self.assertEqual(article.excerpt, "Résumé automatique pour nouveau post.")
		mock_summary_fn.assert_called_once()

	@override_settings(GEMINI_API_KEY='fake-test-key')
	@patch('blog.ai_summary.generate_article_summary')
	def test_article_save_preserves_existing_excerpt(self, mock_summary_fn):
		article = Article(
			title="Article avec résumé manuel",
			slug="article-avec-resume-manuel",
			excerpt="Mon résumé rédigé manuellement par l'auteur.",
			content="<p>Voici un contenu détaillé rédigé pour cet article de test.</p>",
			author=self.user,
			category=self.category,
		)
		article.save()

		# L'excerpt existant ne doit JAMAIS être écrasé
		self.assertEqual(article.excerpt, "Mon résumé rédigé manuellement par l'auteur.")
		mock_summary_fn.assert_not_called()

	@override_settings(GEMINI_API_KEY='fake-test-key')
	@patch('blog.admin.generate_article_summary')
	def test_admin_generate_summary_endpoint(self, mock_summary_fn):
		mock_summary_fn.return_value = "Résumé généré via AJAX."
		self.client.login(username='admin_user', password='adminpassword')

		url = reverse('admin:blog_article_generate_summary')
		payload = {
			'title': 'Mon Super Article',
			'content': '<p>Contenu rédigé dans CKEditor par le rédacteur.</p>'
		}
		response = self.client.post(
			url,
			data=json.dumps(payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertTrue(data.get('success'))
		self.assertEqual(data.get('summary'), "Résumé généré via AJAX.")
