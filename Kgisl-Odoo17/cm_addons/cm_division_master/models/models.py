# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cm_division_master(models.Model):
#     _name = 'cm_division_master.cm_division_master'
#     _description = 'cm_division_master.cm_division_master'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

