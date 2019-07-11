from datetime import datetime, date
from odoo import models, fields, api, _

class InfoTambahanEmployee(models.Model):
    _inherit = "hr.employee"
    
    religion = fields.Selection([('islam','Islam'),('christian','Christian')], string='Religion')
    homeaddress = fields.Text(string="Home Address")
    housephone = fields.Char(string="Phone")
    linklinkedin = fields.Html(string="Linkedin")
    
    tabelkarir = fields.One2many('tabel_karir', 'penghubung')

class TableCareerHistory (models.Model):
    _name = "tabel_karir"
    _rec_name = "penghubung"
    
    jobposition = fields.Char(string="Job / Role")
    tanggalawal = fields.Date(string="Start Date")
    tanggalakhir = fields.Date(string="End Date")
    penghubung = fields.Many2one('hr.employee', '')
    
    