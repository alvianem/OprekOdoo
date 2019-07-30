# -*- coding: utf-8 -*-

from odoo import models, api, SUPERUSER_ID
from odoo.exceptions import UserError


class mail_message(models.Model):
    _name = 'mail.message'
    _inherit = 'mail.message'

    @api.multi
    def unlink(self):
        if self._context.get('message_delete'):
            if self._uid != SUPERUSER_ID:
                raise UserError(
                    (u'Only Administrator can delete it.'),
                )
        return super(mail_message, self).unlink()
