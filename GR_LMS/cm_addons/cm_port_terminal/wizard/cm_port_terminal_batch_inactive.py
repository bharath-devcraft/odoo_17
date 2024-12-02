# -*- coding: utf-8 -*-

from odoo import fields, models

class CmTerminalBatchInactive(models.TransientModel):
    _name = 'cm.port.terminal.batch.inactive'
    _description = "Port Terminal Batch Inactive"

    master_ids = fields.Many2many('cm.port.terminal', string="Inactive Data", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()

