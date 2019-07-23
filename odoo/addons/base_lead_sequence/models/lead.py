from odoo import api, models, exceptions, _


class CrmLead(models.Model):
    """Assigns 'ref' from a sequence on creation and copying"""

    _inherit = 'crm.lead'

    @api.multi
    def _get_next_ref(self, vals=None):
        return self.env['ir.sequence'].next_by_code('crm.lead')

    @api.model
    def create(self, vals):
        if not vals.get('ref') and self._needsRef(vals=vals):
            vals['ref'] = self._get_next_ref(vals=vals)
        return super(CrmLead, self).create(vals)

    @api.multi
    def copy(self, default=None):
        default = default or {}
        if self._needsRef():
            default['ref'] = self._get_next_ref()
        return super(CrmLead, self).copy(default)

    @api.multi
    def write(self, vals):
        for lead in self:
            if not vals.get('ref') and lead._needsRef(vals) and \
               not lead.ref:
                vals['ref'] = lead._get_next_ref(vals=vals)

            super(CrmLead, lead).write(vals)
        return True

    @api.multi
    def _needsRef(self, vals=None):
        """
        Checks whether a sequence value should be assigned to a partner's 'ref'

        :param cr: database cursor
        :param uid: current user id
        :param id: id of the partner object
        :param vals: known field values of the partner object
        :return: true iff a sequence value should be assigned to the\
                      partner's 'ref'
        """
        if not vals and not self:  # pragma: no cover
            raise exceptions.UserError(_(
                'Either field values or an id must be provided.'))
        # only assign a 'ref' to commercial partners
        if self:
            vals = {}
            vals['active'] = self.active
        return vals.get('active')

    @api.model
    def _commercial_fields(self):
        """
        Make the partner reference a field that is propagated
        to the partner's contacts
        """
        return super(CrmLead, self)._commercial_fields() + ['ref']
