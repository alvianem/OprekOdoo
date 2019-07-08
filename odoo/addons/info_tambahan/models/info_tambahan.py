from datetime import datetime, date
from odoo import models, fields, api, _

class InfoTambahanEmployee(models.Model):
    _inherit = "hr.employee"
    
    religion = fields.Selection([('islam','Islam'),('christian','Christian')], string='Religion')
    homeaddress = fields.Text(string="Home Address")
    housephone = fields.Char(string="Phone")
    linklinkedin = fields.Html(string="Linkedin")

            