from odoo import fields, models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    """Extend purchase.order to support multi-vendor bidding."""

    _inherit = 'purchase.order'

    # Make partner_id optional for multi-vendor RFQs
    partner_id = fields.Many2one('res.partner', required=False)

    is_multi_vendor = fields.Boolean(
        string='Multi-Vendor RFQ',
        default=False,
        help='Enable this to send the RFQ to multiple vendors and collect bids.',
    )
    
    vendor_ids = fields.Many2many(
        'res.partner', 
        string='Vendors', 
        domain=[('supplier_rank', '>', 0)]
    )
    
    bid_ids = fields.One2many(
        'purchase.bid', 
        'order_id', 
        string='Bids'
    )
    
    purchase_request_id = fields.Many2one(
        'purchase.request', 
        string='Purchase Request',
        readonly=True
    )

    def action_create_bids(self):
        self.ensure_one()
        if not self.is_multi_vendor:
            raise UserError(_('This action is only available for Multi-Vendor RFQs.'))
        if not self.vendor_ids:
            raise UserError(_('Please select at least one vendor.'))
            
        for vendor in self.vendor_ids:
            # Check if bid already exists for this vendor
            existing_bid = self.env['purchase.bid'].search([
                ('order_id', '=', self.id),
                ('partner_id', '=', vendor.id)
            ])
            if not existing_bid:
                bid_vals = {
                    'order_id': self.id,
                    'partner_id': vendor.id,
                    'line_ids': [
                        (0, 0, {
                            'product_id': line.product_id.id,
                            'product_qty': line.product_qty,
                            'price_unit': 0.0,
                        }) for line in self.order_line if line.product_id
                    ]
                }
                self.env['purchase.bid'].create(bid_vals)
        
        # Optionally mark request as RFQ created
        if self.purchase_request_id and self.purchase_request_id.state == 'approved':
            self.purchase_request_id.write({'state': 'rfq_created'})
