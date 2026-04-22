# AgriTech Vertical Integration Limited

<p align="center">
  <img src="ATVI-logo.png"
       alt="AgriTech Vertical Integration Logo"
       width="120">
</p>

**AgriTech Vertical Integration Limited** is a technology-driven agricultural enterprise focused on transforming modern farming through **end-to-end supply chain control, data systems, and sustainable production methods**.

The company operates on a **vertical integration model**, meaning it manages multiple stages of the agricultural value chain — from production to distribution — within a single organization to ensure efficiency, quality, and profitability.

## 🎯 Vision

To build a fully integrated, technology-powered agricultural ecosystem that maximizes productivity, sustainability, and profitability from farm to market.

**One-line definition:**
**AgriTech Vertical Integration Limited is a data-driven agricultural company that controls the full farming value chain using technology to optimize production, reduce costs, and maximize profits.**

---

## 🧠 Core Concept

At its foundation, the company combines:

- **AgriTech innovation** (software + automation)
- **Farm operations management**
- **Supply chain ownership**

AgriTech refers to the use of technology to improve farming efficiency, sustainability, and productivity.

---

## ⚙️ What the Company Does

AgriTech Vertical Integration Limited operates across **three main layers** of the agricultural value chain:

### 1. 🌾 Production (Upstream)

- Crop cultivation (tomatoes, onions, fruits, vegetables, etc.)
- Smart farming practices with data tracking and optimization
- Future expansion: vertical farming / aeroponics systems

Modern agritech systems can use **up to 95% less water** and enable year-round production.

### 2. 🧾 Operations & Technology (Core Layer)

This is where the **Farm Manager CLI** (this project) lives — the company’s internal intelligence system.

### 3. 🚚 Distribution & Market (Downstream)

- Direct selling to markets, retailers, or consumers
- Elimination of middlemen
- Full control over pricing, quality, and traceability

Vertical integration delivers lower costs, higher margins, consistent quality, and complete product traceability.

---

## 💡 Key Value Proposition

- Full control of the entire agricultural pipeline
- Data-driven decision making
- Higher profitability through operational efficiency
- Sustainable farming practices
- Consistent product quality from farm to customer

---

## 🚀 The Project: Farm Manager CLI

**Farm Manager** is the flagship internal digital platform of AgriTech Vertical Integration Limited.

It turns traditional farming into a **data-driven business** by providing real-time visibility, automated analytics, and actionable insights across all farm operations.

### ✨ Core Features

- **Crop Records Management** — Track every crop from planting to harvest
- **Expense Tracking per Crop** — Granular cost allocation and monitoring
- **Profitability Analysis** — Real-time profit/loss calculations per crop and per season
- **Smart Alerts** — Overspending detection, critical thresholds, and reminders
- **Comprehensive Reporting & Analytics** — Summaries, trends, and exportable reports
- **Future Roadmap** — Dashboard web interface, automation, IoT integration, and predictive analytics

---

## 🛠️ Tech Stack & Architecture

| Layer             | Technology                             | Purpose                                         |
| ----------------- | -------------------------------------- | ----------------------------------------------- |
| **Language**      | Python 3.10+                           | Core application logic                          |
| **CLI Framework** | Typer (with Rich for beautiful output) | Modern, intuitive command-line interface        |
| **Data Layer**    | Pandas + CSV / SQLite                  | Fast in-memory analytics and persistent storage |
| **Configuration** | Pydantic + TOML                        | Type-safe settings management                   |
| **Visualization** | Rich + Tabulate                        | Terminal-friendly tables and dashboards         |
| **Testing**       | pytest                                 | Comprehensive test coverage                     |
| **Packaging**     | Poetry + setuptools                    | Easy installation and distribution              |

**Key Technical Highlights:**

- **Modular architecture** — Each command (`crop`, `expense`, `report`, `alert`) is a self-contained module for easy extension.
- **Data-driven design** — All business logic is built around pandas DataFrames for lightning-fast calculations.
- **Zero external dependencies for core functionality** — Runs offline on any machine with Python.
- **Extensible** — Designed from day one to evolve into a full web dashboard or integrate with IoT sensors and ERP systems.
- **Developer-friendly** — Clear separation of concerns, comprehensive type hints, and detailed logging.
