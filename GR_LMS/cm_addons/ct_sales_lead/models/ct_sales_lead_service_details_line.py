# -*- coding: utf-8 -*-
from unicodedata import category

from odoo import models, fields, api, _
from odoo.exceptions import UserError

CUSTOM_STATUS = [
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('new_lead', 'New Lead')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CtSalesServiceDetailsLine(models.Model):
    _name = 'ct.sales.lead.service.details.line'
    _description = 'Service Details'
    _order = 'id desc'

    header_id = fields.Many2one('ct.sales.lead', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    is_select = fields.Boolean(string="Select")
    service_id = fields.Many2one('cm.service', string="Service Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('category', '=', 'main')])
    tank_count = fields.Integer(string="Business Volume(Tank Count)", copy=False)
    business_value = fields.Float(string="Business Value", copy=False)
    product_name = fields.Char(string="Product", size=80, copy=False)
    pol = fields.Char(string="POL", size=80, copy=False)
    pod = fields.Char(string="POD", size=80, copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status")
    rej_remark_id = fields.Many2one('cm.rejection.remark', string="Rejection Remark", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    lost_remark = fields.Text(string="Lost Remarks", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
