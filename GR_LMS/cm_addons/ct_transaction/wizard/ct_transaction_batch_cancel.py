# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CtTransactionBatchCancel(models.TransientModel):
    _name = 'ct.transaction.batch.cancel'
    _description = "Batch Cancel"

    transaction_ids = fields.Many2many('ct.transaction', string="Batch Cancel", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    batch_info = fields.Text(string="Info", copy=False, default=lambda self: self._compute_dynamic_value(), c_rule=True)

    def _compute_dynamic_value(self):
        if self.env.context.get('active_ids'):
            invalid_ids = [tran_rec.name if tran_rec.name else tran_rec.draft_name for rec in self.env.context.get('active_ids') for tran_rec in self.env['ct.transaction'].browse(rec) if tran_rec.status not in ('approved','draft')]
            if invalid_ids:
                invalid_vals = "The following entries are not eligible for batch cancellation : " +( ",".join(invalid_ids))
                return invalid_vals

    def action_batch_cancel(self):
        for rec in self.transaction_ids:
            rec.cancel_remark = self.cancel_remark
            rec.entry_cancel()

