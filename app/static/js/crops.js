const token = getToken();

// Logout
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/login";
  });
}

// Load Crops
async function loadCrops() {
  try {
    const response = await fetch(`${API}/crops/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.status === 401) {
      cleanToken();
      window.location.href = "/login";
      return;
    }

    const crops = await response.json();
    const tbody = document.getElementById("crops-tbody");

    if (crops.length === 0) {
      tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="empty-state">
                        No crops yet. Add your first crop.
                    </td>
                </tr>
            `;
    }

    tbody.innerHTML = crops
      .map(
        (crop) => `
            <tr>
                <td><strong>${crop.name}</strong></td>
                <td>${crop.planting_date || "--"}</td>
                <td>${crop.field_size ? crop.field_size + " acres" : "--"}</td>
                <td>${crop.planted_quantity || "--"}</td>
                <td>${crop.harvest_date || "--"}</td>
                <td>${crop.harvest_quantity ? crop.harvest_quantity + "kg" : "--"}</td>
                <td>${crop.selling_price ? "TZS " + crop.selling_price.toLocaleString() : "--"}</td>
                <td>
                    <span class="status-budge ${crop.harvest_date ? "harvested" : "growing"}">
                        ${crop.harvest_date ? "Harvest" : "Growing"}
                    </span>
                </td>
                <td class="actions-buttons">
                    ${
                      !crop.harvest_date
                        ? `
                        <button class="btn-action btn-harvest" 
                            onclick="openHarvestModal(${crop.id})">
                            <img
                                src="/static/images/harvest.png"
                                style="width: 15px; height: 15px"
                            /> 
                            Harvest
                        </button>
                    `
                        : ""
                    }
                    <button class="btn-action btn-delete" 
                            onclick="openDeleteModal(${crop.id})">
                            <img
                                src="/static/images/delete.png"
                                style="width: 15px; height: 15px"
                            />
                            Delete
                    </button>
                </td>
            </tr>
            
            `,
      )
      .join("");
  } catch (err) {
    console.error("Failed to load crops:", err);
  }
}

// ADD CROP
document.getElementById("add-crop-btn").addEventListener("click", () => {
  document.getElementById("add-crop-modal").classList.remove("hidden");
});

document.getElementById("cancel-add-btn").addEventListener("click", () => {
  document.getElementById("add-crop-modal").classList.add("hidden");
});

document.getElementById("save-crop-btn").addEventListener("click", async () => {
  const name = document.getElementById("crop-name").value.trim();
  const planting_date = document.getElementById("crop-planting-date").value;
  const field_size = document.getElementById("crop-field-size").value;
  const planted_quantity = document.getElementById("crop-quantity").value;
  const errorDiv = document.getElementById("add-modal-error");

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
      document.getElementById("add-crop-modal").classList.add("hidden");
      document.getElementById("crop-name").value = "";
      document.getElementById("crop-planting-date").value = "";
      document.getElementById("crop-field-size").value = "";
      document.getElementById("crop-quantity").value = "";
      loadCrops();
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

// HARVEST MODAL
function openHarvestModal(cropId) {
  document.getElementById("harvest-crop-id").value = cropId;
  document.getElementById("harvest-modal").classList.remove("hidden");
}

document.getElementById("cancel-harvest-btn").addEventListener("click", () => {
  document.getElementById("harvest-modal").classList.add("hidden");
});

document
  .getElementById("save-harvest-btn")
  .addEventListener("click", async () => {
    const cropId = document.getElementById("harvest-crop-id").value;
    const qty = document.getElementById("harvest-qty").value;
    const date = document.getElementById("harvest-date").value;
    const price = document.getElementById("selling-price").value;
    const errorDiv = document.getElementById("harvest-modal-error");

    if (!qty || !date || !price) {
      errorDiv.textContent = "All harvest fields are required.";
      errorDiv.classList.remove("hidden");
      return;
    }

    const params = new URLSearchParams({
      crop_id: cropId,
      harvest_quantity: qty,
      harvest_date: date,
      selling_price: price,
    });

    try {
      const response = await fetch(`${API}/crops/harvest?${params}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        document.getElementById("harvest-modal").classList.add("hidden");
        loadCrops();
      } else {
        const data = await response.json();
        errorDiv.textContent = data.detail || "Failed to record harvest.";
        errorDiv.classList.remove("hidden");
      }
    } catch (err) {
      errorDiv.textContent = "Cannot connect to server.";
      errorDiv.classList.remove("hidden");
    }
  });

// DELETE MODAL
function openDeleteModal(cropId) {
  document.getElementById("delete-crop-id").value = cropId;
  document.getElementById("delete-modal").classList.remove("hidden");
}

document.getElementById("cancel-delete-btn").addEventListener("click", () => {
  document.getElementById("delete-modal").classList.add("hidden");
});

document
  .getElementById("confirm-delete-btn")
  .addEventListener("click", async () => {
    const cropId = document.getElementById("delete-crop-id").value;

    try {
      const response = await fetch(`${API}/crops/${cropId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        document.getElementById("delete-modal").classList.add("hidden");
        loadCrops();
      }
    } catch (err) {
      console.error("Delete failed:", err);
    }
  });

loadCrops();
