from odoo import fields, models, api, _

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
    p_status = fields.Selection([('1iwo','Request For IWO'),('3progress','On Progress'),('4delivered','Delivered'),('5closed','Closed'),('6onhold','On Hold'),('7cancelled','Cancelled')], string='Project Status', readonly=True, default = '1iwo')
    
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

    
    
    description = fields.Html()

    iwodone = fields.Boolean(string = 'IWO', default = False)
    
    charter = fields.Boolean(string = 'Project Charter', default = False)
    uat = fields.Boolean(string = 'UAT', default = False)
    kickoff = fields.Boolean(string = 'Kickoff', default = False)
    
    bast = fields.Boolean(string = 'BAST', default = False)
    handover = fields.Boolean(string = 'Hand Over', default = False)
    
    suratonhold = fields.Boolean(string = 'On Hold Notice', default = False)
    
    suratcancel = fields.Boolean(string = 'Cancel Notice', default = False)
    
    closed = fields.Boolean(string = 'Closed', default = False)

    iwoattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_iwo_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document IWO")

    charterattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_charter_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document Project Charter")

    uatattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_uat_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document UAT")

    kickoffattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_kickoff_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document Kickoff")

    bastattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_bast_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document BAST")

    handoverattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_handover_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document Hand Over")

    suratonholdattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_onhold_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document On Hold Notice")

    suratcancelattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_cancel_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document Cancel Notice")

    closedattach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_closed_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Document Closed")
    

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

    @api.multi
    def iwo_progressbar(self):
        self.write({'p_status': '1iwo'})
    
    @api.multi
    @api.depends('iwodone')
    def progress_progressbar(self):
        for rec in self:
            if rec.iwodone == True:
                self.write({'p_status': '3progress'})
    
    @api.multi
    @api.depends('charter','uat','kickoff')
    def delivered_progressbar(self):
        for rec in self:
            if rec.charter == True and rec.uat == True and rec.kickoff == True:
                self.write({'p_status': '4delivered'})
    
    @api.multi
    @api.depends('closed','bast','handover')
    def closed_progressbar(self):
        for rec in self:
            if rec.closed == True and rec.bast == True and rec.handover == True:
                self.write({'p_status': '5closed'})
    
    @api.multi
    @api.depends('suratonhold')
    def onhold_progressbar(self):
        for rec in self:
            if rec.suratonhold == True:
                self.write({'p_status': '6onhold'})
    
    @api.multi
    @api.depends('suratcancel')
    def cancelled_progressbar(self):
        for rec in self:
            if rec.suratcancel == True:
                self.write({'p_status': '7cancelled'})
    
    