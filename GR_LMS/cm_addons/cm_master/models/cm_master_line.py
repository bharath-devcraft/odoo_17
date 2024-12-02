# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmMasterLine(models.Model):
    _name = 'cm.master.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_code = fields.Char(string="State Code", copy=False, readonly=True, size=252)
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id:
            self.state_code = self.state_id.code
        else:
            self.state_code = False
