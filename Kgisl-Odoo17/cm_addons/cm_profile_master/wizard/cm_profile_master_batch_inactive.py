# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CmProfileMasterBatchIactive(models.TransientModel):
    _name = 'cm.profile.master.batch.inactive'
    _description = "Inactive multiple Profile Master entries"

    master_ids = fields.Many2many(
        string="Master recs to inactive",
        comodel_name='cm.profile.master',
        default=lambda self: self.env.context.get('active_ids'),
    )
    inactive_remark = fields.Text('Inactive Remarks')

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()

