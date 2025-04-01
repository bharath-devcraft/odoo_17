# -*- coding: utf-8 -*-

from odoo import models, fields, api

CONTAINER_SIZE = [('20_feet_tk', '20 Feet TK'), ('40_feet_tk', '40 Feet TK')]


class CtJobCardContainerDetailsLine(models.Model):
    _name = 'ct.job.card.container.details.line'
    _description = 'Container Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.job.card', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    container_no = fields.Char(string="Container No", copy=False)
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", copy=False)
    serial_no = fields.Char(string="Flexi Bag Serial No", copy=False)


    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
