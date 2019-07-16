from datetime import datetime, date
from odoo import models, fields, api, _

class create_rfr(models.Model):

    _inherit = 'hr.applicant'
    
    sambungan = fields.One2many('rfr','sambungan2')
    
class rfr(models.Model):

    _name = 'rfr'
    # _inherit = 'hr.applicant'
    _rec_name = 'code_rfr'
    
    sambungan2 = fields.Many2one('hr.applicant', 'Request For Recruitment')
    
    code_rfr = fields.Char(string='RFR Code')
    recruitment_types = fields.Selection([('internal','Internal'),('external','External')], string='Recruitment Types')
    employee_classification = fields.Selection([('permanent','Permanent'),('contract','Contract')], string='Employee Clasification')
    date = fields.Date()
    unit = fields.Char()
    # cost_center = fields.Integer()
    position = fields.Char()
    grade = fields.Selection([('jr','Junior'),('mid','Middle'),('sr','Senior'),('mn','Manager')], string='Grade')
    
    expect_joindate = fields.Date()
    number_of_employee = fields.Integer()
    # number_of_manpower = fields.Integer()
    job_description = fields.Char()
    job_attach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_job_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Description")
    # description_job = fields.Text()
    reason_request = fields.Text()
    
    user_prepared = fields.Many2one('hr.employee')
    head_prepared1 = fields.Char(default='General Manager')
    head_prepared2 = fields.Char()
    director_prepared1 = fields.Char(default='CEO / (BOD1)')
    director_prepared2 = fields.Char()
    hr_checked = fields.Char()
    bod2_approved = fields.Char()
    
    comfirmer = fields.Char()
    approver1 = fields.Char()
    date_confirm = fields.Date(string="Confirm Date")
    date_approved1 = fields.Date(string="Approved Date")
    date_checked = fields.Date(string="Checked Date")
    date_approved2 = fields.Date(string="Approved Date")
    
    hr_comments = fields.Text()
    manpower_plan = fields.Text()
    budget_control = fields.Text()
    # approbation1 = fields.One2many('approbations','approbation2')
    
    # draft = = fields.Boolean(string = 'Drat', default = False)
    confirm = fields.Boolean(string = 'Confirm Done', default = False)
    approve1 = fields.Boolean(string = 'Confirm', default = False)
    check = fields.Boolean(string = 'Approve 2 Done', default = False)
    approve2 = fields.Boolean(string = 'Approve Done', default = False)
    # validate = fields.Boolean(string = 'Validate Done', default = False)
    
    state = fields.Selection([
        ('draft', 'To Submit'),('confirm', 'Confirm'),('tocheck', 'To Check'),('check', 'Check'),('approved', 'Approved')
        ], string='Status', compute='_statuschange', store=True)
    
    
    @api.depends('confirm','approve1','check','approve2')
    def _statuschange(self):
        for rec in self:
            if rec.code_rfr:
                rec.state='draft'
                if rec.confirm == True:
                    rec.state='confirm'
                    if rec.approve1 == True:
                        rec.state='tocheck'
                        if rec.check == True:
                            rec.state='check'
                            if rec.approve2 == True:
                                rec.state='approved'


    @api.multi
    def action_confirm(self):
        for rec in self:
            if rec.code_rfr:
                self.write({'confirm': True})
                
        for each in self:
            self.write({'head_prepared2': 'General Manager'})
            each.date_confirm = date.today()
            
    @api.multi
    def action_approve1(self):
        for rec in self:
            if rec.confirm == True:
                self.write({'approve1': True})

            for each in self:
                self.write({'director_prepared2': 'CEO / (BOD1)'})
                each.date_approved1 = date.today()
        # self.write({'approve1': True})
        
    @api.multi
    def action_check(self):
        for rec in self:
            if rec.approve1 == True:
                self.write({'check': True})

            for each in self:
                self.write({'hr_checked': 'Human Capital'})
                each.date_checked = date.today()
        # self.write({'check': True})
        
    @api.multi
    def action_approve2(self):
        for rec in self:
            if rec.check == True:
                self.write({'approve2': True})

            for each in self:
                self.write({'bod2_approved': 'CFO / (BOD2)'})
                each.date_approved2 = date.today()
        # self.write({'approve2': True})

class employee(models.Model):
    _inherit='hr.employee'
    
    