const token = getToken();

// Logout
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/login";
  });
}

async function loadReports() {
  try {
    const response = await fetch(`${API}/reports/profit`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 401) {
      clearToken();
      window.localStorage.href = "/login";
      return;
    }
    const reports = await response.json();
    const tbody = document.getElementById("reports-tbody");

    if (reports.length === 0) {
      tbody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-state">
                    No report data yet. Add crops and record harvests.
                </td>
            </tr>`;
      return;
    }

    tbody.innerHTML = reports
      .map((report) => {
        const status =
          report.profit > 0
            ? "PROFIT"
            : report.profit < 0
              ? "LOSS"
              : "BREAK EVEN";
        const statusClass =
          report.profit > 0 ? "harvested" : report.profit < 0 ? "growing" : "";

        return `
            <tr>
                <td><strong>${report.crop}</strong></td>
                <td>${report.harvest_quantity ? report.harvest_quantity + " kg" : "--"}</td>
                <td>${report.selling_price ? "TZS" + report.selling_price.toLocaleString() : "--"}</td>
                <td>${report.revenue ? "TZS" + report.revenue.toLocaleString() : "--"}</td>
                <td>${report.total_expenses ? "TZS" + report.total_expenses.toLocaleString() : "--"}</td>
                <td>${report.profit ? "TZS" + report.profit.toLocaleString() : "--"}</td>
                <td>
                  <span class="status-badge ${statusClass}">${status}</span>
                </td>
            </tr>
      `;
      })
      .join("");
  } catch (err) {
    console.error("Failed to load report:", err);
  }
}

loadReports();
