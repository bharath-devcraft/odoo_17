import time
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.custom_properties.decorators import is_mobile_num,is_valid_mail

RES_USERS = 'res.users'

CUSTOM_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
        ]

class CmTaskGroupLine(models.Model):
    _name = 'cm.task.group.line'
    _description = 'Custom Task Group Line'

    header_id = fields.Many2one('cm.task.group', string='Task Group Head Ref',
                                index=True, required=True, ondelete='cascade')
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True,
                              tracking=True, copy=False)
    name = fields.Char(string="Name", readonly=True, index=True, copy=False, size=15)
    email = fields.Char(string="Email", copy=False, size=252)
    mobile_no = fields.Char(string="Mobile No", size=15)
    task_manager_id = fields.Many2one(RES_USERS, string="Name", 
                                 ondelete='restrict')
    
    @api.constrains('mobile_no')
    def _check_mobile_no(self):
        if self.mobile_no and is_mobile_num(self.mobile_no):
            raise UserError(
                _(
                    'Mobile number is invalid. Please enter the correct mobile number. Ref: %s'
                ) % self.mobile_no
            )
        return True

    @api.constrains('email')
    def _check_email(self):
        if self.email and is_valid_mail(self.email):
                raise UserError(
                    _(
                        'Email is invalid. Please enter the correct email. Ref : %s'
                    ) % self.email
                )
        return True
