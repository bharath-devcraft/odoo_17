# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email,valid_phone_no

from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

APPLICABLE_OPTION = [('applicable', 'Applicable'),('not_applicable', 'Not Applicable')]

IR_ATTACHMENT = 'ir.attachment'

class CmVehicleMasterLine(models.Model):
    _name = 'cm.vehicle.master.line'
    _description = 'Additional Contact Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.vehicle.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    amc = fields.Selection(selection=APPLICABLE_OPTION, string="AMC", copy=False)
    amc_provider_id = fields.Many2one('res.partner', string="AMC Provider Name", ondelete='restrict') #, domain=[('status', '=', 'active'),('active_trans', '=', True)])    
    amc_from_date = fields.Date(string="From Date")
    amc_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    amc_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    amc_to_date = fields.Date(string="To Date")
    acm_doc_ids = fields.Many2many(IR_ATTACHMENT,'amc_doc_m2m', string="AMC Document", ondelete='restrict', check_company=True)
    acm_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'acm_oth_doc_ids_m2m', string="Others", ondelete='restrict', check_company=True)
    amc_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

