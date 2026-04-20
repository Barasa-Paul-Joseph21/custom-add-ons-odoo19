# 📦 RFQ Multi-Vendor Bidding

> An Odoo 19 custom module that extends the **Purchases (RFQ)** module with multi-vendor bidding, bid comparison, winner selection, and a purchase request approval workflow.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Module Architecture](#module-architecture)
- [Data Models](#data-models)
- [Workflow](#workflow)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

In standard Odoo, a **Request for Quotation (RFQ)** is sent to a single vendor at a time. This module extends that functionality to support a **multi-vendor bidding process**, enabling procurement teams to:

- Invite multiple vendors to bid on a single RFQ
- Collect, compare, and evaluate competing bids
- Select a winning bid and seamlessly convert it into a confirmed Purchase Order
- Manage the entire lifecycle through an internal **Purchase Request** approval workflow

This is ideal for organisations that require competitive procurement, transparent vendor selection, and auditable purchasing workflows.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Vendor RFQ** | Attach multiple vendors to a single RFQ and dispatch bid requests to all of them simultaneously |
| **Vendor Bid Management** | Each vendor submits a bid with pricing and notes; bids are tracked with statuses (`Draft`, `Submitted`, `Accepted`, `Rejected`) |
| **Bid Comparison** | View all bids side-by-side within the RFQ form to make informed procurement decisions |
| **Winner Selection** | Select the best bid as the winner; the RFQ converts into a confirmed Purchase Order for that vendor |
| **Purchase Request Workflow** | Internal users raise purchase requests that go through an approval process before generating RFQs |
| **Seamless Integration** | Built on top of Odoo's native `purchase` module using model inheritance — no core modifications |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **ERP Framework** | [Odoo 19 (Community / Enterprise)](https://www.odoo.com/) |
| **Backend Language** | Python 3.10+ |
| **ORM** | Odoo ORM (Active Record pattern) |
| **Frontend / Views** | Odoo QWeb XML views |
| **Database** | PostgreSQL 14+ |
| **Web Server** | Werkzeug (bundled with Odoo) |
| **Package Manager** | pip / apt |
| **Version Control** | Git |

---

## Module Architecture

The module follows Odoo's standard addon architecture and uses **model inheritance** (`_inherit`) to extend existing models without modifying Odoo core source code.

```
┌─────────────────────┐
│   Purchase Request   │  (New model: purchase.request)
│  Draft → Approved    │
└────────┬────────────┘
         │ generates
         ▼
┌─────────────────────┐
│   Purchase Order     │  (Inherited: purchase.order)
│   (RFQ - Multi)      │◄──── vendor_ids (Many2many → res.partner)
└────────┬────────────┘
         │ bid_ids (One2many)
         ▼
┌─────────────────────┐
│    Vendor Bid        │  (New model: vendor.bid)
│  Draft → Submitted   │
│  → Accepted/Rejected │
└─────────────────────┘
```

---

## Data Models

### `purchase.order` *(inherited)*

Extended fields added to the existing RFQ/Purchase Order model:

| Field | Type | Description |
|-------|------|-------------|
| `is_multi_vendor` | Boolean | Toggle to enable multi-vendor bidding mode |
| `vendor_ids` | Many2many → `res.partner` | List of vendors invited to bid |
| `bid_ids` | One2many → `vendor.bid` | Bids received for this RFQ |
| `request_id` | Many2one → `purchase.request` | Originating purchase request |
| `winning_bid_id` | Many2one → `vendor.bid` | The selected winning bid |

### `vendor.bid` *(new model)*

| Field | Type | Description |
|-------|------|-------------|
| `order_id` | Many2one → `purchase.order` | Parent RFQ |
| `vendor_id` | Many2one → `res.partner` | Bidding vendor |
| `amount` | Float | Total bid amount |
| `notes` | Text | Vendor comments or remarks |
| `state` | Selection | `draft` / `submitted` / `accepted` / `rejected` |

### `purchase.request` *(new model)*

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char (auto-sequence) | Request reference (e.g., `PR00001`) |
| `requested_by` | Many2one → `res.users` | Employee who raised the request |
| `product_ids` | Many2many → `product.product` | Products being requested |
| `rfq_ids` | One2many → `purchase.order` | RFQs generated from this request |
| `state` | Selection | `draft` / `approved` / `rfq_created` / `done` |

---

## Workflow

```
 ┌──────────┐     Approve     ┌──────────┐    Generate RFQ    ┌──────────────┐
 │  Draft   │ ──────────────► │ Approved │ ─────────────────► │ RFQ Created  │
 │ (Request)│                 │          │                    │ (Multi-Vendor)│
 └──────────┘                 └──────────┘                    └──────┬───────┘
                                                                     │
                                                          Vendors submit bids
                                                                     │
                                                                     ▼
                              ┌──────────┐   Select Winner   ┌──────────────┐
                              │   Done   │ ◄──────────────── │Bids Collected│
                              │ (PO)     │                    │              │
                              └──────────┘                    └──────────────┘
```

1. **Create Purchase Request** — An internal user raises a request for products/services.
2. **Approve Request** — A manager reviews and approves the request.
3. **Generate RFQ** — An RFQ is created and sent to multiple vendors.
4. **Collect Bids** — Vendors submit their bids with pricing.
5. **Select Winner** — The procurement team compares bids and selects a winner.
6. **Confirm Purchase Order** — The winning bid is converted into a confirmed PO.

---

## Prerequisites

Before installing this module, ensure you have:

- **Odoo 19** (Community or Enterprise) installed and running
- **Python 3.10+**
- **PostgreSQL 14+** configured as the Odoo database backend
- The **Purchase** (`purchase`) module installed and enabled in your Odoo instance
- Your Odoo instance configured to load addons from the directory containing this module

---

## Installation & Setup

### 1. Clone the Repository

```bash
cd /opt/odoo19/custom-addons
git clone https://github.com/Barasa-Paul-Joseph21/custom-add-ons-odoo19.git .
```

> If you already have the repository cloned, pull the latest changes:
> ```bash
> git pull origin main
> ```

### 2. Add the Custom Addons Path

Ensure your Odoo configuration file (`odoo.conf`) includes the custom addons directory:

```ini
[options]
addons_path = /opt/odoo19/odoo/addons,/opt/odoo19/custom-addons
```

### 3. Restart the Odoo Service

```bash
sudo systemctl restart odoo
```

Or, if running Odoo manually:

```bash
python3 odoo-bin -c /etc/odoo/odoo.conf -u rfq_multi_vendor
```

### 4. Update the Apps List

1. Log in to your Odoo instance as an administrator.
2. Enable **Developer Mode**: *Settings → General Settings → Developer Tools → Activate Developer Mode*.
3. Navigate to **Apps → Update Apps List** and click **Update**.

### 5. Install the Module

1. Go to **Apps**.
2. Remove the *"Apps"* filter from the search bar.
3. Search for **"RFQ Multi-Vendor"**.
4. Click **Install**.

---

## Configuration

After installation:

1. Navigate to **Purchase → Requests for Quotation**.
2. Open any existing RFQ or create a new one.
3. Check the **"Multi-Vendor RFQ"** checkbox to enable the multi-vendor bidding tab.
4. The **"Multi-Vendor Bids"** tab will appear in the form, providing access to bid management features.

No additional system configuration is required — the module integrates directly with Odoo's existing purchase workflow.

---

## Usage

### Creating a Multi-Vendor RFQ

1. Go to **Purchase → Requests for Quotation → New**.
2. Check **"Multi-Vendor RFQ"**.
3. Add vendors and products as usual.
4. Use the **Multi-Vendor Bids** tab to manage incoming bids.

### Managing Bids *(Phase 2)*

- Add bids from each vendor with their quoted amounts.
- Compare bids within the RFQ form.
- Mark a bid as **Accepted** to set it as the winner.

### Purchase Request *(Phase 2)*

- Navigate to **Purchase → Purchase Requests**.
- Create a request, add products, and submit for approval.
- Once approved, generate RFQs directly from the request.

---

## Folder Structure

```
rfq_multi_vendor/
├── __init__.py                  # Root package init
├── __manifest__.py              # Module manifest (metadata, dependencies, data files)
├── README.md                    # This file
├── data/                        # Seed data and sequences (Phase 2)
├── models/
│   ├── __init__.py              # Models package init
│   └── purchase_order.py        # Inherited purchase.order model
├── security/
│   └── ir.model.access.csv      # Access control rules
└── views/
    └── purchase_order_views.xml  # XML view extensions for the RFQ form
```

---

## Development Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| **1.5** | Module scaffold, manifest, inherited model, placeholder UI | ✅ Complete |
| **2a** | Full data models (`vendor.bid`, `purchase.request`) | 🔲 Pending |
| **2b** | Bidding workflow, winner selection logic | 🔲 Pending |
| **2c** | Form/tree views for bids and purchase requests | 🔲 Pending |
| **2d** | Validation, status bars, reports, automated tests | 🔲 Pending |

---

## Contributing

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request.

Please follow Odoo's [coding guidelines](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html) and ensure your code is clean and well-documented.

---

## License

This project is licensed under the **LGPL-3** license. See the [LICENSE](https://www.gnu.org/licenses/lgpl-3.0.en.html) file for details.

---

## Author

**Joseph Barasa**

Built as part of an Odoo 19 Purchases module extension assignment.
