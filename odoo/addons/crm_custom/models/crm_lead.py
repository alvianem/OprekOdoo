# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CRMLead(models.Model):

    _inherit = "crm.lead"

    user_id = fields.Many2one('res.users', string='Account Manager', default=lambda self: self.env.uid, store=True)
    tag_ids = fields.Many2many('crm.lead.tag', 'crm_lead_tag_rel', 'lead_id', 'tag_id', string='Opportunity Type', help="Classify and analyze your lead/opportunity categories like: Training, Service")
    priority = fields.Selection(string='Priority', index=True)

