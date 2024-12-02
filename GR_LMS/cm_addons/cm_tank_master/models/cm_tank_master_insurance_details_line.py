# -*- coding: utf-8 -*-
from odoo import models, fields, api

TYPE_INS = [('external', 'External'), ('cleaning', 'Cleaning'), ('condition', 'Condition'), ('on_hire', 'On Hire'), ('off_hire', 'Off Hire'), ('all', 'All')] 

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

INSURANCE = [('active', 'Active'), ('expired', 'Expired'), ('not_required', 'Not Required')]

RES_COMPANY = 'res.company'

class CmTankMasterInsuranceDetailsLine(models.Model):
    _name = 'cm.tank.master.insurance.details.line'
    _description = 'Insurance Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.tank.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    tank_operator_id= fields.Many2one('cm.tank.operator', string="Insured By(Tank Operator)", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id= fields.Many2one('cm.vendor.master', string="Vendor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    insurance = fields.Selection(selection=INSURANCE, string="Insurance")
    policy_no = fields.Char(string="Policy No")
    validity_from = fields.Date(string="Validity From Date", copy=False)
    validity_to = fields.Date(string="Validity To Date", copy=False)

    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

