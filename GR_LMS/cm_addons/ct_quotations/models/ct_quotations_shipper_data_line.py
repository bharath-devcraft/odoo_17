# -*- coding: utf-8 -*-

from odoo import models, fields

class CtQuotationsShipperDataLine(models.Model):
    _name = 'ct.quotations.shipper.data.line'
    _description = 'Shipper Business Data'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    bl_ref = fields.Char(string="BL Ref No", size=252) #TODO
    bl_date = fields.Date(string="BL Date") #TODO
    demurrage_days = fields.Integer(string="Demurrage Days") #TODO
    demurrage_value = fields.Float(string="Demurrage Value")    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)