# -*- coding: utf-8 -*-

from odoo import fields, models


class CmRoEmergencyContactBatchInactive(models.TransientModel):
    _name = 'cm.ro.emergency.contact.batch.inactive'
    _description = "RoEmergencyContact Template Batch Inactive"

    master_ids = fields.Many2many(
    'cm.ro.emergency.contact',
        'cm_ro_emergency_contact_rel',
        'cm_ro_emergency_contact_rec_id',
        'cm_ro_emergency_contact_id',    
    string="Inactive Data", default=lambda self: self.env.context.get('active_ids'), c_rule=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)

    def action_batch_inactive(self):
        for rec in self.master_ids:
            rec.inactive_remark = self.inactive_remark
            rec.entry_inactive()
        return {
        'type': 'ir.actions.client',
        'tag': 'reload',
    }

