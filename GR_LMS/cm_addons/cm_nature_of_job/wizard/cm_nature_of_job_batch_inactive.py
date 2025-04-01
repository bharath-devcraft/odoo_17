# -*- coding: utf-8 -*-

from odoo import fields, models


class CmNatureOfJobBatchInactive(models.TransientModel):
    _name = 'cm.nature.of.job.batch.inactive'
    _description = "NatureOfJob Template Batch Inactive"

    master_ids = fields.Many2many('cm.nature.of.job', string="Inactive Data", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()
        return {
        'type': 'ir.actions.client',
        'tag': 'reload',
    }

