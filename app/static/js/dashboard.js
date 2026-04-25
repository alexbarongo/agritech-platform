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
      totalHarvest > 0 ? `${totalHarvest.toFixed(1)} kg` : "0 kg";

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
      `TZS ${total.toLocaleString()}`;
  } catch (err) {
    console.error("Expenses load failed:", err);
  }
}

//Fetch Net Profit
async function loadProfitReport() {
  try {
    const response = await fetch(`${API}/reports/profit`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) return;

    const data = await response.json();
    const totalProfit = data.reduce((sum, row) => sum + row.profit, 0);
    const profitEl = document.getElementById("net-profit");

    profitEl.textContent = `TZS ${totalProfit.toLocaleString()}`;
    profitEl.style.color = totalProfit >= 0 ? "#276749" : "#c53030";
  } catch (err) {
    console.error("Profit load failed:", err);
  }
}
//Fetch Farmer's Name
async function loadFarmerName() {
  try {
    const response = await fetch(`${API}/profile/`, {
      headers: { Authorization: `Bearer ${token}`}
    });
    if (response.ok) {
      const user = await response.json();
      const firstName = user.name.split(" ")[0];
      document.getElementById("farmer-name").textContent = firstName;
    }
  } catch (err) {
    console.error("Failed to load farmer name:", err);
  }
}

// Load everything
loadDashboard();
loadExpenses();
loadProfitReport();
loadFarmerName();
