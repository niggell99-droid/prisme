import { initOAuth } from "./oauth.js";

document.addEventListener("DOMContentLoaded", () => {
  initOAuth();

  const logoutBtns = document.querySelectorAll("#logout-btn, #logout-btn-2");
  logoutBtns.forEach(btn => btn.addEventListener("click", logout));

  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("change", () => {
      document.body.classList.toggle("dark-mode", themeToggle.checked);
      localStorage.setItem("darkMode", themeToggle.checked);
    });

    // Charger état sauvegardé
    const saved = localStorage.getItem("darkMode") === "true";
    themeToggle.checked = saved;
    document.body.classList.toggle("dark-mode", saved);
  }

  // Exemple d’utilisateur simulé
  const user = JSON.parse(localStorage.getItem("user")) || {
    name: "Utilisateur Prisme",
    email: "user@prisme.com",
    avatar: "../assets/images/avatar-default.svg"
  };

  document.getElementById("user-name").textContent = user.name;
  document.getElementById("user-email").textContent = user.email;
  document.getElementById("user-avatar").src = user.avatar;
});

function logout() {
  localStorage.removeItem("user");
  window.location.href = "../auth/signin.html";
}


import { initOAuth } from "./oauth.js";

document.addEventListener("DOMContentLoaded", () => {
  initOAuth();

  const logoutBtns = document.querySelectorAll("#logout-btn, #logout-btn-2");
  logoutBtns.forEach(btn => btn.addEventListener("click", logout));

  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("change", () => {
      document.body.classList.toggle("dark-mode", themeToggle.checked);
      localStorage.setItem("darkMode", themeToggle.checked);
    });

    const saved = localStorage.getItem("darkMode") === "true";
    themeToggle.checked = saved;
    document.body.classList.toggle("dark-mode", saved);
  }

  // Exemple d’utilisateur simulé
  const user = JSON.parse(localStorage.getItem("user")) || {
    name: "Isabelle Malaji",
    email: "isabelle@prisme.com",
    avatar: "" // Laisse vide pour déclencher la génération auto
  };

  document.getElementById("user-name").textContent = user.name;
  document.getElementById("user-email").textContent = user.email;

  const avatarImg = document.getElementById("user-avatar");

  if (user.avatar) {
    avatarImg.src = user.avatar;
  } else {
    avatarImg.src = generateAvatar(user.name);
  }
});

function logout() {
  localStorage.removeItem("user");
  window.location.href = "../auth/signin.html";
}

/**
 * Génère un avatar SVG basé sur les initiales de l'utilisateur
 */
function generateAvatar(name) {
  const initials = name
    .split(" ")
    .map(part => part[0]?.toUpperCase() || "")
    .slice(0, 2)
    .join("");

  const gradients = [
    ["#4f46e5", "#a855f7"],
    ["#0ea5e9", "#6b21a8"],
    ["#3b82f6", "#9333ea"],
    ["#10b981", "#3b82f6"]
  ];
  const [start, end] = gradients[Math.floor(Math.random() * gradients.length)];

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${start}"/>
          <stop offset="100%" stop-color="${end}"/>
        </linearGradient>
      </defs>
      <circle cx="64" cy="64" r="60" fill="url(#grad)" />
      <text x="50%" y="54%" text-anchor="middle" font-size="48" font-family="Inter, Arial, sans-serif" fill="#fff" dy=".3em">${initials}</text>
    </svg>
  `;

  // Convertit le SVG en data URI
  return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)));
}


document.addEventListener("DOMContentLoaded", () => {
  const user = JSON.parse(localStorage.getItem("user")) || {
    name: "Isabelle Malaji",
    email: "isabelle@prisme.com",
    avatar: "" // vide => génère un avatar dynamique
  };

  const nameEl = document.getElementById("user-name");
  const emailEl = document.getElementById("user-email");
  const avatarEl = document.getElementById("user-avatar");

  if (nameEl) nameEl.textContent = user.name;
  if (emailEl) emailEl.textContent = user.email;

  // Si pas d'avatar => générer dynamiquement
  const avatarSrc = user.avatar || generateAvatar(user.name);
  if (avatarEl) {
    avatarEl.src = avatarSrc;
    avatarEl.classList.add("avatar-animate");
  }

  // Thème clair/sombre
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("change", () => {
      document.body.classList.toggle("dark-mode", themeToggle.checked);
      localStorage.setItem("darkMode", themeToggle.checked);
    });

    const saved = localStorage.getItem("darkMode") === "true";
    themeToggle.checked = saved;
    document.body.classList.toggle("dark-mode", saved);
  }
});

/**
 * Génère un avatar SVG en fonction du nom (initiales)
 */
function generateAvatar(name) {
  const initials = name
    .split(" ")
    .map(part => part[0]?.toUpperCase() || "")
    .slice(0, 2)
    .join("");

  const gradients = [
    ["#4f46e5", "#a855f7"],
    ["#0ea5e9", "#6b21a8"],
    ["#3b82f6", "#9333ea"],
    ["#10b981", "#3b82f6"],
    ["#6366f1", "#ec4899"]
  ];
  const [start, end] = gradients[Math.floor(Math.random() * gradients.length)];

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${start}"/>
          <stop offset="100%" stop-color="${end}"/>
        </linearGradient>
      </defs>
      <circle cx="64" cy="64" r="60" fill="url(#grad)" />
      <text x="50%" y="54%" text-anchor="middle" font-size="48" font-family="Inter, Arial, sans-serif" fill="#fff" dy=".3em">${initials}</text>
    </svg>
  `;
  return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)));
}


