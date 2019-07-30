# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    sale_tag = fields.Many2many('res.partner.category', column1='partner_id',
        column2='category_id', string='Category', default=_default_category)

    user_id = fields.Many2one('res.users', string='Account Manager', default=lambda self: self.env.uid, store=True)
    tag_ids = fields.Many2many('crm.lead.tag', 'sale_order_tag_rel', 'order_id', 'tag_id', string='Sale Order Type')

    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term', required=False, store=True)
    x_payment_term = fields.Selection([('one', 'One Time Charge'),('month', 'Monthly Charge')], string="Payment Terms", track_visibility='onchange', store=True)

    
