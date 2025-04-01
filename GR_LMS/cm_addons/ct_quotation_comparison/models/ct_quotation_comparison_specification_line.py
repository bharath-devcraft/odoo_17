# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

RES_USERS = 'res.users'
RES_COMPANY = 'res.company'

class CtQuotationComparisonSpecificationLine(models.Model):
    _name = 'ct.quotation.comparison.specification.line'
    _description = 'Specification'
    _order = 'description asc'

    header_id_1 = fields.Many2one('ct.quotation.comparison', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    header_id_2 = fields.Many2one('ct.quotation.comparison', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    header_id_3 = fields.Many2one('ct.quotation.comparison', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    header_id_4 = fields.Many2one('ct.quotation.comparison', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    sequence_no = fields.Integer(string="Sequence No")
    title = fields.Char(string="Title")
    description = fields.Char(string="Description")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    status = fields.Selection(related='header_id_1.status', store=True, c_rule=True)
