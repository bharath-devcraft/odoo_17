# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmRoEmergencyContactLine(models.Model):
    _name = 'cm.ro.emergency.contact.line'
    _description = 'Contact Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.ro.emergency.contact', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    employee_id = fields.Many2one('cm.employee', string="Employee Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    designation_id = fields.Many2one('cm.designation', string="Designation", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    toll_free_no = fields.Char(string="Toll Free Number", size=15, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id.id
            self.designation_id = self.employee_id.designation_id.id
            self.mobile_no = self.employee_id.mobile_no
            self.email = self.employee_id.email
        else:
            self.department_id = False
            self.designation_id = False
            self.mobile_no = ''
            self.email = ''
