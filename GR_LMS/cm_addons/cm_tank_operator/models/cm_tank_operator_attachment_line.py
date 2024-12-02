# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

RES_USERS = 'res.users'

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]
VALIDITY_OPTION = [('perpetual','Perpetual'), ('limited','Limited')]
ENTRY_MODE =  [('manual', 'Manual'),
               ('auto', 'Auto')]

class CmTankOperatorAttachmentLine(models.Model):
    _name = 'cm.tank.operator.attachment.line'
    _description = 'Attachments'
    _order = 'id asc'

    header_id = fields.Many2one('cm.tank.operator', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    attach_desc = fields.Char(string="Description", size=252)
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    attach_date = fields.Datetime(string="Attached Date", copy=False, readonly=True)
    attach_user_id = fields.Many2one(RES_USERS, string="Attached By", copy=False, ondelete='restrict', readonly=True)
    mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", copy=False, tracking=True, default='yes')
    validity = fields.Selection(selection=VALIDITY_OPTION, string="Validity", copy=False, tracking=True)
    from_date = fields.Date(string="Issue Date", c_rule=True)
    validity_period = fields.Integer(string="Validity Period(Months)", copy=False)
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)

    @api.onchange('attachment_ids')
    def onchange_attachment_ids(self):
        if self.attachment_ids:
            self.write({'attach_user_id': self.env.user.id,
                        'attach_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            self.write({'attach_user_id': False,
                        'attach_date': False})

    @api.onchange('from_date', 'validity_period')
    def update_expiry_date_onchange(self):
        if self.from_date and self.validity_period:
            self.expiry_date = self.from_date + relativedelta(months=self.validity_period)
        else:
            self.expiry_date = False

    def unlink(self):
        for rec in self:
            if rec.entry_mode == 'auto':
                raise UserError(_("You can't delete other than manually created attachments"))
            models.Model.unlink(rec)
        return True