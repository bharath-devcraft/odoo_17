# -*- coding: utf-8 -*-

from odoo import models, fields, api

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

class CtQuotationsFlexiBagPricingLine(models.Model):
    _name = 'ct.quotations.flexi.bag.pricing.line'
    _description = 'Flexi Bag Pricing'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    accessory_set_id = fields.Many2one('cm.accessories.set', string="Flexi Bag Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bag_qty = fields.Float(string="Bag Quantity(Nos)", digits=(2, 3))
    acc_is_required = fields.Selection(selection=YES_OR_NO, string="Accessories Required", default='yes') #TODO
    line_count = fields.Integer(string="Line Count", default=0, readonly=True, store=True, compute='_compute_all_line')
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    line_ids = fields.One2many('ct.quotations.acc.details.line', 'header_id', string="Accessories Details", copy=True, c_rule=True)

    @api.depends('line_ids')
    def _compute_all_line(self):
        for data in self:
            data.line_count = len(data.line_ids)

    @api.onchange('accessory_set_id')
    def onchange_accessory_set_id(self):
        self.line_ids = [(5, 0, 0)]
        if self.accessory_set_id:
            self.line_ids = [
                (0, 0, {
                    'accessories_id': line.accessories_id.id,
                    'uom_id': line.uom_id.id,
                    'qty': line.qty
                }) for line in self.accessory_set_id.line_ids
            ]