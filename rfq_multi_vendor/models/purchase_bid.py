from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseBid(models.Model):
    _name = 'purchase.bid'
    _description = 'Vendor Bid for RFQ'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Bid Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')
    order_id = fields.Many2one('purchase.order', string='Master RFQ', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True)
    date_bid = fields.Date(string='Bid Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('won', 'Won'),
        ('lost', 'Lost')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    line_ids = fields.One2many('purchase.bid.line', 'bid_id', string='Bid Lines')
    amount_total = fields.Float(compute='_compute_amount_total', string='Total Amount', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.bid') or 'New'
        return super(PurchaseBid, self).create(vals_list)

    @api.depends('line_ids.price_subtotal')
    def _compute_amount_total(self):
        for bid in self:
            bid.amount_total = sum(bid.line_ids.mapped('price_subtotal'))

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_select_winning_bid(self):
        self.ensure_one()
        if self.state != 'submitted':
            raise UserError(_('Only submitted bids can be selected as winning bids.'))

        # Mark other bids as lost
        other_bids = self.search([('order_id', '=', self.order_id.id), ('id', '!=', self.id)])
        other_bids.write({'state': 'lost'})

        # Mark this bid as won
        self.write({'state': 'won'})

        # Update Master RFQ
        order = self.order_id
        order.write({
            'partner_id': self.partner_id.id,
            'state': 'draft', # Ensure it can be confirmed
        })
        
        # Update prices on Master RFQ lines based on winning bid
        for line in order.order_line:
            bid_line = self.line_ids.filtered(lambda l: l.product_id == line.product_id)
            if bid_line:
                line.write({'price_unit': bid_line[0].price_unit})
        
        # Confirm the Master RFQ -> becomes a PO
        order.button_confirm()

class PurchaseBidLine(models.Model):
    _name = 'purchase.bid.line'
    _description = 'Vendor Bid Line'

    bid_id = fields.Many2one('purchase.bid', string='Bid', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_qty = fields.Float(string='Quantity', required=True, default=1.0)
    price_unit = fields.Float(string='Unit Price', required=True, default=0.0)
    price_subtotal = fields.Float(compute='_compute_price_subtotal', string='Subtotal', store=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_qty * line.price_unit
