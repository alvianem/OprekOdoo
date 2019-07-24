from datetime import date, datetime
from odoo import fields, models, api, _

class ProjectProject(models.Model):
    _inherit = "project.project"

    p_start_date = fields.Date(string="Project Start Date", track_visibility='onchange', store=True)
    revise_start_date = fields.Date(string='Revise Start Date', track_visibility='onchange', store=True)
    p_end_date = fields.Date(string='Project End Date', track_visibility='onchange', store=True)
    revise_end_date = fields.Date(string='Revise End Date', track_visibility='onchange', store=True)
    deltadate = fields.Integer(string="Selisih Deadline", compute='_itung_deadline', store=True)
    customer_project = fields.Many2one(readonly=False, related='saleproject_o2m.customersale', track_visibility='onchange', store=True)
    customer_group = fields.Selection([('asyst', 'ASYST'),('garuda', 'GA'),('ga_group', 'GA Group'),('non_ga_group', 'NON GA Group')], string="Customer Group", track_visibility='onchange', store=True)
    type_project = fields.Selection([('internal','Internal'),('external','External')], string='Type Project', track_visibility='onchange', store=True)
    p_status = fields.Selection([
        ('1created','Created'),
        ('2iwo','Request For IWO'),
        ('proposeteam','Propose Team'),
        ('3progress','In Progress'),
        ('4delivered','Delivered'),
        ('5closed','Closed'),
        ('6onhold','On Hold'),
        ('7cancelled','Cancelled')],
        compute='_statuschange', 
        string='Project Status', 
        default = '1created',store=True)
    project_no = fields.Integer(string='Project No', related='id', store=False)
    project_code = fields.Text(string='Project Code', compute='_project_code_concat', store=True)
    pmo_in_charge = fields.Many2one('res.users', string='PMO in Charge', default=lambda self: self.env.uid, store=True)
    description = fields.Html()

    partner_idi = fields.Many2one('res.partner', 'partnerr')
    # user_idi = fields.Many2one('res.users', 'userr', related='teamo2mp.userem2o')
# related='teamo2mp.userem2o'
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

    onholdvisible = fields.Boolean(string = 'On Hold Visibility', default = False)
    cancelvisible = fields.Boolean(string = 'Cancel Visibility', default = False)

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
    
    #members = fields.Many2many('hr.employee', 'project_user_rel', 'project_id',
                               # 'uid', 'Project Members', help="""Project's
                               # members are users who can have an access to
                               # the tasks related to this project."""
                               # )

    teamo2mp = fields.One2many('project.team', 'projectm2o', string="Team Projects")
    saleproject_o2m = fields.One2many('project.sale', 'projectm2os', string="Sale Projects")
    salesidnya = fields.Many2one(string='Sales No', readonly=True, related='saleproject_o2m.salem2os',store=True)

    # user_id = fields.Many2one('res.users',
    #     string='Assigned to',
    #     default=lambda self: self.env.uid,
    #     index=True, track_visibility='always')

    # @api.multi
    # def _datenow(self):
    #     for each in self:
    #         each.datenow = date.today()

    @api.multi
    @api.depends('revise_end_date', 'deltadate')
    def _itung_deadline(self):
        datenow = date.today()
        for each in self:
            if each.revise_end_date:
                d1=datetime.strptime(str(each.revise_end_date),'%Y-%m-%d') 
                d2=datetime.strptime(str(datenow),'%Y-%m-%d')
                d3=d1-d2
                if int(d3.days) < 0:
                    each.deltadate= int(0)
                else:
                    each.deltadate=int(d3.days)
                
    @api.depends('project_no')
    def _project_code_concat(self):
        for rec in self:
            code="PMO"
            rec.project_code = code + str(rec.project_no)
    
    @api.depends('salesidnya', 'teamdone', 'iwodone', 'uat', 'closed', 'bast', 'handover', 'suratcancel', 'suratonhold')
    def _statuschange(self):
        for rec in self:
            if rec.salesidnya:
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
            if not rec.salesidnya:
                rec.p_status='1created'
                if rec.salesidnya:
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

    @api.multi
    def action_follow(self):
        # fetch the partner's id and subscribe the partner to the sale order
        for rec in self:
            if rec.partner_idi not in rec.message_partner_ids:
                rec.message_subscribe([rec.partner_idi.id])
        return True

    # @api.multi
    # def iwo_progressbar(self):
    #     self.write({'p_status': '1iwo'})
    
    @api.multi
    def iwo_progressbar(self):
        self.write({'p_status': '2iwo'})

    @api.multi
    def propose_progressbar(self):
        if self.iwoattach:
            self.write({'iwodone': 'True'})

    @api.multi
    def progress_progressbar(self):
        self.write({'teamdone': 'True'})
    
    @api.multi
    def delivered_progressbar(self):
        if self.uatattach:
            self.write({'uat': 'True'})
    
    @api.multi
    def closed_progressbar(self):
        if self.closedattach and self.bastattach and self.handoverattach:
            self.write({'closed': 'True'})
            self.write({'bast': 'True'})
            self.write({'handover': 'True'})

    
    @api.multi
    def onhold_progressbar(self):
        if self.suratonholdattach and self.onholdvisible == True:
            self.write({'suratonhold': 'True'})
    
    @api.multi
    def cancelled_progressbar(self):
        if self.suratcancelattach and self.cancelvisible == True:
            self.write({'suratcancel': 'True'})
    
    @api.multi
    def onholdvisible_progressbar(self):
        self.onholdvisible = True

    @api.multi
    def cancelvisible_progressbar(self):
        self.cancelvisible = True

    @api.multi
    def continue_progressbar(self):
        self.suratonhold = False

    @api.multi
    def uncancel_progressbar(self):
        self.suratcancel = False


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    #projectmembers = fields.Many2many('project.project', 'project_user_rel',
    #                                 'uid', 'project_id', 'Project History',
    #                                 help="""Project's members are users who
    #                                  can have an access to the tasks related
    #                                  to this project.""")
    
    # teamm2o = fields.Many2one('project.team', string="Project Team m2o")
    teamo2me = fields.One2many(related="user_id.teamo2mu", string="Project Team")
    countproject = fields.Integer(string="Jumlah All Project", compute="_compute_project")
    currentproject = fields.Integer(string="Current Project", compute="_compute_current_project")
    
    def _compute_project(self):
        for employee in self:
            user = employee.user_id
            if user:
                current = self.env['project.team'].sudo().search([('userem2o','=',user.id)])
                employee.countproject = str(len(current))

    def _compute_current_project(self):
        for employee in self:
            user = employee.user_id
            if user:
                current = self.env['project.team'].sudo().search(['&',('userem2o','=',user.id),('status_assign','=','assigned')])
                employee.currentproject = str(len(current))

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    teamo2mu = fields.One2many('project.team', 'userem2o', string="Project Team")

