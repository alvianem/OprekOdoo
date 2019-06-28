from odoo import fields, models, api

class ProjectProject(models.Model):
    _inherit = "project.project"

    p_start_date = fields.Date(string="Start Date")
    revise_start_date = fields.Date(string='Revise Start Date')
    p_end_date = fields.Date(string='End Date')
    revise_end_date = fields.Date(string='Revise End Date')
    actual_end_date = fields.Date(string='Actual End Date')
    
    #customer partner_id project di xml nya aja
    customer_project = fields.Many2one('res.partner', string="Customer", related='analytic_account_id.partner_id')
    customer_group = fields.Selection([('asyst', 'ASYST'),('ga_group', 'GA Group'),('non_ga_group', 'NON GA Group')], string="Customer Group")
    
    type_project = fields.Selection([('internal','Internal'),('external','External')], string='Type Project')
    p_status = fields.Selection([('1iwo','Request For IWO'),('2created','Created'),('3progress','On Progress'),('4delivered','Delivered'),('5closed','Closed'),('6onhold','On Hold'),('7cancelled','Cancelled')], string='Project Status')
    
    #p_status = fields.Text(string='Project Status', compute='_get_project_status', readonly=True)

    project_no = fields.Integer(string='Project No', related='id')
    project_code = fields.Text(string='Project Code', compute='_project_code_concat')
    #project_id = fields.Text(string='Project Status', readonly=True, compute='kasi kode') compute kasi code
    #salesid = fields.Integer(string='Sales Id' readonly=True, related=salesorderid) compute kasi kode
    
    salesorder = fields.One2many('sale.order', 'project_project_id', string='Sales order')
    salesid = fields.Integer(string='Sales Id', readonly=True, related='salesorder.id')
    sales_code = fields.Text(string='Project Code', compute='_sales_code_concat')
    salesperson = fields.Many2one('res.users', string='Account Manager', readonly=True, related='salesorder.user_id', domain=[('project_project_id','=', 'id')]) 
    pmo_in_charge = fields.Many2one('res.users', string='PMO in Charge')

    
    project_check = fields.One2many('project.checklist', 'projectcheck_id', string='Project checklist')

    description = fields.Html()

    @api.depends('active')
    def _get_project_status(self):
        for rec in self:
            if rec.active == True:
                rec.p_status = 'Open'
            else:
                rec.p_status = 'Closed'
                
    @api.depends('project_no')
    def _project_code_concat(self):
        for rec in self:
            code="PR"
            rec.project_code = code + str(rec.project_no)

    @api.depends('salesid')
    def _sales_code_concat(self):
        for rec in self:
            code="SO"
            rec.sales_code = code + str(rec.salesid)

