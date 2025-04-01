# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CtQuotationsReviseRemarks(models.TransientModel):
    _name = 'ct.quotations.revise.remarks'
    _description = "Revise Remark"

    revise_remark = fields.Text(string="Revise Remarks", copy=False)

    def action_revise(self):
        for rec in  self.env.context.get('active_ids'):
            quotation_add_service = self.env['ct.quotations.add.services.cost.line'].search([('id', '=', rec)])
            vals = {'revise_remark' : self.revise_remark}
            quotation_add_service.revise_action(vals)