# -*- coding: utf-8 -*-

from odoo import models, fields

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('quotation_sent', 'Quotation Sent'),
    ('order_released ', 'Order Released'),    
    ('revised', 'Revised'),
    ('cancelled', 'Cancelled')]

class CtQuotationsAdditionalServicesCostLine(models.Model):
    _name = 'ct.quotations.add.services.cost.line'
    _description = 'Additional Services Cost'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    name = fields.Char(string="Quotation No", index=True, size=30, c_rule=True)
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    tot_value = fields.Float(string="Total Value") 
    child_status = fields.Selection(selection=CUSTOM_STATUS, string="Status", default="draft", store=True, tracking=True)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
