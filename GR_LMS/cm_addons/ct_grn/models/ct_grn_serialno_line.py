# -*- coding: utf-8 -*-

from odoo import models, fields

WARRANTY_STATUS = [('purchase', 'Under Warranty - Purchase'),
                                        ('service', 'Under Warranty - Service'),
                                        ('expired', 'Expired')]

class CtGRNSerialnoLine(models.Model):
    _name = 'ct.grn.serialno.line'
    _description = 'Serial Number'
    _order = 'id asc'

    header_id = fields.Many2one('ct.grn.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    serial_no = fields.Char(string="Serial No", copy=False, size=252)
    qty = fields.Float(string="Quantity", digits=(2, 3),default=1)
    replace_sno = fields.Char(string="Replacement Serial No")
    warranty_details = fields.Text('Warranty Details')
    warranty_status = fields.Selection(selection=WARRANTY_STATUS, string="Warranty Status") 
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    flag_used = fields.Boolean(string="Flag Used", default=False)
    qty_sum = fields.Float(string="Sum", digits = (12,3))
    
    mfg_from_date = fields.Date(status="Mfg Date")
    mfg_month = fields.Float(status="Months")
    mfg_days = fields.Integer(status="Days")
    mfg_expiry_date = fields.Date(status="Expiry Date")
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
