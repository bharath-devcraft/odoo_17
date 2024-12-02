# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CtSalesLeadProgressLogLine(models.Model):
    _name = 'ct.sales.lead.progress.log.line'
    _description = 'Details'
    _order = 'crt_date desc'

    header_id = fields.Many2one('ct.sales.lead', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    user_id = fields.Many2one('res.users', string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    next_followup_date = fields.Date(string="Next Follow Up Date", copy=False, tracking=True)
    remarks = fields.Text(string="Remarks", copy=False)
    readonly_flag = fields.Boolean(string="Readonly Flag", default=False, readonly=True)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    def unlink(self):
        for rec in self:
            if rec.readonly_flag == True:
                raise UserError(_("Past date progress log is not allow to delete"))
            models.Model.unlink(rec)
        return True
    
    @api.onchange('next_followup_date')
    def onchange_next_followup_date(self):
        if self.next_followup_date and self.next_followup_date < fields.Date.today():
            raise UserError(_("Next follow up Date should not be lesser than current date"))
