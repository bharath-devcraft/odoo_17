import time
from odoo import models, fields, api
from odoo.exceptions import UserError

class CmMasterLine(models.Model):
    _name = 'cm.master.line'
    _description = 'Custom Master Line'

    header_id = fields.Many2one('cm.master', string='Master Head Ref',
                                index=True, required=True, ondelete='cascade')
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    state_code = fields.Char(string='State Code', help='The state code.', required=True)
    note = fields.Html(string="Note", copy=False)

    #onchange
    @api.onchange('state_id')
    def _onchange_state_id(self):
        '''onchange_state_id'''
        if self.state_id:
            self.state_code = self.state_id.code
        else:
            self.state_code = False
