import time
from odoo import models, fields, api
from odoo.exceptions import UserError

class CmSurveyLine(models.Model):
    _name = 'cm.survey.line'
    _description = 'Custom Survey Line'

    header_id = fields.Many2one('cm.survey', string='Survey Reference',
                                index=True, required=True, ondelete='cascade')
    name = fields.Char(string="Name", index=True, copy=False)
    feedback = fields.Text(string="Feedback", copy=False)
    received_date = fields.Datetime(string='Received Date', readonly=True, copy=False)
