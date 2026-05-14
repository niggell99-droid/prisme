/* script.js - moderne, robuste et sécurisé
   - utilisation de defer dans HTML (donc DOM prêt)
   - vérifications DOM avant addEventListener
   - localStorage theme enregistré en JSON
   - overlay close on outside click + Escape
   - prevention scroll when nav/search open
*/

(() => {
  // Helpers
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));
  const body = document.body;

  // Elements
  const hamburger = $(".hamburger");
  const navlinks = document.getElementById("primary-navigation");
  const searchToggle = $(".search-toggle");
  const searchOverlay = $("#search-overlay");
  const closeSearchBtn = $("#close-search-overlay");
  const searchFullInput = $("#search-full");
  const modeToggle = $(".mode-toggle");

  // Utilities
  const NO_SCROLL = "no-scroll";
  const DARK_KEY = "prisme_dark_mode";
  const MOBILE_BREAKPOINT = 900;

  function setNoScroll(enabled) {
    if (enabled) body.classList.add(NO_SCROLL);
    else body.classList.remove(NO_SCROLL);
  }

  // ===== Theme (dark/light) =====
  function applyTheme(isDark) {
    if (isDark) {
      body.classList.add("dark-mode");
      if (modeToggle) modeToggle.classList.add("active");
      modeToggle && modeToggle.setAttribute("aria-pressed", "true");
    } else {
      body.classList.remove("dark-mode");
      if (modeToggle) modeToggle.classList.remove("active");
      modeToggle && modeToggle.setAttribute("aria-pressed", "false");
    }
  }

  function initTheme() {
    try {
      const raw = localStorage.getItem(DARK_KEY);
      const saved = raw !== null ? JSON.parse(raw) : null;
      if (typeof saved === "boolean") {
        applyTheme(saved);
      }
    } catch (err) {
      console.warn("Erreur lecture thème:", err);
    }
  }

  function toggleTheme() {
    const isDark = !body.classList.contains("dark-mode");
    applyTheme(isDark);
    try {
      localStorage.setItem(DARK_KEY, JSON.stringify(isDark));
    } catch (e) {}
  }

  // ===== Search overlay (version animée et optimisée) =====
  function openSearch() {
    if (!searchOverlay || !searchToggle) return;
    searchOverlay.classList.add("open");
    searchOverlay.classList.remove("closing");
    searchOverlay.setAttribute("aria-hidden", "false");
    searchToggle.setAttribute("aria-expanded", "true");
    setNoScroll(true);
    setTimeout(() => {
      searchFullInput && searchFullInput.focus();
    }, 180);
  }

  function closeSearch() {
    if (!searchOverlay || !searchToggle) return;

    // Ajout d’un effet de rebond fluide
    searchOverlay.classList.add("closing");
    searchOverlay.addEventListener(
      "animationend",
      () => {
        searchOverlay.classList.remove("open", "closing");
        searchOverlay.setAttribute("aria-hidden", "true");
        searchToggle.setAttribute("aria-expanded", "false");
        setNoScroll(false);
        if (searchFullInput) searchFullInput.value = "";
      },
      { once: true },
    );
  }

  // ===== Init général =====
  function init() {
    initTheme();

    // Theme switch
    if (modeToggle) {
      modeToggle.addEventListener("click", toggleTheme);
      modeToggle.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggleTheme();
        }
      });
    }

    // Search overlay
    if (searchToggle) searchToggle.addEventListener("click", openSearch);
    if (closeSearchBtn) closeSearchBtn.addEventListener("click", closeSearch);
    if (searchOverlay) {
      searchOverlay.addEventListener("click", (e) => {
        const inner = e.currentTarget.querySelector(".search-overlay-inner");
        if (!inner || !inner.contains(e.target)) closeSearch();
      });
    }

    // Inline search
    const inlineSearchBtn = $("#search-inline-btn");
    const inlineSearchInput = $("#search");
    if (inlineSearchBtn && inlineSearchInput) {
      inlineSearchBtn.addEventListener("click", (e) => {
        e.preventDefault();
        const q = inlineSearchInput.value.trim();
        if (q)
          window.location.href = `./search.html?q=${encodeURIComponent(q)}`;
        else inlineSearchInput.focus();
      });
    }

    // ===== Navigation (Desktop + Mobile) =====
    const mobileMenu = $(".mobile-menu");
    const mobileMenuOverlay = $(".mobile-menu-overlay");
    const hamburgerMini = $(".hamburger-mini");
    const closeMobileMenuBtn = $(".close-mobile-menu");
    const navOverlay = $(".nav-overlay");

    function openDesktopNav() {
      if (!navlinks || !hamburger) return;
      navlinks.classList.add("open");
      hamburger.classList.add("open");
      hamburger.setAttribute("aria-expanded", "true");
      if (navOverlay) navOverlay.classList.add("active");
      setNoScroll(true);
      if (mobileMenu?.classList.contains("open")) closeMobileMenu();
    }

    function closeDesktopNav() {
      if (!navlinks || !hamburger) return;
      navlinks.classList.remove("open");
      hamburger.classList.remove("open");
      hamburger.setAttribute("aria-expanded", "false");
      if (navOverlay) navOverlay.classList.remove("active");
      setNoScroll(false);
    }

    function toggleDesktopNav() {
      if (!navlinks) return;
      if (navlinks.classList.contains("open")) closeDesktopNav();
      else openDesktopNav();
    }

    function openMobileMenu() {
      if (!mobileMenu || !mobileMenuOverlay) return;
      mobileMenu.classList.add("open");
      mobileMenuOverlay.classList.add("active");
      setNoScroll(true);
      if (navlinks?.classList.contains("open")) closeDesktopNav();
    }

    function closeMobileMenu() {
      if (!mobileMenu || !mobileMenuOverlay) return;
      mobileMenu.classList.add("closing");
      mobileMenu.addEventListener(
        "animationend",
        () => {
          mobileMenu.classList.remove("closing", "open");
        },
        { once: true },
      );
      mobileMenuOverlay.classList.remove("active");
      setNoScroll(false);
    }

    // Gestion du hamburger principal
    if (hamburger) {
      hamburger.addEventListener("click", () => {
        if (window.innerWidth <= MOBILE_BREAKPOINT) {
          mobileMenu?.classList.contains("open")
            ? closeMobileMenu()
            : openMobileMenu();
        } else {
          toggleDesktopNav();
        }
      });
    }

    // Hamburger mini (navbar du bas)
    //const hamburgerMini = $(".hamburger-mini");
    if (hamburgerMini) {
      hamburgerMini.addEventListener("click", () => {
        if (window.innerWidth <= MOBILE_BREAKPOINT) openMobileMenu();
        else toggleDesktopNav();
      });
    }

    // Bouton Partager (navbar du bas)
    const shareBtn = $("#share-button");
    if (shareBtn) {
      shareBtn.addEventListener("click", async () => {
        if (navigator.share) {
          try {
            await navigator.share({
              title: document.title,
              text: "Découvrez cet article sur Prisme !",
              url: window.location.href,
            });
          } catch (err) {
            // L'utilisateur a annulé ou erreur silencieuse
          }
        } else {
          // Fallback: copier l'URL
          try {
            await navigator.clipboard.writeText(window.location.href);
            // On pourrait utiliser un toast plus élégant si dispo
            alert("Lien copié dans le presse-papier !");
          } catch (err) {
            console.error("Échec de la copie:", err);
          }
        }
      });
    }

    // Fermetures
    if (closeMobileMenuBtn)
      closeMobileMenuBtn.addEventListener("click", closeMobileMenu);
    if (mobileMenuOverlay)
      mobileMenuOverlay.addEventListener("click", closeMobileMenu);
    if (navOverlay) navOverlay.addEventListener("click", closeDesktopNav);

    // Close on Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        if (mobileMenu?.classList.contains("open")) closeMobileMenu();
        if (navlinks?.classList.contains("open")) closeDesktopNav();
        if (searchOverlay?.classList.contains("open")) closeSearch();
      }
    });

    // Resize adaptation
    window.addEventListener(
      "resize",
      () => {
        if (
          window.innerWidth > MOBILE_BREAKPOINT &&
          mobileMenu?.classList.contains("open")
        ) {
          closeMobileMenu();
        } else if (
          window.innerWidth <= MOBILE_BREAKPOINT &&
          navlinks?.classList.contains("open")
        ) {
          closeDesktopNav();
        }
      },
      { passive: true },
    );

    // Fermer nav desktop quand un lien est cliqué (mobile)
    if (navlinks) {
      navlinks.addEventListener("click", (e) => {
        const target = e.target.closest("a");
        if (target && navlinks.classList.contains("open")) closeDesktopNav();
      });
    }
  }

  // DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

// ===== Barre de progression du scroll (version fluide) =====
(() => {
  const bar = document.querySelector(".scroll-progress");
  if (!bar) return;

  let currentWidth = 0;
  let targetWidth = 0;
  let ticking = false;

  function updateTarget() {
    const scrollTop =
      document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight =
      document.documentElement.scrollHeight -
      document.documentElement.clientHeight;
    targetWidth = (scrollTop / scrollHeight) * 100;
    requestTick();
  }

  function requestTick() {
    if (!ticking) {
      requestAnimationFrame(animate);
      ticking = true;
    }
  }

  function animate() {
    // interpolation douce (easing)
    const speed = 0.15; // 0.1 à 0.3 selon fluidité souhaitée
    currentWidth += (targetWidth - currentWidth) * speed;

    bar.style.width = currentWidth.toFixed(2) + "%";

    if (Math.abs(targetWidth - currentWidth) > 0.1) {
      requestAnimationFrame(animate);
    } else {
      ticking = false;
    }
  }

  window.addEventListener("scroll", updateTarget, { passive: true });
})();
