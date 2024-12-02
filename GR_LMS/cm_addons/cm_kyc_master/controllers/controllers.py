#-*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

import logging
from ast import literal_eval
from datetime import date

_logger = logging.getLogger(__name__)

class CmKyc(http.Controller):
    @http.route('/custom/required_fields', type='json', auth='user')
    def disable_popup_notification(self, **kw):
        fieldName = kw.get('fieldName')
        model = kw.get('model')
        company_id = request.env['res.company'].search([('id','=',kw.get('company_id'))])
        source = request.env['cm.kyc.master'].search([('model_id.model','=',model),('country_id','=', company_id.country_id.id),('status', 'in', ['active'])], limit=1, order="id desc")
        return True if fieldName in [field.name for field in source.man_fields_ids] else False
