# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

BOUND_OPTIONS = [('east', 'East'),
            ('west', 'West')]

CUSTOM_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

VALIDITY_OPTION = [('perpetual','Perpetual'), ('limited','Limited')]


class CmKycLine(models.Model):
    _name = 'cm.kyc.line'       
    _description = 'Document Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.kyc', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", copy=False, tracking=True)
    validity = fields.Selection(selection=VALIDITY_OPTION, string="Validity", copy=False, tracking=True)
    validity_period = fields.Integer(string="Validity Period(Months)", copy=False)
    remark = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
