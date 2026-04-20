# RFQ Multi-Vendor Bidding

> Odoo 19 module that extends the Purchases (RFQ) module with multi-vendor bidding and purchase request capabilities.

## Objective

Enable organisations to:
- Send a single RFQ to **multiple vendors** simultaneously
- **Collect and compare** vendor bids side-by-side
- **Select a winning bid** and automatically generate a Purchase Order
- Manage the full lifecycle through a **Purchase Request** workflow

## Current Progress

| Milestone | Status |
|-----------|--------|
| Module scaffold & manifest | ✅ Done |
| Model inheritance (`purchase.order`) | ✅ Done |
| Placeholder UI (Multi-Vendor tab in RFQ form) | ✅ Done |
| Access control file | ✅ Done |
| Full data models (Bid, Purchase Request) | 🔲 Pending |
| Bidding workflow & winner selection | 🔲 Pending |
| Purchase Request → RFQ generation | 🔲 Pending |
| Reports & polish | 🔲 Pending |

## Planned Features

1. **Multi-Vendor RFQ** — Attach multiple vendors to a single RFQ and dispatch requests.
2. **Vendor Bid Management** — Vendors submit bids; bids are tracked with status (`draft` / `submitted` / `accepted` / `rejected`).
3. **Winner Selection** — Compare bids and select a winner; the RFQ converts into a confirmed Purchase Order.
4. **Purchase Request Workflow** — Internal users create purchase requests that flow through approval before generating RFQs.

## Installation

1. Place this module in your Odoo `custom-addons` directory.
2. Update the Apps list: **Settings → Apps → Update Apps List**.
3. Search for *"RFQ Multi-Vendor"* and click **Install**.

## Technical Details

- **Odoo version:** 19.0
- **Dependencies:** `purchase`
- **License:** LGPL-3

## Author

Joseph Barasa
