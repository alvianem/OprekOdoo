# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    techskill_ids = fields.One2many(
        'tech.tech', 'employee_id')
    nontechskill_ids = fields.One2many('nontech.nontech', 'employee_id')
    
    education_ids = fields.One2many(
        'employee.education', 'employee_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'employee_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession', 'employee_id', 'Professional Experience')
     
class HrApplicant(models.Model):
    _name ='nama'
    _inherit = 'hr.applicant'

    tes = fields.One2many('nontech.nontech', 'applicant_id')
    

class TechTech(models.Model):
    _name = 'tech.tech'
    _rec_name = 'competency_tech'
    
    applicant_id = fields.Many2one('hr.applicant', 'Applicant Id')
    employee_id = fields.Many2one('hr.employee', 'Employee Id')
    competency_tech_types = fields.Many2one(related='competency_tech.types', string='Competency Types')
    category_competency_tech = fields.Many2one(related='competency_tech.category', string='Competency Category')
    competency_tech = fields.Many2one('comp.tech', string='Competency Name')
    levels_tech = fields.Selection([('fundamental', 'Fundamental Awareness'), ('novice', 'Novice'), ('intermediate', 'Intermediate'),('advance','Advance'),('expert','Expert')], 'Levels')

class CompetencyTechTypes(models.Model):

    _name = 'comp.tech.types'
    
    name = fields.Char()

class CompetencyTechCategory(models.Model):

    _name = 'comp.tech.category'
    
    name = fields.Char()
    
class CompetencyTech(models.Model):

    _name = 'comp.tech'

    name = fields.Char(required="True")
    types = fields.Many2one('comp.tech.types', required="True")
    category = fields.Many2one('comp.tech.category', required="True")
# ------------------------------------------------------------------------------------------

class NontechNontech(models.Model):

    _name = 'nontech.nontech'
    _rec_name = 'competency_nontech'
    
    # tes2 = fields.Many2one('tes')
    
    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.employee')
    category_competency_nontech = fields.Many2one(related='competency_nontech.category')
    competency_nontech = fields.Many2one('comp.nontech')
    levels_nontech = fields.Selection([('fundamental', 'Fundamental Awareness'), ('novice', 'Novice'), ('intermediate', 'Intermediate'),('advance','Advance'),('expert','Expert')], 'Levels')

class CompetencyNonTechCategory(models.Model):

    _name = 'comp.nontech.category'
    
    name = fields.Char()

class CompetencyNonTech(models.Model):

    _name = 'comp.nontech'
    
    name = fields.Char(required="True")
    category = fields.Many2one('comp.nontech.category', required="True")

# ------------------------------------------------------------------------------------------
class EmployeeEducation(models.Model):

    _name = 'employee.education'

    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    type_id = fields.Many2one('hr.recruitment.degree',
                              "Degree", ondelete="cascade")
    institute_id = fields.Many2one(
        'hr.institute', 'Institutes', ondelete="cascade")
    score = fields.Char()
    qualified_year = fields.Date()
    doc = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_transcript_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Transcripts")


class HrInstitute(models.Model):

    _name = 'hr.institute'

    name = fields.Char()
    country_id = fields.Many2one('res.country', 'Country')
    state_id = fields.Many2one('res.country.state', 'State')


class RecruitmentDegree(models.Model):

    _inherit = "hr.recruitment.degree"

    name = fields.Char("Degree")
    sequence = fields.Integer(
        "Sequence", default=1, help="Gives the sequence \
        order when displaying a list of degrees.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         'The name of the Degree of Recruitment must be unique!'),
        ('seq_uniq', 'unique (sequence)', "Sequence name already exists!")
    ]


class EmployeeCertification(models.Model):

    _name = 'employee.certification'

    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    course_id = fields.Many2one('cert.cert', 'Course Name', ondelete="cascade")
    levels = fields.Char('Bands/Levels of Completion')
    year = fields.Date('Year of completion')
    yearend = fields.Date('Expired Year')
    doc = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_ir_certificate_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Certificates")


class CertCert(models.Model):

    _name = 'cert.cert'

    name = fields.Char('Course Name')
    sequence = fields.Integer("Sequence")

    _sql_constraints = [
        ('cert_unique', 'unique (name)',
         'The name of the Certifications must be unique!'),
        ('seq_uniq', 'unique (sequence)', "Sequence name already exists!")
    ]


class EmployeeProfession(models.Model):

    _name = 'employee.profession'

    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    job_id = fields.Many2one('hr.job', 'Job Title')
    jobtitle = fields.Char('Job Title')
    company = fields.Char('Company')
    industry = fields.Selection([('it', 'IT'),('travel', 'Travel'), ('hr', 'Human Resources'), ('aviation', 'Aviation'), ('hotel',
    'Hotel'), ('transportation','Transportation'), ('banking','Banking'), ('etc','etc.')], string="Industry")
    location = fields.Char()
    from_date = fields.Date('Start Date')
    to_date = fields.Date('End Date')
    doc = fields.Binary('Experience Certificates')

    _sql_constraints = [
        ('to_date_greater', 'check(to_date > from_date)',
         'Start Date of Professional Experience \
         should be less than End Date!'),
    ]
    
    #integrasi dengan technical skill (custom)
    tech_id2 = fields.Many2one(
        'tech.tech', 'Related Skills', ondelete="cascade")

    @api.constrains('from_date', 'to_date')
    def check_from_date(self):
        """
        This method is called when future Start date is entered.
        --------------------------------------------------------
        @param self : object pointer
        """
        date = fields.Datetime.now()
        if (self.from_date > date) or (self.to_date > date):
            raise ValidationError(
                'Future Start Date or End Date \
                in Professional experience is not acceptable!!')


class HrApplicant(models.Model):

    _inherit = 'hr.applicant'

    techskill_ids = fields.One2many(
        'tech.tech', 'applicant_id', 'Technical Skills')
    nontechskill_ids = fields.One2many(
        'nontech.nontech', 'applicant_id', 'Non-Technical Skills')
    education_ids = fields.One2many(
        'employee.education', 'applicant_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'applicant_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession', 'applicant_id', 'Professional Experience')

    @api.multi
    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            address_id = contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])[
                    'contact']
                contact_name = applicant.partner_id.name_get()[0][1]
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write(
                    {'no_of_hired_employee':
                        applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.phone or False,
                    'techskill_ids': [(6, 0, self.techskill_ids.ids)],
                    'nontechskill_ids': [(6, 0, self.nontechskill_ids.ids)],
                    'education_ids': [(6, 0, self.education_ids.ids)],
                    'certification_ids': [(6, 0, self.certification_ids.ids)],
                    'profession_ids': [(6, 0, self.profession_ids.ids)],
                })
                applicant.write({'emp_id': employee.id})
                applicant.job_id.message_post(
                    body=_(
                        'New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired")
                employee._broadcast_welcome()
            else:
                raise UserError(
                    _('You must define an Applied Job and a Contact Name for this applicant.'))
        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        if employee:
            dict_act_window['res_id'] = employee.id
        dict_act_window['view_mode'] = 'form,tree'
        return dict_act_window

