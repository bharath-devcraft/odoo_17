# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

DAY = [
		('monday', 'Monday'),
		('tuesday', 'Tuesday'),
		('wednesday', 'Wednesday'),
		('thursday', 'Thursday'),
		('friday', 'Friday'),
		('saturday', 'Saturday'),
		('sunday', 'Sunday')]

class CmGrHolidayLine(models.Model):
	_name = 'cm.gr.holiday.line'
	_description = 'Details'
	_order = 'id asc'

	header_id = fields.Many2one('cm.gr.holiday', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	date = fields.Date(string="Date", copy=False)
	day = fields.Selection(selection=DAY, string="Day", copy=False)
	occasion = fields.Char(string="Occasion")
	note = fields.Html(string="Notes", copy=False, sanitize=False)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

	@api.onchange('state_id')
	def onchange_state_id(self):
		if self.state_id:
			self.state_code = self.state_id.code
		else:
			self.state_code = False
