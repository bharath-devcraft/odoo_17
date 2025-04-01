# -*- coding: utf-8 -*-

from odoo import models, fields, api

FLEXI_TYPE = [('tltd','TLTD'),
              ('tlbd', 'TLBD'),
              ('blbd', 'BLBD')]

POD_SERVICES = [('disposal', 'Disposal'), ('discharge', 'Discharge'), ('both', 'Both'), ('not_required', 'Not Required')]


class CtDeliveryChallanAccessoriesLine(models.Model):
    _name = 'ct.delivery.challan.acc.line'
    _description = 'Flexi Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.delivery.challan', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    flexi_type = fields.Selection(selection=FLEXI_TYPE, string="Flexi Type", copy=False)
    flexi_layer_type_id = fields.Many2one('cm.flexi.layer.type', string="Layer Type", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    flexi_capacity_id = fields.Many2one('cm.flexi.capacity', string="Capacity", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id = fields.Many2one('cm.vendor.master', string="Preferred Vendor", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    line_count = fields.Integer(string="Line Count", default=0, readonly=True, store=True, compute='_compute_all_line')

    accessory_set_id = fields.Many2one('cm.accessories.set', string="Flexi Bag Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pod_services = fields.Selection(selection=POD_SERVICES, string="POD Services", copy=False)
    bag_req_date = fields.Date(string="Bag Required Date", copy=False)

    qty = fields.Float(string="Qty", digits=(2, 3), default=1)
    bc_line_id = fields.Many2one('ct.business.confirmation.acc.line', string="BC Line ID")
    pending_qty = fields.Float(related='bc_line_id.pending_qty', store=True)
    lot_ids = fields.Many2many('ct.stock.lot', string="Serial No", domain="[('product_id','=',flexi_bag_id),('store_pend_qty','>',0),('po_pend_qty','>',0)]")
    flexi_bag_id = fields.Many2one('product.template', string="Flexi Bag ID", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_bag')])
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    entry_mode = fields.Selection(related='header_id.entry_mode', store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    line_ids = fields.One2many('ct.delivery.challan.acc.details.line', 'header_id', string="Details", copy=True, c_rule=True)

    @api.depends('line_ids')
    def _compute_all_line(self):
        for data in self:
            data.line_count = len(data.line_ids)

    @api.onchange('qty')
    def onchange_qty(self):
        for line in self.line_ids.filtered(lambda l: l.qty):
            line.qty *= self.qty