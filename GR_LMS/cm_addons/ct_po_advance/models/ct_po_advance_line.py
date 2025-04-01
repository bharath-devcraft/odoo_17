# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

RES_COMPANY = 'res.company'

class CtPoAdvanceLine(models.Model):
    _name = 'ct.po.advance.line'
    _description = 'Details'
    _order = 'id desc'

    header_id = fields.Many2one('ct.po.advance', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    advance_id = fields.Many2one('ct.po.advance', string="No")
    advance_date = fields.Date(string="Date")
    advance_amt = fields.Float(string="Released Amount", digits = (12,2))
    balance_amt = fields.Float(string="Balance Amount", digits = (12,2))
    ref_no = fields.Char(string="Ref No")
    department_id = fields.Many2one('cm.department', string="Department", related='header_id.department_id', store=True)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)