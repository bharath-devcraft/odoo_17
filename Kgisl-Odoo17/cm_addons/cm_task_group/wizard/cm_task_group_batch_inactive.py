# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CmTaskGroupBatchInactive(models.TransientModel):
    _name = 'cm.task.group.batch.inactive'
    _description = "Inactive multiple task group entries"

    master_ids = fields.Many2many(
        string="Task group recs to inactive",
        comodel_name='cm.task.group',
        default=lambda self: self.env.context.get('active_ids'),
    )
    inactive_remark = fields.Text('Inactive Remarks')

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()

