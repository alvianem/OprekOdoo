from datetime import date, datetime
from odoo import fields, models, api, _

class ProjectProject(models.Model):
    _inherit = "project.project"

    p_start_date = fields.Date(string="Start Date", track_visibility='onchange')
    revise_start_date = fields.Date(string='Revise Start Date', track_visibility='onchange')
    p_end_date = fields.Date(string='End Date', track_visibility='onchange')
    revise_end_date = fields.Date(string='Revise End Date', track_visibility='onchange')
    datenow = fields.Date(string='Date Now', compute='_datenow')
    deltadate = fields.Integer(string="Selisih Deadline", compute='_itung_deadline')
    #patokan = fields.Integer(string="Patokan", compute='_itung_patokan')
    #customer partner_id project di xml nya aja
    customer_project = fields.Many2one('res.partner', string="Customer", related='analytic_account_id.partner_id', track_visibility='onchange')
    customer_group = fields.Selection([('asyst', 'ASYST'),('ga_group', 'GA Group'),('non_ga_group', 'NON GA Group')], string="Customer Group", track_visibility='onchange')
    
    type_project = fields.Selection([('internal','Internal'),('external','External')], string='Type Project', track_visibility='onchange')
    p_status = fields.Selection([
        ('2iwo','Request For IWO'),
        ('1created','Created'),
        ('proposeteam','Propose Team'),
        ('3progress','In Progress'),
        ('4delivered','Delivered'),
        ('5closed','Closed'),
        ('6onhold','On Hold'),
        ('7cancelled','Cancelled')],
        compute='_statuschange', 
        string='Project Status', 
        default = '1created')
    #p_statusnow = fields.Selection(string='Status', related='p_status', readonly=True)
    
    project_no = fields.Integer(string='Project No', related='id')
    project_code = fields.Text(string='Project Code', compute='_project_code_concat')
    salesid = fields.Integer(string='Sales Id', readonly=True, related='salesorder.id')
    # sales_code = fields.Text(string='Project Code', compute='_sales_code_concat')
    
    salesorder = fields.One2many('sale.order', 'project_project_id', string='Sales order') #nampilin saleorder bersangkutan, dan bisa create disini
    salesno = fields.Many2one('sale.order', string='Sales No') #ngerefer ngambil id nya sale order yang mana
    salesnorelated = fields.Char(string='Sales No', related='salesorder.name')
    # salesperson = fields.Many2one('res.users', string='Account Manager', readonly=False, related='salesorder.user_id', domain=[('project_project_id','=', 'id')]) 
    pmo_in_charge = fields.Many2one('res.users', string='PMO in Charge')

    
    
    description = fields.Html()

    teamdone = fields.Boolean(string = 'Team Done', default = False)

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
    
    members = fields.Many2many('hr.employee', 'project_user_rel', 'project_id',
                               'uid', 'Project Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project."""
                               )

    # refers_to = fields.Reference(
    # [('res.user', 'User'), ('res.partner', 'Partner')],
    # 'Refers to')

    @api.multi
    def _datenow(self):
        for each in self:
            each.datenow = date.today()

    # @api.multi
    # def _itung_patokan(self):
    #     for each in self:
    #         each.patokan = 6

    @api.multi
    @api.depends('datenow', 'revise_end_date', 'deltadate')
    def _itung_deadline(self):
        # result = {}
        # if deltadate:
        #     selisih = self.env['project.project'].search([('id', '=', deltadate)])
        # if selisih:
        #     result['deltatanggal'] = selisih.deltatanggal
        # return {'value': result}
        for each in self:
            if each.datenow and each.revise_end_date:
                d1=datetime.strptime(str(each.revise_end_date),'%Y-%m-%d') 
                d2=datetime.strptime(str(each.datenow),'%Y-%m-%d')
                d3=d1-d2
                each.deltadate=str(d3.days)
        


    
                
    @api.depends('project_no')
    def _project_code_concat(self):
        for rec in self:
            code="PMO"
            rec.project_code = code + str(rec.project_no)

    # @api.depends('salesid')
    # def _sales_code_concat(self):
    #     for rec in self:
    #         code="IWO"
    #         rec.sales_code = code + str(rec.salesid)

    #@api.multi
    #def iwo_progressbar(self):
    #    self.write({'p_status': '1iwo'})

    #@api.multi
    #def created_progressbar(self):
    #    self.write({'p_status': '2created'})    
    
    #@api.multi
    #@api.depends('iwodone')
    #def progress_progressbar(self):
    #    for rec in self:
    #        if rec.iwodone == True:
    #            self.write({'p_status': '3progress'})
    
    #@api.multi
    #@api.depends('charter','uat','kickoff')
    #def delivered_progressbar(self):
    #    for rec in self:
    #        if rec.uat == True:
    #            self.write({'p_status': '4delivered'})
    
    #@api.multi
    #@api.depends('closed','bast','handover')
    #def closed_progressbar(self):
    #    for rec in self:
    #        if rec.closed == True and rec.bast == True and rec.handover == True:
    #            self.write({'p_status': '5closed'})
    
    #@api.multi
    #@api.depends('suratonhold')
    #def onhold_progressbar(self):
    #    for rec in self:
    #        if rec.suratonhold == True:
    #            self.write({'p_status': '6onhold'})
    
    #@api.multi
    #@api.depends('suratcancel')
    #def cancelled_progressbar(self):
    #    for rec in self:
    #        if rec.suratcancel == True:
    #            self.write({'p_status': '7cancelled'})
    
    @api.depends('salesno', 'teamdone', 'iwodone', 'uat', 'closed', 'bast', 'handover', 'suratcancel', 'suratonhold')
    def _statuschange(self):
        for rec in self:
            if rec.salesno:
                rec.p_status='2iwo'
                if rec.iwodone == True:
                    rec.p_status='proposeteam'
                    if rec.teamdone == True:
                        rec.p_status='3progress'
                        if rec.uat == True:
                            rec.p_status='4delivered'
                            if rec.closed == True and rec.bast == True and rec.handover == True:
                                rec.p_status='5closed'
                        if rec.suratonhold == True:
                            rec.p_status='6onhold'
                        if rec.suratcancel == True:
                            rec.p_status='7cancelled'
                    if rec.suratonhold == True:
                        rec.p_status='6onhold'
                    if rec.suratcancel == True:
                        rec.p_status='7cancelled'
                elif rec.suratonhold == True:
                    rec.p_status='6onhold'
                elif rec.suratcancel == True:
                    rec.p_status='7cancelled'
            elif not rec.salesno:
                rec.p_status='1created'
                if rec.salesno:
                    rec.p_status='2iwo'
                    if rec.iwodone == True:
                        rec.p_status='proposeteam'
                        if rec.teamdone == True:
                            rec.p_status='3progress'
                            if rec.uat == True:
                                rec.p_status='4delivered'
                                if rec.closed == True and rec.bast == True and rec.handover == True:
                                    rec.p_status='5closed'
                            if rec.suratonhold == True:
                                rec.p_status='6onhold'
                            if rec.suratcancel == True:
                                rec.p_status='7cancelled'
                        if rec.suratonhold == True:
                            rec.p_status='6onhold'
                        if rec.suratcancel == True:
                            rec.p_status='7cancelled'
                    if rec.suratonhold == True:
                        rec.p_status='6onhold'
                    if rec.suratcancel == True:
                        rec.p_status='7cancelled'
                elif rec.suratonhold == True:
                    rec.p_status='6onhold'
                elif rec.suratcancel == True:
                    rec.p_status='7cancelled'
    #@api.multi
    #@api.depends('iwodone', 'charter','uat','kickoff', 'closed','bast','handover', 'suratonhold', 'suratcancel', 'p_status')
    #def statusbar_onchange(self):
    #    for rec in self:
    #        if rec.iwodone == True:
    #            self.write({'p_status': '3progress'})
    #        elif rec.charter == True and rec.uat == True and rec.kickoff == True:
    #            self.write({'p_status': '4delivered'})
    #        elif rec.closed == True and rec.bast == True and rec.handover == True:
    #            self.write({'p_status': '5closed'})
    #        elif rec.suratonhold == True:
    #            self.write({'p_status': '6onhold'})        
    #        elif rec.suratcancel == True:
    #            self.write({'p_status': '7cancelled'})



class ResUsersInherit(models.Model):
    _inherit = 'hr.employee'

    projectmembers = fields.Many2many('project.project', 'project_user_rel',
                                    'uid', 'project_id', 'Project History',
                                    help="""Project's members are users who
                                     can have an access to the tasks related
                                     to this project.""")
            
