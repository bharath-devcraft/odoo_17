#-*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError


class travel_payment_master(models.Model):
    _name = 'travel_payment_master.travel_payment_master'
    _description = 'travel_payment_master.travel_payment_master'
    _rec_name = 'code'

    name = fields.Char('Name')
    code = fields.Char('Code')
    description = fields.Text('Description')
    max_days = fields.Integer('Maximum Days')
    starting_point = fields.Char(string='Starting Point')
    max_guest = fields.Integer('Maximum Guest')
    pkg_amount = fields.Float('Package Amount')
    slot_availability = fields.Selection([('yes', 'Yes'),
         ('no', 'No'),
        ], string='Slot Availability', default='yes', readonly=True)
    state = fields.Selection([('draft', 'Draft'),
	('confirm', 'WFA'),('approved', 'Approved'),
	('reject', 'Reject')
        ], string='Status', readonly=True, default='draft')
    reject_remark = fields.Text('Reject Remark')

	
    
    ### Entry Info ###
    company_id = fields.Many2one(
        'res.company',
        'Company Name',
        readonly=True,
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean('Active', default=True)
    user_id = fields.Many2one(
        'res.users',
        'Created By',
        readonly=True,
        default=lambda self: self.env.user.id)
    crt_date = fields.Datetime(
        'Created Date',
        readonly=True,
        default=lambda * a: time.strftime('%Y-%m-%d %H:%M:%S'))
    confirm_date = fields.Datetime('Confirmed Date', readonly=True)
    confirm_user_id = fields.Many2one(
        'res.users', 'Confirmed By', readonly=True)
    approved_date = fields.Datetime('Approved Date', readonly=True)
    approved_user_id = fields.Many2one(
        'res.users', 'Approved By', readonly=True)
    rejected_date = fields.Datetime('Rejected Date', readonly=True)
    rejected_user_id = fields.Many2one(
        'res.users', 'Rejected By', readonly=True)
    update_date = fields.Datetime('Last Updated Date', readonly=True)
    update_user_id = fields.Many2one(
        'res.users', 'Last Updated By', readonly=True)
    
    

    def entry_confirm(self):
        """ entry_confirm """
        if self.state == 'draft':
            self.write({'state': 'confirm',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def entry_approve(self):
        """ entry_approve """
        if self.state == 'confirm':
            self.write({'state': 'approved',
                        'approved_user_id': self.env.user.id,
                        'approved_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def entry_reject(self):
        """ entry_reject """
        if self.state == 'approved':
            if not self.reject_remark:
                raise UserError("EEEEEEEEE")
            self.write({'state': 'reject',
                        'rejected_user_id': self.env.user.id,
                        'rejected_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def unlink(self):
        """ Unlink Funtion """
        for rec in self:
            if rec.state in ('approved','reject'):
                raise UserError('Warning, You can not delete this entry')
            if rec.state in ('draft','confirm'):
                models.Model.unlink(rec)
        return True

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'update_user_id': self.env.user.id})
        return super(travel_package_master, self).write(vals)
