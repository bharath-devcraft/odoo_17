# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api

RES_USERS = 'res.users'
RES_COMPANY = 'res.company'

class CmCustomerHistoryLine(models.Model):
	_name = 'cm.customer.history.line'
	_description = 'History'
	_order = 'id asc'

	header_id = fields.Many2one('cm.customer', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	feedback = fields.Char(string="Feedback", size=252)
	crt_date = fields.Datetime(string="Added Date", copy=False, readonly=True)
	user_id = fields.Many2one(RES_USERS, string="Added By", copy=False, ondelete='restrict', readonly=True)
	remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

	@api.onchange('feedback')
	def onchange_feedback(self):
		if self.feedback:
			self.write({'user_id': self.env.user.id,
						'crt_date': time.strftime('%Y-%m-%d %H:%M:%S')})
		else:
			self.write({'user_id': False,
						'crt_date': False})
