# -*- coding: utf-8 -*-
from odoo import models, fields, api

TYPE_INS = [('external', 'External'), ('cleaning', 'Cleaning'), ('condition', 'Condition'), ('on_hire', 'On Hire'), ('off_hire', 'Off Hire'), ('all', 'All')] 

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

PASS_FAIL = [('pass', 'Pass'), ('fail', 'Fail')]

RES_COMPANY = 'res.company'

class CmTankMasterRecentlyUsedProductLine(models.Model):
    _name = 'cm.tank.master.recently.used.product.line'
    _description = 'Recently used Product'
    _order = 'id asc'

    header_id = fields.Many2one('cm.tank.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    product_id = fields.Many2one('cm.product', string="Product Name", copy=False, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    dg_product = fields.Selection(selection=YES_OR_NO, string="Dangerous Goods")
    bl_ref_no = fields.Char(string="BL Reference No")
    date = fields.Date(string="Date", copy=False)

    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

