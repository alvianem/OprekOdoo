from odoo import fields, models, api

class ProjectChecklist(models.Model):
    _name = "project.checklist"

    projectcheck_id = fields.Many2one('project.project')
    #attach_task_id = fields.Many2one('sale.task', string='Sale Task')
    iwodone = fields.Boolean(string = 'IWO', default = False)
    
    charter = fields.Boolean(string = 'Project Charter', default = False)
    uat = fields.Boolean(string = 'UAT', default = False)
    kickoff = fields.Boolean(string = 'Kickoff', default = False)
    
    bast = fields.Boolean(string = 'BAST', default = False)
    handover = fields.Boolean(string = 'Hand Over', default = False)
    
    suratonhold = fields.Boolean(string = 'On Hold Notice', default = False)
    
    suratcancel = fields.Boolean(string = 'Cancel Notice', default = False)
    
    created = fields.Boolean(string = 'Created', default = False)
    
    closed = fields.Boolean(string = 'Closed', default = False)