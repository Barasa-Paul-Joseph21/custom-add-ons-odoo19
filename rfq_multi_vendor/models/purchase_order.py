from odoo import fields, models


class PurchaseOrder(models.Model):
    """Extend purchase.order to support multi-vendor bidding."""

    _inherit = 'purchase.order'

    is_multi_vendor = fields.Boolean(
        string='Multi-Vendor RFQ',
        default=False,
        help='Enable this to send the RFQ to multiple vendors and collect bids.',
    )
