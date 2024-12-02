# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api

RES_USERS = 'res.users'
RES_COMPANY = 'res.company'

class CmBusinessVerticalLine(models.Model):
    _name = 'cm.business.vertical.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.business.vertical', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    reason = fields.Text(string="Reason", copy=False)
    crt_date = fields.Datetime(string="Creation Date", copy=False, c_rule=False, readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, c_rule=False, ondelete='restrict', readonly=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.onchange('service_id','reason')
    def onchange_service_id_reason(self):
        if self.service_id and self.reason:
            self.write({'user_id': self.env.user.id,
                        'crt_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            self.write({'user_id': False,
                        'crt_date': False})