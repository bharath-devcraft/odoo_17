# -*- coding: utf-8 -*-
from odoo import models, fields, api

from dateutil.relativedelta import relativedelta

TYPE_INS = [('external', 'External'), ('cleaning', 'Cleaning'), ('condition', 'Condition'), ('on_hire', 'On Hire'), ('off_hire', 'Off Hire'), ('all', 'All')] 

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

PASS_FAIL = [('pass', 'Pass'), ('fail', 'Fail')]

RES_COMPANY = 'res.company'

class CmTankMasterLine(models.Model):
    _name = 'cm.tank.master.line'
    _description = 'Surveyor Inspection Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.tank.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    type_ins = fields.Selection(selection=TYPE_INS, string="Type of Inspection")
    ins_status = fields.Selection(selection=PASS_FAIL, string="Inspection Status")
    inspected_by = fields.Char(string="Inspected By")
    last_inspection_date = fields.Date(string="Inspected Date", copy=False)
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    validity_period = fields.Integer(string="Validity Period(Months)", copy=False)
    valid_to_date = fields.Date(string="Validity To Date", copy=False)

    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.onchange('last_inspection_date','validity_period')
    def onchange_issue_date(self):
        if self.last_inspection_date and self.validity_period:
            self.valid_to_date = self.last_inspection_date + relativedelta(days=+self.validity_period)