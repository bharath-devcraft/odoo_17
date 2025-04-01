# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

ACCOUNT_TAX = 'account.tax'

class CtDomsBusinessConfirmationCustomerPricingDetailsLine(models.Model):
    _name = 'ct.doms.bus.con.cus.pri.details.line'
    _description = 'Pricing Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.doms.business.confirmation', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    chrg_head_id = fields.Many2one('cm.charges.heads', string="Charges Head", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)    
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Quantity", digits=(2, 3))	
    unit_price = fields.Float(string="Unit Price")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)
    tax_ids = fields.Many2many(ACCOUNT_TAX, string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    disc_amt = fields.Float(string="Discount Amount(-)")    
    disc_per = fields.Float(string="Discount(%)")
    unitprice_wt = fields.Float(string="Unit Price(WT)", help="Unit price with Taxes")
    taxable_amt = fields.Float(string="Taxable Value")    
    tax_amt = fields.Float(string="Tax Value")    	
    tot_amt = fields.Float(string="Total Value")
    line_tot_amt = fields.Float(string="Line Total")    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
                
                        
    