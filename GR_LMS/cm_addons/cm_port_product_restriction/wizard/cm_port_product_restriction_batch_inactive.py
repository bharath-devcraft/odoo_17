# -*- coding: utf-8 -*-

from odoo import fields, models


class CmPortProductRestrictionBatchInactive(models.TransientModel):
    _name = 'cm.port.pro.rst.batch.inactive'
    _description = "Port Product Restriction Batch Inactive"

    master_ids = fields.Many2many('cm.port.product.restriction', string="Inactive Data", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()

