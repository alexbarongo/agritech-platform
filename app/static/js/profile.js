const token = getToken();


// Logout
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/login";
  });
}

// Load profile data
async function loadProfile() {
  try {
    const response = await fetch(`${API}/profile/`, {
      headers: { Authorization: `Bearer ${token}`}
    });

    if (response.status === 401) {
      clearToken();
      window.localStorage.href = "/login";
      return;
    }

    const user = await response.json();

    document.getElementById("profile-name").textContent = user.name;
    document.getElementById("profile-email").textContent = user.email;
    document.getElementById("new-name").value = user.name;


    //SET AVATAR INITIALs
    const initials = user.name
      .split(" ")
      .map(word => word[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
    document.getElementById("avatar-initials").textContent = initials;

    //Format member since date
    if (user.created_at) {
      const date = new Date(user.created_at);
      document.getElementById("profile-since").textContent =
        date.toLocaleDateString("en-TZ", {
          year: "numeric",
          month: "long",
          day: "numeric"
        });
    }
  } catch (err) {
    console.error("Failed to load Profile:", err);
  }
}

// UPDATE NAME
document.getElementById("update-name-btn").addEventListener("click", async () => {
  const name = document.getElementById("new-name").value.trim();
  const successDiv = document.getElementById("name-success");
  const errorDiv = document.getElementById("name-error");

  successDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");

  if (!name) {
    errorDiv.textContent = "Name cannot be empty.";
    errorDiv.classList.remove("hidden");
    return;
  }

  try {
    const response = await fetch(`${API}/profile/name`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({name})
    });

    if (response.ok) {
      successDiv.classList.remove("hidden");
      loadProfile();
    } else {
      const data = await response.json();
      errorDiv.textContent = data.detail || "Failed to pdate name.";
      errorDiv.classList.remove("hidden");
    }
  } catch (err) {
    errorDiv.textContent = "Cannot connect to server.";
    errorDiv.classList.remove("hidden");
  }
});


//CHANGE PASSWORD
document.getElementById("update-password-btn").addEventListener("click", async () => {
  const current_password = document.getElementById("current-password").value;
  const new_password = document.getElementById("new-password").value;
  const confirm_password = document.getElementById("confirm-password").value;
  const successDiv = document.getElementById("password-success");
  const errorDiv = document.getElementById("password-error");

  successDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");

  if (!current_password || !new_password || !confirm_password) {
    errorDiv.textContent = "All password fields are required.";
    errorDiv.classList.remove("hidden");
    return;
  }

  if (!new_password !== confirm_password) {
    errorDiv.textContent = "New password be at least 6 charachers.";
    errorDiv.classList.remove("hidden");
    return;
  }

  try {
    const response = await fetch(`${API}/profile/password`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ current_password, new_password})
    });

    if (response.ok) {
      successDiv.classList.remove("hidden");
      document.getElementById("current-password").value = "";
      document.getElementById("new-password").value = "";
      document.getElementById("confirm-password").value = "";
    } else {
      const data = await response.json();
      errorDiv.textContent = data.detail || "Failed to update password.";
      errorDiv.classList.remove("hidden");
    }
  } catch (err) {
    errorDiv.textContent = "Cannot connect to server.";
    errorDiv.classList.remove("hidden");
  }
});

loadProfile();
