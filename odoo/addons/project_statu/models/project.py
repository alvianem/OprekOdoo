from odoo import fields, models, api

class ProjectProject(models.Model):
    _inherit = "project.project"

    p_start_date = fields.Date(string="Start Date")
    revise_start_date = fields.Date(string='Revise Start Date')
    p_end_date = fields.Date(string='End Date')
    revise_end_date = fields.Date(string='Revise End Date')
    actual_end_date = fields.Date(string='Actual End Date')
    type_project = fields.Selection([('internal','Internal'),('external','External')], string='Type Project')
    p_status = fields.Text(string='Project Status', compute='_get_project_status', readonly=True)
    customer_group = fields.Selection([('asyst', 'ASYST'),('ga_group', 'GA Group'),('non_ga_group', 'NON GA Group')], string="Customer Group")
    project_no = fields.Integer(string='Project No', related='id')
    #iwo_no = fields.Char(string='IWO No', related=)
    #invoice_no

    #account manager
    #pmo pic

    #tim

    description = fields.Html()

    @api.depends('active')
    def _get_project_status(self):
        for rec in self:
            if rec.active == True:
                rec.p_status = 'Open'
            else:
                rec.p_status = 'Closed'
   