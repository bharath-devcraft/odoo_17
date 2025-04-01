# -*- coding: utf-8 -*-

from odoo import fields, models


class CmProductManufacturerBatchInactive(models.TransientModel):
    _name = 'cm.product.manufacturer.batch.inactive'
    _description = "ProductManufacturer Template Batch Inactive"

    master_ids = fields.Many2many('cm.product.manufacturer','cm_product_manufacturer_batch_inactive_rel','wiz_batch_id','manufactuer_id','Inactive Data', default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()
        return {
        'type': 'ir.actions.client',
        'tag': 'reload',
    }

