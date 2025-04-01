# -*- coding: utf-8 -*-

from odoo import models, fields

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

QUALITY_RANK =  [('a','A'),('b', 'B'),('c', 'C'),('d', 'D')]


class CtQuotationsOldTankLine(models.Model):
    _name = 'ct.quotations.old.tank.line'
    _description = 'Old Tank Suggestions'
    _order = 'age desc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    select = fields.Boolean(string="Select", store=True)
    tank_no_id = fields.Many2one('cm.tank.master', string="Tank Number", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)]) #TODO
    depot_id = fields.Many2one('cm.depot.location', string="Current Location", domain=[('status', '=', 'active'),('active_trans', '=', True)], related='tank_no_id.depot_id')
    manufacturing_year = fields.Char(string="Manufacturing Year", size=252)
    age = fields.Integer(string="Age", related='tank_no_id.age')
    quality_rank = fields.Selection(selection=QUALITY_RANK, string="Quality Rank", related='tank_no_id.quality_rank')    
    dom_applicable = fields.Selection(selection=YES_OR_NO, string="Domestication Completed", related='tank_no_id.dom_applicable')    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)