# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

RES_USERS = 'res.users'
RES_COMPANY = 'res.company'

class CtPiPoEntrySupplierDetailsLine(models.Model):
    _name = 'ct.pipo.entry.supplier.details.line'
    _description = 'Supplier Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.pipo.entry', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    brand_id = fields.Many2one('cm.master', string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    supplier_id =  fields.Many2one('ct.vendor.price.list', string="Vendor", copy=False, domain="[('status', '=', 'approved'),('active_trans', '=', True),('product_id', '=', product_id),('brand_id', '=', brand_id)]")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)

    def approved_item_list_form_view(self):
        if self.supplier_id:
            return {
                'name': "Approved Price List",
                'type': 'ir.actions.act_window',
                'res_model': 'ct.vendor.price.list',
                'res_id': self.supplier_id.id,
                'target': 'new',
                'views': [(self.env.ref("ct_vendor_price_list.ct_vendor_price_list_form").id, 'form')],
            }
