import html
import logging
import os
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def clean_html_content(raw_html: str) -> str:
    """Nettoie le code HTML (issu de CKEditor) pour obtenir du texte brut."""
    if not raw_html:
        return ""
    text = strip_tags(raw_html)
    text = html.unescape(text)
    # Nettoyage des espaces multiples et retours à la ligne superflus
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def generate_article_summary(content: str, title: str = "") -> str:
    """
    Génère un résumé percutant (2 à 3 phrases) pour un article de blog à l'aide de Google Gemini.
    
    :param content: Le contenu HTML ou texte de l'article.
    :param title: Le titre de l'article (optionnel mais recommandé).
    :return: Le texte du résumé généré.
    :raises ValueError: Si le contenu est trop court ou la clé API absente.
    """
    cleaned_text = clean_html_content(content)
    if not cleaned_text or len(cleaned_text.strip()) < 40:
        raise ValueError("Le contenu de l'article est trop court pour générer un résumé pertinent.")

    # Tronquer si l'article est exceptionnellement long (sécurité tokens)
    if len(cleaned_text) > 30000:
        cleaned_text = cleaned_text[:30000]

    api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        error_msg = "Clé API Gemini non configurée (veuillez renseigner GEMINI_API_KEY dans votre fichier .env)."
        logger.warning(error_msg)
        raise ValueError(error_msg)

    import google.generativeai as genai

    genai.configure(api_key=api_key, transport='rest')
    preferred_model = getattr(settings, 'GEMINI_SUMMARY_MODEL', None) or os.environ.get('GEMINI_SUMMARY_MODEL') or 'gemini-flash-lite-latest'
    
    # Ordre des modèles à tester pour parer aux dépréciations d'alias Google
    model_candidates = [preferred_model]
    for fallback in ['gemini-flash-lite-latest', 'gemini-flash-latest']:
        if fallback not in model_candidates:
            model_candidates.append(fallback)

    prompt = (
        "Tu es un rédacteur en chef et référenceur expert pour un média web moderne qui oeuvre dans l'ingenierie mecatronique avec une philosophie de deconstruction et reconstruction des concepts brique par brique.\n"
        "Rédige un résumé accrocheur, captivant et concis en français (6 points maximum) "
        "de l'article ci-dessous. Ce résumé servira d'accroche/chapeau (excerpt) sur la page d'accueil et les cartes d'articles.\n\n"
        "RÈGLES STRICTES :\n"
        "1. Donne UNIQUEMENT le texte du résumé, sans aucun guillemet, sans préambule ni commentaire (ex: pas de 'Voici un résumé:').\n"
        "2. Ton professionnel, dynamique et fluide.\n"
    )
    if title:
        prompt += f"\nTitre de l'article : {title.strip()}\n"

    prompt += f"\nContenu de l'article :\n{cleaned_text}\n"

    last_error = None
    for candidate_name in model_candidates:
        try:
            model = genai.GenerativeModel(candidate_name)
            response = model.generate_content(prompt)
            if not response or not response.text:
                continue

            summary = response.text.strip()
            # Supprimer d'éventuels guillemets englobants
            if (summary.startswith('"') and summary.endswith('"')) or (summary.startswith('«') and summary.endswith('»')):
                summary = summary[1:-1].strip()
            return summary
        except Exception as exc:
            last_error = exc
            logger.warning(f"Modèle {candidate_name} indisponible ({exc}). Tentative avec le modèle suivant...")

    logger.error(f"Erreur lors de la génération du résumé avec Gemini: {last_error}", exc_info=True)
    raise last_error or RuntimeError("Impossible de générer le résumé.")