// === Gestion des avatars personnalisés ===
const avatarEl = document.getElementById("user-avatar");
const uploadInput = document.getElementById("avatar-upload");
const resetBtn = document.getElementById("reset-avatar");

if (uploadInput) {
  uploadInput.addEventListener("change", handleAvatarUpload);
}
if (resetBtn) {
  resetBtn.addEventListener("click", resetAvatar);
}

function handleAvatarUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (event) {
    const base64 = event.target.result;
    avatarEl.src = base64;
    avatarEl.classList.add("avatar-animate");

    // Sauvegarde dans localStorage
    const user = JSON.parse(localStorage.getItem("user")) || {};
    user.avatar = base64;
    localStorage.setItem("user", JSON.stringify(user));
  };
  reader.readAsDataURL(file);
}

function resetAvatar() {
  const user = JSON.parse(localStorage.getItem("user")) || {};
  user.avatar = "";
  localStorage.setItem("user", JSON.stringify(user));

  const newAvatar = generateAvatar(user.name || "Utilisateur");
  avatarEl.src = newAvatar;
  avatarEl.classList.add("avatar-animate");
}

document.addEventListener("DOMContentLoaded", () => {
  // Inject header/footer
  fetch("../header.html").then(r => r.text()).then(h => document.querySelector("#header-placeholder").innerHTML = h);
  fetch("../footer.html").then(r => r.text()).then(f => document.querySelector("#footer-placeholder").innerHTML = f);

  // Avatar preview
  const avatarInput = document.getElementById("avatar-upload");
  const avatarPreview = document.getElementById("avatar-preview");
  let avatarBase64 = null;

  avatarInput?.addEventListener("change", e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      avatarBase64 = reader.result;
      avatarPreview.src = avatarBase64;
    };
    reader.readAsDataURL(file);
  });

  // Champs de profil
  const nameField = document.getElementById("fullname");
  const emailField = document.getElementById("email");
  const bioField = document.getElementById("bio");

  // Charger le profil existant
  const userData = JSON.parse(localStorage.getItem("prisme_user") || "{}");
  if (userData.name) nameField.value = userData.name;
  if (userData.email) emailField.value = userData.email;
  if (userData.bio) bioField.value = userData.bio;
  if (userData.avatar) avatarPreview.src = userData.avatar;

  // Enregistrement du profil
  document.querySelector("#profile form")?.addEventListener("submit", e => {
    e.preventDefault();
    const updatedUser = {
      name: nameField.value.trim() || "Nom d’utilisateur",
      email: emailField.value.trim(),
      bio: bioField.value.trim(),
      avatar: avatarBase64 || userData.avatar || "../assets/img/avatar-default.png",
      domain: userData.domain || "Génie mécanique",
      location: userData.location || "RDC"
    };
    localStorage.setItem("prisme_user", JSON.stringify(updatedUser));
    alert("✅ Profil mis à jour avec succès !");
  });

  // === Préférences utilisateur ===
  const darkToggle = document.getElementById("dark-mode-toggle");
  const langSelect = document.getElementById("language");
  const emailNotif = document.getElementById("email-notifs");
  const compactMode = document.getElementById("compact-mode");

  const prefs = JSON.parse(localStorage.getItem("prisme_prefs") || "{}");
  darkToggle.checked = prefs.darkMode || false;
  langSelect.value = prefs.language || "fr";
  emailNotif.checked = prefs.emailNotif || false;
  compactMode.checked = prefs.compactMode || false;
  document.body.classList.toggle("dark-mode", prefs.darkMode);

  darkToggle.addEventListener("change", e => {
    document.body.classList.toggle("dark-mode", e.target.checked);
  });

  document.querySelector("#preferences .btn-save")?.addEventListener("click", e => {
    e.preventDefault();
    const updatedPrefs = {
      darkMode: darkToggle.checked,
      language: langSelect.value,
      emailNotif: emailNotif.checked,
      compactMode: compactMode.checked
    };
    localStorage.setItem("prisme_prefs", JSON.stringify(updatedPrefs));
    alert("✅ Préférences enregistrées !");
  });
});


document.addEventListener("DOMContentLoaded", () => {
  // Inject header/footer
  fetch("../header.html").then(r => r.text()).then(h => document.querySelector("#header-placeholder").innerHTML = h);
  fetch("../footer.html").then(r => r.text()).then(f => document.querySelector("#footer-placeholder").innerHTML = f);

  // Charger les infos utilisateur depuis localStorage
  const user = JSON.parse(localStorage.getItem("prisme_user") || "{}");

  document.getElementById("user-name").textContent = user.name || "Nom d’utilisateur";
  document.getElementById("user-bio").textContent = user.bio || "Aucune bio disponible.";
  document.getElementById("user-domain").textContent = user.domain ? `Domaine : ${user.domain}` : "Domaine : Génie mécanique";
  document.getElementById("user-location").textContent = user.location || "Localisation inconnue";
  document.getElementById("user-avatar").src = user.avatar || "../assets/img/avatar-default.png";

  // Mise à jour dynamique de l’avatar
  const avatarInput = document.getElementById("avatar-change");
  avatarInput?.addEventListener("change", e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result;
      document.getElementById("user-avatar").src = base64;
      user.avatar = base64;
      localStorage.setItem("prisme_user", JSON.stringify(user));
    };
    reader.readAsDataURL(file);
  });

  // Gestion des onglets
  const tabs = document.querySelectorAll(".tab-btn");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach(btn => {
    btn.addEventListener("click", () => {
      tabs.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      contents.forEach(c => c.classList.remove("active"));
      const id = btn.dataset.tab;
      document.getElementById(`tab-${id}`).classList.add("active");
    });
  });
});
