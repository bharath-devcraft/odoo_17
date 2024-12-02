# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CmTransactionBatchCancel(models.TransientModel):
    _name = 'ct.transaction.batch.cancel'
    _description = "Batch Cancel"

    transaction_ids = fields.Many2many(
        string="Batch Cancel",
        comodel_name='ct.transaction',
        default=lambda self: self.env.context.get('active_ids'),
    )
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    batch_info = fields.Text(string="Info", copy=False, default=lambda self: self._compute_dynamic_value())

    def _compute_dynamic_value(self):
        if self.env.context.get('active_ids'):
            invalid_ids = [tran_rec.name if tran_rec.name else tran_rec.name_draft for rec in self.env.context.get('active_ids') for tran_rec in self.env['ct.transaction'].browse(rec) if tran_rec.status not in ('approved','draft')]
            if invalid_ids:
                invalid_vals = 'The following entries are not eligible for batch cancellation : ' +( ','.join(invalid_ids))
                return invalid_vals

    def action_batch_cancel(self):
        for rec in self.transaction_ids:
            rec.cancel_remark = self.cancel_remark
            rec.entry_cancel()

