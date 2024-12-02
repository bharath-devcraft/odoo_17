# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api

RES_USERS = 'res.users'
RES_COMPANY = 'res.company'

ATTACHMENTS = [
		('gst', 'GST Certificate'),
		('iec', 'IEC Certificate'),
		('pan', 'PAN'),
		('kyc', 'KYC Details'),
		('cancel_cheque', 'Cancel Cheque leaf'),
		('bank', 'Bank Details'),
		('vat', 'VAT Certificate'),
		('company_reg', 'Company Reg Certificate'),
		('uaci', 'UACI Certificate'),
		('tax_reg', 'Tax Registration')]

class CmCustomerAttachmentLine(models.Model):
	_name = 'cm.customer.attachment.line'
	_description = 'Attachments'
	_order = 'id asc'

	header_id = fields.Many2one('cm.customer', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	attach_desc = fields.Char(string="Description", size=252)
	attachments = fields.Selection(selection=ATTACHMENTS, string="Attachments", copy=False, tracking=True)
	attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
	attach_date = fields.Datetime(string="Attached Date", copy=False, readonly=True)
	attach_user_id = fields.Many2one(RES_USERS, string="Attached By", copy=False, ondelete='restrict', readonly=True)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

	@api.onchange('attachment_ids')
	def onchange_attachment_ids(self):
		if self.attachment_ids:
			self.write({'attach_user_id': self.env.user.id,
						'attach_date': time.strftime('%Y-%m-%d %H:%M:%S')})
		else:
			self.write({'attach_user_id': False,
						'attach_date': False})
