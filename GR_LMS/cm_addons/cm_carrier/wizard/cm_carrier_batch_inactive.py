# -*- coding: utf-8 -*-

from odoo import fields, models


class CmCarrierBatchInactive(models.TransientModel):
    _name = 'cm.carrier.batch.inactive'
    _description = "Carrier Template Batch Inactive"

    master_ids = fields.Many2many('cm.carrier',string="Inactive Data", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()

