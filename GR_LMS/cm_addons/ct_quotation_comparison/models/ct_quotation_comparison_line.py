# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_VENDOR_MASTER = 'cm.vendor.master'
RES_CURRENCY = 'res.currency'
ACCOUNT_TAX = 'account.tax'

WARRANTY =  [('from_grn', 'From GRN Date'),
            ('from_invoice', 'From Sup Invoice Date'),
            ('custom', 'Custom/Commissioning Date')]

class CtQuotationComparisonLine(models.Model):
    _name = 'ct.quotation.comparison.line'
    _description = 'Quotation Comparison Line'

    header_id = fields.Many2one('ct.quotation.comparison', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one('cm.master', string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    brand_desc = fields.Char('Brand')
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(12, 3))
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


    vendor_1_qs_line_id = fields.Integer(string="QS Line ID")
    vendor_1_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 1", readonly=True)
    vendor_1_select = fields.Boolean(string="LP")
    vendor_1_qty = fields.Float(string="Qty", readonly=True, digits=(16, 3))
    vendor_1_price = fields.Float(string="Rate", digits=(16, 3), store=True)
    vendor_1_value = fields.Float(string="Value", digits=(16, 2))
    vendor_1_subtotal = fields.Float(string="Subtotal",store=True, digits=(12, 2))
    vendor_1_total_discount = fields.Float(string="Total Discount Amount",store=True, digits=(12, 2))
    vendor_1_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_1_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_vendor_1_tax', 'qc_line_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_1_discount = fields.Float(string="Dis(%)", store=True,digits=(16, 2))
    vendor_1_discount_amt = fields.Float(string="Dis Amt", store=True,digits=(16, 2))
    vendor_1_tax_amt = fields.Float(string="Tax Amt", store=True,digits=(16, 2))
    vendor_1_warranty_period = fields.Float(string="W", digits=(16, 2))
    vendor_1_warranty_from = fields.Selection(selection=WARRANTY, string="Warranty From")

    vendor_2_qs_line_id = fields.Integer(string="QS Line ID")
    vendor_2_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 1", readonly=True)
    vendor_2_select = fields.Boolean(string="LP")
    vendor_2_qty = fields.Float(string="Qty", readonly=True, digits=(16, 3))
    vendor_2_price = fields.Float(string="Rate", digits=(16, 3))
    vendor_2_value = fields.Float(string="Value", digits=(16, 2))
    vendor_2_subtotal = fields.Float(string="Subtotal",store=True, digits=(12, 2))
    vendor_2_total_discount = fields.Float(string="Total Discount Amount",store=True, digits=(12, 2))
    vendor_2_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_2_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_vendor_2_tax', 'qc_line_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_2_discount = fields.Float(string="Dis(%)", store=True,digits=(16, 2))
    vendor_2_discount_amt = fields.Float(string="Dis Amt", store=True,digits=(16, 2))
    vendor_2_tax_amt = fields.Float(string="Tax Amt", store=True,digits=(16, 2))
    vendor_2_warranty_period = fields.Float(string="W", digits=(16, 2))
    vendor_2_warranty_from = fields.Selection(selection=WARRANTY, string="Warranty From")

    vendor_3_qs_line_id = fields.Integer(string="QS Line ID")
    vendor_3_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 1", readonly=True)
    vendor_3_select = fields.Boolean(string="LP")
    vendor_3_qty = fields.Float(string="Qty", readonly=True, digits=(16, 3))
    vendor_3_price = fields.Float(string="Rate", digits=(16, 3))
    vendor_3_value = fields.Float(string="Value", digits=(16, 2))
    vendor_3_subtotal = fields.Float(string="Subtotal", store=True, digits=(12, 2))
    vendor_3_total_discount = fields.Float(string="Total Discount Amount", store=True, digits=(12, 2))
    vendor_3_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_3_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_vendor_3_tax', 'qc_line_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_3_discount = fields.Float(string="Dis(%)", store=True,digits=(16, 2))
    vendor_3_discount_amt = fields.Float(string="Dis Amt", store=True,digits=(16, 2))
    vendor_3_tax_amt = fields.Float(string="Tax Amt", store=True,digits=(16, 2))
    vendor_3_warranty_period = fields.Float(string="W", digits=(16, 2))
    vendor_3_warranty_from = fields.Selection(selection=WARRANTY, string="Warranty From")

    vendor_4_qs_line_id = fields.Integer(string="QS Line ID")
    vendor_4_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 1", readonly=True)
    vendor_4_select = fields.Boolean(string="LP")
    vendor_4_qty = fields.Float(string="Qty", readonly=True, digits=(16, 3))
    vendor_4_price = fields.Float(string="Rate", digits=(16, 3))
    vendor_4_value = fields.Float(string="Value", digits=(16, 2))
    vendor_4_subtotal = fields.Float(string="Subtotal", store=True, digits=(12, 2))
    vendor_4_total_discount = fields.Float(string="Total Discount Amount", store=True, digits=(12, 2))
    vendor_4_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_4_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_vendor_4_tax', 'qc_line_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_4_discount = fields.Float(string="Dis(%)", store=True,digits=(16, 2))
    vendor_4_discount_amt = fields.Float(string="Dis Amt", store=True,digits=(16, 2))
    vendor_4_tax_amt = fields.Float(string="Tax Amt", store=True,digits=(16, 2))
    vendor_4_warranty_period = fields.Float(string="W", digits=(16, 2))
    vendor_4_warranty_from = fields.Selection(selection=WARRANTY, string="Warranty From")
