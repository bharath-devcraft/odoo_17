# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CmProductCategoryBatchInactive(models.TransientModel):
    _name = 'cm.product.category.batch.inactive'
    _description = "Inactive multiple product category entries"

    master_ids = fields.Many2many('product.category',string="Inactive Data", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()