class ProjectTeam(models.Model):
    _name = 'project.team'

    _sql_constraints = [ ('unique_user', 
        'unique(userem2o, projectm2o)', 
        'User has been assigned to this project!\nPlease, select a different user!')]

    # employeeo2m = fields.One2many('hr.employee', 'teamm2o', string="Employee team")
    # user_id = fields.Many2one(related='employeeo2m.user_id')
    partnerm2o = fields.Many2one('res.partner', string="related partner", related='userem2o.partner_id')
    userem2o = fields.Many2one('res.users', string="Users")
    projectm2o = fields.Many2one('project.project', string="Projects")
    # employeem2o = fields.Many2one('hr.employee', string="Employees")
    start_assign = fields.Datetime(string="Start Assigned Date", readonly=True)
    end_assign = fields.Datetime(string="End Assigned Date", readonly=True)
    status_assign = fields.Selection([('assigned','Assigned'),('unassigned','Unassigned')], string="Status", readonly=True)
    message_partner = fields.Many2many(related="projectm2o.message_partner_ids")

    @api.multi
    def assign_person(self):
        # partner = self.partnerm2o
        # message_partner_proj = self.projectm2o.message_partner_ids
        self.start_assign = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status_assign = 'assigned'
            # self.env['project.project'].action_follow()
            # self.write({'projectm2o.partner_idi': self.partnerm2o})
            # for rec in self:
            #     if rec.partnerm2o not in message_partner_proj:
            #         partner.message_subscribe([rec.partnerm2o.id])
            # return True

    @api.multi
    def unassign_person(self):
        self.end_assign = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status_assign = 'unassigned'

    @api.multi
    @api.depends('start_assign')
    def assignbol(self):
        for rec in self:
            if rec.start_assign:
                rec.assignbool = True

    @api.multi
    @api.depends('end_assign')
    def unassignbol(self):
        for rec in self:
            if rec.end_assign:
                rec.unassignbool = True


    # @api.multi
    # def assign_person(self):
    #     if not self.start_assign:
    #         self.start_assign = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         self.status_assign = 'assigned'

    # @api.one
    # def auto_date(self):
    #     if not self.start_assign:
    #         self.start_assign = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    # @api.multi
    # @api.onchange('employeem2o')
    # def auto_status(self):
    #     for rec in self:
    #         if rec.end_assign:
    #             rec.status_assign = 'unassigned'
    #         elif rec.start_assign:
    #             rec.status_assign = 'assigned'

class ProjectSaleInherit(models.Model):
    _inherit = 'sale.order'

    # projectconvert = fields.Boolean(string = "Convert to Project", compute="convert_project")
    state = fields.Selection(selection_add=[
        ('review', 'PMO Review'),
        ('reviewed', 'PMO Reviewed')
        # ('invoice', 'Ready to Invoice')
        ])
    projectsale_o2ms = fields.One2many('project.sale', 'salem2os', string='Project salem2os')
    statusproject = fields.Selection(related='projectsale_o2ms.projectstate')
    
    @api.multi
    def action_review(self):
        return self.write({'state': 'review'})

    @api.multi
    def action_done_review(self):
        return self.write({'state': 'reviewed'})

    # @api.multi
    # def action_ready_invoice(self):
    #     return self.write({'state': 'invoice'})


class ProjectSale(models.Model):
    _name = 'project.sale'

    projectm2os = fields.Many2one('project.project', string="Projects")
    salem2os = fields.Many2one('sale.order', string="Sales")
    customersale = fields.Many2one(related='salem2os.partner_id')
    projectstate = fields.Selection(related='projectm2os.p_status', readonly=True)