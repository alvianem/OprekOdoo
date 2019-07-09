from odoo import models, fields, api, _

class tambahan_skill_qualification2(models.Model):
    _inherit = "emp.tech.skills"
    penyambungprofesi = fields.Many2one('employee.profession', string="penyambungProfesi")

class tambahan_skill_qualification1(models.Model):
    _inherit = "employee.profession"
    #model tujuan, field tujuan, string
    penyambungskill = fields.One2many('emp.tech.skills', 'penyambungprofesi', string="penyambungSkill")
    #model tujuan, string
    relatedskill = fields.Many2one('emp.tech.skills', string="Related Skill", related="penyambungskill.tech_id")
    


            