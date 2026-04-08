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

// Fetch crops and populate dashboard
async function loadDashboard() {
  try {
    const response = await fetch(`${API}/crops/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 401) {
      clearToken();
      window.location.href = "/login";
      return;
    }

    const crops = await response.json();

    //Update total harvest
    document.getElementById("total-crops").textContent = crops.length;

    // Calculate total harvest
    const totalHarvest = crops.reduce((sum, crop) => {
      return sum + (crop.harvest_quantity || 0);
    }, 0);
    document.getElementById("total-harvest").textContent =
      totalHarvest > 0 ? `${totalHarvest.toFixed(1)} kg` : "0 kg;";

    // Populate crops table
    const tbody = document.getElementById("crops-table-body");
    if (crops.length === 0) {
      tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-state">
                        No crops yet. Add your first crop to get started.
                    </td>
                </tr>`;
      return;
    }

    tbody.innerHTML = crops
      .map(
        (crop) => `
            <tr>
                <td><strong>${crop.name}<strong></td>
                <td>${crop.planting_date || "Not recorded"}</td>
                <td>${crop.field_size ? crop.field_size + " acres" : "Not recorded"}</td>
                <td>${crop.harvest_date || "Pending"}</td>
                <td>
                    <span class="status-badge ${crop.harvest_date ? "harvested" : "growing"}">
                        ${crop.harvest_date ? "Harvested" : "Growing"}
                    </span>
                </td>
            </tr>
            `,
      )
      .join("");
  } catch (err) {
    console.error("Dashboard load failed:", err);
  }
}

// Fetch expenses for summary
async function loadExpenses() {
  try {
    const response = await fetch(`${API}/expenses/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const expenses = await response.json();

    const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    document.getElementById("total-expenses").textContent =
      `TZ ${total.toLocaleString()}`;
  } catch (err) {
    console.error("Expenses load failed:", err);
  }
}

// Add crop modal
const addCropBtn = document.getElementById("add-crop-btn");
const modal = document.getElementById("add-crop-modal");
const cancelBtn = document.getElementById("cancel-crop-btn");
const saveCropBtn = document.getElementById("save-crop-btn");

if (addCropBtn) {
  addCropBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
  });
}

if (cancelBtn) {
  cancelBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
  });
}

if (saveCropBtn) {
  saveCropBtn.addEventListener("click", async () => {
    const name = document.getElementById("crop-name").value.trim();
    const planting_date = document.getElementById("crop-planting-date").value;
    const field_size = document.getElementById("crop-field-size").value;
    const planted_quantity = document.getElementById("crop-quantity").value;
    const errorDiv = document.getElementById("modal-error");

    if (!name) {
      errorDiv.textContent = "Crop name is required.";
      errorDiv.classList.remove("hidden");
      return;
    }

    const params = new URLSearchParams({ name });
    if (planting_date) params.append("planting_date", planting_date);
    if (field_size) params.append("field_size", field_size);
    if (planted_quantity) params.append("planted_quantity", planted_quantity);

    try {
      const response = await fetch(`${API}/crops/?${params}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        modal.classList.add("hidden");
        loadDashboard();
      } else {
        const data = await response.json();
        errorDiv.textContent = data.detail || "Failed to add crop.";
        errorDiv.classList.remove("hidden");
      }
    } catch (err) {
      errorDiv.textContent = "Cannot connect to server.";
      errorDiv.classList.remove("hidden");
    }
  });
}

// Load everything
loadDashboard();
loadExpenses();
