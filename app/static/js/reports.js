const token = getToken();

// Set current date
const dateEl = document.getElementById("current-date");
if (dateEl) {
  const now = new Date();
  dateEl.textContent = now.toLocaleDateString("en-TZ", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// Logout
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/login";
  });
}
