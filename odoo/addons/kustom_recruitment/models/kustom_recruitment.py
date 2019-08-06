from datetime import datetime, date
from odoo import models, fields, api, _

class create_rfr(models.Model):

    _inherit = 'hr.employee'
    
    sambungan = fields.One2many('rfr','sambungan2')
    
class rfr(models.Model):

    _name = 'rfr'
    # _inherit = 'hr.applicant'
    _rec_name = 'name'
    
    employee_id = fields.Many2one('hr.employee', string='Employee')
    sambungan2 = fields.Many2one('hr.applicant', 'Request For Recruitment')
    
    name = fields.Char(string='RFR Code', readonly=True, copy=False, index=True, default=lambda self: _('FHR/RFR/EMP-'))
    recruitment_types = fields.Selection([('internal','Internal'),('external','External')], string='Recruitment Types', required=True)
    employee_classification = fields.Selection([('permanent','Permanent'),('contract','Contract')], string='Employee Clasification', required=True)
    date = fields.Date(compute='_statuschange')
    unit = fields.Many2one('hr.department', related='employee_id.department_id', string='Unit / Departement', store=True , required=True)
    # cost_center = fields.Integer()
    position = fields.Many2one('hr.job', related='employee_id.job_id', string='Position', store=True , required=True)
    grade = fields.Selection([('jr','Junior'),('mid','Middle'),('sr','Senior'),('mn','Manager')], string='Grade' , required=True)
    
    expect_joindate = fields.Date(required=True)
    number_of_employee = fields.Integer(required=True)
    # number_of_manpower = fields.Integer()
    job_description = fields.Char(required=True)
    job_attach= fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_job_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Description")
    # description_job = fields.Text()
    reason_request = fields.Text(required=True)
    
    user_prepared = fields.Many2one('res.users', readonly='True', default=lambda self: self.env.uid)
    
    head_prepared0 = fields.Many2one('res.users', readonly='True', default=lambda self: self.env.uid)
    director_prepared0 = fields.Many2one('res.users', readonly='True', default=lambda self: self.env.uid)
    hr_checked0 = fields.Many2one('res.users', readonly='True', default=lambda self: self.env.uid)
    bod2_approved0 = fields.Many2one('res.users', readonly='True', default=lambda self: self.env.uid)
    
    head_prepared1 = fields.Char(default='General Manager')
    approver1 = fields.Char()
    director_prepared1 = fields.Char(default='CEO / (BOD1)')
    
    comfirmer = fields.Char()
    
    head_prepared2 = fields.Many2one('res.users')
    head_prepared2_note = fields.Text()
    
    director_prepared2 = fields.Many2one('res.users')
    director_prepared2_note = fields.Text()
    
    hr_checked = fields.Many2one('res.users')
    hr_checked_note = fields.Text()
    
    bod2_approved = fields.Many2one('res.users')
    bod2_approved_note = fields.Text()
    
    date_confirm = fields.Date(string="Confirm Date")
    date_refuse1 = fields.Date(string="Refuse Date")
    date_approved1 = fields.Date(string="Approved Date")
    date_refuse2 = fields.Date(string="Refuse Date")
    date_checked = fields.Date(string="Checked Date")
    date_refuse3 = fields.Date(string="Refuse Date")
    date_approved2 = fields.Date(string="Approved Date")
    date_refuse4 = fields.Date(string="Refuse Date")
    
    hr_comments = fields.Text()
    manpower_plan = fields.Text()
    budget_control = fields.Text()
    
    confirm = fields.Boolean(string = 'Confirm Done', default = False)
    approve1 = fields.Boolean(string = 'Approve 1 Done', default = False)
    check = fields.Boolean(string = 'Check Done', default = False)
    approve2 = fields.Boolean(string = 'Approve 2 Done', default = False)
    refuse1 = fields.Boolean(string = 'Refuse GM', default = False)
    refuse2 = fields.Boolean(string = 'Refuse BOD 1', default = False)
    refuse3 = fields.Boolean(string = 'Refuse HC', default = False)
    refuse4 = fields.Boolean(string = 'Refuse BOD 2', default = False)
    
    note1 = fields.Text(compute='_note1')
    note2 = fields.Text(compute='_note2')
    note3 = fields.Text(compute='_note3')
    note4 = fields.Text(compute='_note4')
    
    state = fields.Selection([
        ('draft', 'To Submit'),('confirm', 'Confirm'),('tocheck', 'To Check'),('check', 'Check'),('approved', 'Approved'),
        ('refusegm', 'General Manager Refused'),('refusebod1', 'BOD 1 Refused'),('refusehc', 'Human Capital Refused'),('refusebod2', 'BOD 2 Refused')
        ], string='Status', compute='_statuschange', store=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('seq_rfr') or _('New')
            # vals['name'] = self.env['ir.sequence'] 
        res = super(rfr, self).create(vals)
        return res
    
    @api.multi
    @api.depends('date','confirm','approve1','check','approve2')
    def _statuschange(self):
        for each in self:
            each.date = date.today()
        for rec in self:
            if rec.recruitment_types:
                rec.state='draft'
                # if rec.refuse1 == True:
                    # rec.state='refusegm'
                # if rec.confirm == True:
                    # rec.state='confirm'
                    # if rec.refuse2 == True:
                        # rec.state='refusebod1'
                    # if rec.approve1 == True:
                        # rec.state='tocheck'
                        # if rec.refuse3 == True:
                            # rec.state='refusehc'
                        # if rec.check == True:
                            # rec.state='check'
                            # if rec.approve2 == True:
                                # rec.state='approved'
                            # if rec.refuse4 == True:
                                # rec.state='refusebod2'

    @api.multi
    @api.depends('user_prepared')
    def action_confirm(self):
        for rec in self:
            if rec.recruitment_types:
                self.write({'confirm': True})
                self.write({'state': 'confirm'})
                for rec in self:
                    rec.head_prepared2 = rec.head_prepared0
                for each in self:
                    each.date_confirm = date.today()
    
    @api.multi
    def action_refusegm(self):
        for rec in self:
            if rec.recruitment_types:
                self.write({'refuse1': True})
                self.write({'state': 'refusegm'})
                for rec in self:
                    rec.head_prepared2 = rec.head_prepared0
                for each in self:
                    each.date_refuse1 = date.today()                
    
    @api.multi
    def action_cancelgm(self):
        for rec in self:
            if rec.confirm == True:
                self.write({'confirm': False})
                self.write({'state': 'draft'})
                self.write({'date_confirm': ''})
                self.write({'head_prepared2': ''})
            if rec.refuse1 == True:
                self.write({'refuse1': False})
                self.write({'state': 'draft'})
                self.write({'date_refuse1': ''})
                self.write({'head_prepared2': ''})
    
    @api.multi
    def action_approve1(self):
        for rec in self:
            if rec.confirm == True:
                self.write({'approve1': True})
                self.write({'state': 'tocheck'})
                for rec in self:
                    rec.director_prepared2 = rec.director_prepared0
                for each in self:
                    each.date_approved1 = date.today()
    
    @api.multi
    def action_refusebod1(self):
        for rec in self:
            if rec.confirm == True:
                self.write({'refuse2': True})
                self.write({'state': 'refusebod1'})
                for rec in self:
                    rec.director_prepared2 = rec.director_prepared0
                for each in self:
                    each.date_refuse2 = date.today() 

    @api.multi
    def action_cancelbod1(self):
        for rec in self:
            if rec.approve1 == True:
                self.write({'approve1': False})
                self.write({'state': 'confirm'})
                self.write({'date_approved1': ''})
                self.write({'director_prepared2': ''})
            if rec.refuse2 == True:
                self.write({'refuse2': False})
                self.write({'state': 'confirm'})
                self.write({'date_refuse2': ''})
                self.write({'director_prepared2': ''})
               
    @api.multi
    def action_check(self):
        for rec in self:
            if rec.approve1 == True:
                self.write({'check': True})
                self.write({'state': 'check'})
                for rec in self:
                    rec.hr_checked = rec.hr_checked0
                for each in self:
                    each.date_checked = date.today()
                    
    @api.multi
    def action_refusehc(self):
        for rec in self:
            if rec.approve1 == True:
                self.write({'refuse3': True})
                self.write({'state': 'refusehc'})
                for rec in self:
                    rec.hr_checked = rec.hr_checked0
                for each in self:
                    each.date_refuse3 = date.today()  
    
    @api.multi
    def action_cancelhc(self):
        for rec in self:
            if rec.check == True:
                self.write({'check': False})
                self.write({'state': 'tocheck'})
                self.write({'date_checked': ''})
                self.write({'hr_checked': ''})
            if rec.refuse3 == True:
                self.write({'refuse3': False})
                self.write({'state': 'tocheck'})
                self.write({'date_refuse3': ''})
                self.write({'hr_checked': ''})
    
    @api.multi
    def action_approve2_admin(self):
        for rec in self:
            if rec.check == True:
                self.write({'approve2': True})
                self.write({'state': 'approved'}) 
                for rec in self:
                    rec.bod2_approved = rec.bod2_approved0
                for each in self:
                    each.date_approved2 = date.today()
    
    @api.multi
    def action_refusebod2(self):
        for rec in self:
            if rec.check == True:
                self.write({'refuse4': True})
                self.write({'state': 'refusebod2'})
                for rec in self:
                    rec.bod2_approved = rec.bod2_approved0
                for each in self:
                    each.date_refuse4 = date.today()  
    
    @api.multi
    def action_cancelbod2(self):
        for rec in self:
            if rec.approve2 == True:
                self.write({'approve2': False})
                self.write({'state': 'check'})
                self.write({'date_approved2': ''})
                self.write({'bod2_approved': ''})
            if rec.refuse4 == True:
                self.write({'refuse4': False})
                self.write({'state': 'check'})
                self.write({'date_refuse4': ''})
                self.write({'bod2_approved': ''})
    
    @api.multi
    @api.depends('head_prepared2_note')
    def _note1(self):
        for rec in self:
            rec.note1 = rec.head_prepared2_note
            
    @api.multi
    @api.depends('director_prepared2_note')
    def _note2(self):
        for rec in self:
            rec.note2 = rec.director_prepared2_note

    @api.multi
    @api.depends('hr_checked_note')
    def _note3(self):
        for rec in self:
            rec.note3 = rec.hr_checked_note

    @api.multi
    @api.depends('bod2_approved_note')
    def _note4(self):
        for rec in self:
            rec.note4 = rec.bod2_approved_note
        