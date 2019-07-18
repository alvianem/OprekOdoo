from datetime import datetime, date
from odoo import models, fields, api, _

class InfoTambahanEmployee(models.Model):
    _inherit = "hr.employee"
    
    religion = fields.Selection([('islam','Islam'),('christian','Christian')], string='Religion')
    homeaddress = fields.Text(string="Home Address")
    housephone = fields.Char(string="Phone")
    linklinkedin = fields.Html(string="Linkedin")
    
    tabelkarir = fields.One2many('tabel_karir', 'penghubung')
    join_date = fields.Date(string='Join Date')
    today_date = fields.Date(string='Today Date', readonly='True', compute='_itung_durasi')
    duration = fields.Integer(compute='_itung_durasi_kerja', string='Duration Days')
    
    #asetalgoritma
    hasil_bagi =  fields.Float(string='Duration Years', compute='_itung_hasil_bagi')
    maka = fields.Char(string="maka", compute="_itung_hasil_bagi")
    
    @api.multi
    def _itung_durasi(self):
        for each in self:
            each.today_date = date.today()

    @api.depends('join_date', 'today_date','duration')
    def _itung_durasi_kerja(self):
        if self.join_date and self.today_date:
            d1=datetime.strptime(str(self.join_date),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.today_date),'%Y-%m-%d')
            d3=d2-d1
            self.duration=str(d3.days)

    @api.depends('duration', 'hasil_bagi')
    def _itung_hasil_bagi(self):
        if self.duration:
            pembagi = 366
            self.hasil_bagi= (self.duration / pembagi)
            if self.hasil_bagi==1:
                self.write({'category_ids.category_id': 'General Manager'})
                
class TableCareerHistory (models.Model):
    _name = "tabel_karir"
    _rec_name = "jobposition"
    
    jobposition = fields.Many2one('hr.job', related='penghubung.job_id', string='Job / Role', store=True)
    tanggalawal = fields.Date(string="Start Date")
    tanggalakhir = fields.Date(string="End Date")
    penghubung = fields.Many2one('hr.employee')