const token = getToken();

// Logout
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/login";
  });
}

// Load Crop Dropdown
async function loadCropDropdown() {
  const response = await fetch(`${API}/crops/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const crops = await response.json();
  const select = document.getElementById("expense-crop-id");
  select.innerHTML = '<option value="">Select a crop...</option>';
  crops.forEach((crop) => {
    select.innerHTML += `<option value="${crop.id}">${crop.name}</option>`;
  });
}

// Load Expenses
async function loadExpenses() {
  try {
    const response = await fetch(`${API}/expenses/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.status === 401) {
      clearToken();
      window.location.href = "/login";
      return;
    }

    const expenses = await response.json();
    const tbody = document.getElementById("expense-tbody");

    if (expenses.length === 0) {
      tbody.innerHTML = ` <tr><td colspan="4" class="empty-state">No expenses yet. Add your first expense.</td></tr>`;
      return;
    }

    tbody.innerHTML = expenses
      .map(
        (expense) => `
            <tr>
                <td><strong>${expense.crop}</strong></td>
                <td>${expense.item || "--"}</td>
                <td>${expense.amount ? "TZS " + expense.amount.toLocaleString() : "--"}</td>
                <td>
                    <button class="btn-action btn-delete" onclick="deleteExpense(${expense.id})">
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
    console.error("Failed to load expenses", err);
  }
}

// Open Modal
document.getElementById("add-expense-btn").addEventListener("click", () => {
  document.getElementById("add-expense-modal").classList.remove("hidden");
  loadCropDropdown();
});

// Cancel
document.getElementById("cancel-expense-btn").addEventListener("click", () => {
  document.getElementById("add-expense-modal").classList.add("hidden");
});

// Save Expense
document
  .getElementById("save-expense-btn")
  .addEventListener("click", async () => {
    const crop_id = document.getElementById("expense-crop-id").value;
    const item = document.getElementById("expense-item").value.trim();
    const amount = document.getElementById("expense-amount").value;
    const errorDiv = document.getElementById("expense-modal-error");

    // CHECKING WHAT IS BEING FILLED FOR POTENTIAL
    // console.log("crop_id:", crop_id);
    // console.log("item:", item);
    // console.log("amount:", amount);

    if (!crop_id || !item || !amount) {
      errorDiv.textContent = "All fields are requuired.";
      errorDiv.classList.remove("hidden");
      return;
    }

    const params = new URLSearchParams({ crop_id, item, amount });

    try {
      const response = await fetch(`${API}/expenses/?${params}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        document.getElementById("add-expense-modal").classList.add("hidden");
        document.getElementById("expense-crop-id").value = "";
        document.getElementById("expense-item").value = "";
        document.getElementById("expense-amount").value = "";
        loadExpenses();
      } else {
        const data = await response.json();
        errorDiv.textContent = data.detail || "Failed to add Expense.";
        errorDiv.classList.remove("hidden");
      }
    } catch (err) {
      errorDiv.textContent = "Cannot connect to server.";
      errorDiv.classList.remove("hidden");
    }
  });

//Delete Expense

function deleteExpense(expenseId) {
  document.getElementById("delete-expense-id").value = expenseId;
  document.getElementById("delete-expense-modal").classList.remove("hidden");
}

document
  .getElementById("cancel-delete-expense-btn")
  .addEventListener("click", () => {
    document.getElementById("delete-expense-modal").classList.add("hidden");
  });

document
  .getElementById("confirm-delete-expense-btn")
  .addEventListener("click", async () => {
    const expenseId = document.getElementById("delete-expense-id").value;

    try {
      const response = await fetch(`${API}/expenses/${expenseId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        document.getElementById("delete-expense-modal").classList.add("hidden");
        loadExpenses();
      }
    } catch (err) {
      console.error("Delete failed:", err);
    }
  });

loadExpenses();
