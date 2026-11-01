(function () {
  'use strict';

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function getArticleContent() {
    // 1. Essayer de récupérer le contenu depuis l'instance CKEditor 5
    const editableEl = document.querySelector('.django_ckeditor_5 .ck-editor__editable, .ck-editor__editable');
    if (editableEl && editableEl.innerHTML.trim().length > 0) {
      return editableEl.innerHTML;
    }

    // 2. Si django_ckeditor_5 expose window.editors
    if (window.editors) {
      for (const key in window.editors) {
        if (window.editors[key] && typeof window.editors[key].getData === 'function') {
          const data = window.editors[key].getData();
          if (data && data.trim().length > 0) {
            return data;
          }
        }
      }
    }

    // 3. Repli vers le textarea source
    const contentTextarea = document.querySelector('#id_content');
    if (contentTextarea && contentTextarea.value.trim().length > 0) {
      return contentTextarea.value;
    }

    return '';
  }

  function getEndpointUrl() {
    const pathname = window.location.pathname;
    // Remplace la fin de l'URL (/add/ ou /123/change/) par /generate-summary/
    if (pathname.includes('/article/')) {
      return pathname.replace(/\/article\/.+$/, '/article/generate-summary/');
    }
    return '/admin/blog/article/generate-summary/';
  }

  function initSummaryButton() {
    const excerptTextarea = document.querySelector('#id_excerpt');
    if (!excerptTextarea) {
      return;
    }

    // Vérifier si le bouton est déjà injecté
    if (document.querySelector('#ai-generate-summary-btn')) {
      return;
    }

    // Création du bloc de contrôle
    const wrapper = document.createElement('div');
    wrapper.className = 'ai-summary-wrapper';
    wrapper.innerHTML = `
      <div class="ai-summary-header">
        <button type="button" id="ai-generate-summary-btn" class="ai-summary-btn">
          <span class="ai-icon">✨</span>
          <span class="ai-btn-text">Générer le résumé avec Gemini IA</span>
        </button>
        <span class="ai-summary-badge">Généré 1 seule fois • Modifiable manuellement</span>
      </div>
      <div id="ai-summary-feedback" class="ai-summary-feedback"></div>
    `;

    // Insertion juste au-dessus du textarea excerpt
    excerptTextarea.parentNode.insertBefore(wrapper, excerptTextarea);

    const btn = document.querySelector('#ai-generate-summary-btn');
    const feedback = document.querySelector('#ai-summary-feedback');

    function showFeedback(type, message) {
      feedback.className = `ai-summary-feedback ${type}`;
      feedback.textContent = message;
      feedback.style.display = 'block';
    }

    function hideFeedback() {
      feedback.style.display = 'none';
      feedback.textContent = '';
    }

    btn.addEventListener('click', async function () {
      const content = getArticleContent();
      const titleInput = document.querySelector('#id_title');
      const title = titleInput ? titleInput.value : '';

      if (!content || content.trim().length < 30) {
        showFeedback('error', '⚠️ Veuillez rédiger ou coller le contenu de l\'article dans l\'éditeur avant de générer le résumé.');
        return;
      }

      // Si le champ excerpt contient déjà du texte, demander confirmation
      if (excerptTextarea.value.trim().length > 0) {
        const confirmOverwrite = window.confirm(
          "Un résumé existe déjà dans ce champ. Souhaitez-vous le remplacer par une nouvelle version générée par l'IA ?"
        );
        if (!confirmOverwrite) {
          return;
        }
      }

      hideFeedback();
      const originalHtml = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `<span class="ai-spinner"></span> <span>Génération du résumé en cours...</span>`;

      const csrfToken = getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]')?.value;

      try {
        const response = await fetch(getEndpointUrl(), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({
            title: title,
            content: content
          })
        });

        const data = await response.json();

        if (response.ok && data.success) {
          excerptTextarea.value = data.summary;
          // Déclencher les événements change / input pour les scripts d'admin
          excerptTextarea.dispatchEvent(new Event('input', { bubbles: true }));
          excerptTextarea.dispatchEvent(new Event('change', { bubbles: true }));

          showFeedback('success', '✅ Résumé généré avec succès par Gemini ! Vous pouvez l\'ajuster ou enregistrer l\'article.');
        } else {
          const errMsg = data.error || 'Une erreur est survenue lors de la génération.';
          showFeedback('error', `❌ ${errMsg}`);
        }
      } catch (err) {
        console.error('Erreur appel IA:', err);
        showFeedback('error', '❌ Impossible de contacter le serveur pour générer le résumé.');
      } finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
      }
    });
  }

  // Initialisation à l'événement adéquat
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSummaryButton);
  } else {
    initSummaryButton();
  }

  // Cas spécifique Unfold ou navigation dynamique
  window.addEventListener('load', initSummaryButton);
})();
