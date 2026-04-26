const token = getToken();


// Logout
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/login";
  });
}


// Load profile
async function loadProfile() {
    try {
        const response = await fetch(`/profile/`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (response.status === 401) {
            clearToken();
            window.location.href = "/login";
            return;
        }

        if (!response.ok) {
            console.error("Failed to load profile:", response.status);
            return;
        }

        const user = await response.json();

        if (!user || !user.name) {
            console.error("Invalid user data received:", user);
            return;
        }

        document.getElementById("profile-name").textContent = user.name;
        document.getElementById("profile-email").textContent = user.email;
        document.getElementById("new-name").value = user.name;

        const initials = user.name
            .split(" ")
            .map(word => word[0])
            .join("")
            .toUpperCase()
            .slice(0, 2);
        document.getElementById("avatar-initials").textContent = initials;

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
        console.error("Failed to load profile:", err);
    }
}

// Update name
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
        const response = await fetch(`/profile/name`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });

        if (response.ok) {
            successDiv.classList.remove("hidden");
            loadProfile();
        } else {
            const data = await response.json();
            errorDiv.textContent = data.detail || "Failed to update name.";
            errorDiv.classList.remove("hidden");
        }
    } catch (err) {
        errorDiv.textContent = "Cannot connect to server.";
        errorDiv.classList.remove("hidden");
    }
});

// Change password
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

    if (new_password !== confirm_password) {
        errorDiv.textContent = "New passwords do not match.";
        errorDiv.classList.remove("hidden");
        return;
    }

    if (new_password.length < 6) {
        errorDiv.textContent = "New password must be at least 6 characters.";
        errorDiv.classList.remove("hidden");
        return;
    }

    try {
        const response = await fetch(`/profile/password`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ current_password, new_password })
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
