from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, default=lambda self: self.env.user.employee_id)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id')
    date_request = fields.Date(string='Request Date', required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('rfq_created', 'RFQ Created'),
        ('rejected', 'Rejected')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    line_ids = fields.One2many('purchase.request.line', 'request_id', string='Products to Purchase')
    rfq_count = fields.Integer(compute='_compute_rfq_count', string='RFQ Count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'
        return super(PurchaseRequest, self).create(vals_list)

    def _compute_rfq_count(self):
        for request in self:
            request.rfq_count = self.env['purchase.order'].search_count([('purchase_request_id', '=', request.id)])

    def action_submit(self):
        self.write({'state': 'to_approve'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_create_rfq(self):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
        action['context'] = {
            'default_purchase_request_id': self.id,
            'default_is_multi_vendor': True,
            'default_order_line': [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'product_uom_id': line.product_uom_id.id,
                    'name': line.product_id.name,
                }) for line in self.line_ids
            ]
        }
        return action

    def action_view_rfqs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFQs',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('purchase_request_id', '=', self.id)],
            'context': "{'create': False}"
        }


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_qty = fields.Float(string='Quantity', required=True, default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
