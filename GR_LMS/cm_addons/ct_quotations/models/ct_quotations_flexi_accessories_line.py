# -*- coding: utf-8 -*-

from odoo import models, fields, api

FLEXI_TYPE = [('tltd','TLTD'),
              ('tlbd', 'TLBD'),
              ('blbd', 'BLBD')]

class CtQuotationsFlexiAccessoriesLine(models.Model):
    _name = 'ct.quotations.flexi.acc.line'
    _description = 'Flexi Accessories'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    flexi_type = fields.Selection(selection=FLEXI_TYPE, string="Flexi Type", copy=False)
    flexi_layer_type_id = fields.Many2one('cm.flexi.layer.type', string="Layer Type", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    flexi_capacity_id = fields.Many2one('cm.flexi.capacity', string="Capacity", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id = fields.Many2one('cm.vendor.master', string="Preferred Vendor", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    accessory_set_qty = fields.Float(string="Set Qty", digits=(2, 3), default=1)
    line_count = fields.Integer(string="Line Count", default=0, readonly=True, store=True, compute='_compute_all_line')
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    line_ids = fields.One2many('ct.quotations.details.line', 'header_id', string="Details", copy=True, c_rule=True)

    @api.depends('line_ids')
    def _compute_all_line(self):
        for data in self:
            data.line_count = len(data.line_ids)

    @api.onchange('flexi_type', 'flexi_layer_type_id', 'flexi_capacity_id', 'vendor_id')
    def onchange_accessory_set_id(self):
        self.line_ids = [(5, 0, 0)]
        if self.flexi_type and self.flexi_layer_type_id and self.flexi_capacity_id and self.vendor_id:
            acc_rec = self.env['cm.accessories.set'].search([
                ('flexi_type', '=', self.flexi_type),
                ('flexi_layer_type_id', '=', self.flexi_layer_type_id.id),
                ('flexi_capacity_id', '=', self.flexi_capacity_id.id),
                ('vendor_id', '=', self.vendor_id.id),
                ('status', '=', 'active'),
                ('active_trans', '=', True)
            ], limit=1)
            if acc_rec:
                self.line_ids = [
                    (0, 0, {
                        'accessories_id': line.accessories_id.id,
                        'uom_id': line.uom_id.id,
                        'qty': line.qty
                    }) for line in acc_rec.line_ids
                ]