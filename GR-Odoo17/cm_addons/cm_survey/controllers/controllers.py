import base64
from datetime import datetime
import json
import pytz
from odoo import http,fields
from werkzeug.exceptions import BadRequest
import werkzeug.wrappers
import functools
import logging
from odoo.exceptions import AccessError, MissingError, AccessDenied
from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _


_logger = logging.getLogger(__name__)

CLOSED_URL = '/survey_closed'
ALREADY_SUBMITTED_URL = '/feedback_already_submitted'
INVALID_URL_TOKEN = '/invalid_transaction_token'

class CmSurvey(http.Controller):
    
    def _fetch_from_access_token(self, survey_token):
        survey_sudo = request.env['cm.survey'].with_context(active_test=False).sudo().search([('access_token', '=', survey_token)],limit=1)

        return survey_sudo

    @http.route('/custom/survey/start/<string:survey_token>', type='http', auth='public', website=True, sitemap=False, multilang=False)
    def custom_survey_start(self, survey_token, **post):

        survey_sudo = self._fetch_from_access_token(survey_token)
        if survey_sudo and survey_sudo.status == 'active' and survey_sudo.from_date <= fields.Date.today() <= survey_sudo.to_date:
            return request.render('cm_survey.home_page', {'survey_token': survey_sudo.access_token,'survey_sudo': survey_sudo})
        elif survey_sudo and (survey_sudo.status != 'active' or not survey_sudo.from_date <= fields.Date.today() <= survey_sudo.to_date):
            return request.redirect(CLOSED_URL)
        elif survey_sudo:
            return request.redirect(ALREADY_SUBMITTED_URL)
        else:
            return request.redirect(INVALID_URL_TOKEN)

    @http.route('/feedback_form', type='http', auth='public', website=True, sitemap=False, multilang=False)
    def custom_survey_feedback(self, survey_token, **post):
        survey_sudo = self._fetch_from_access_token(survey_token)
        if survey_sudo and survey_sudo.status == 'active' and survey_sudo.from_date <= fields.Date.today() <= survey_sudo.to_date:
            return request.render('cm_survey.feedback_form', {'survey_token': survey_sudo.access_token,'survey_sudo': survey_sudo})
        elif survey_sudo and (survey_sudo.status != 'active' or not survey_sudo.from_date <= fields.Date.today() <= survey_sudo.to_date):
            return request.redirect(CLOSED_URL)
        elif survey_sudo:
            return request.redirect(ALREADY_SUBMITTED_URL)
        else:
            return request.redirect(INVALID_URL_TOKEN)

    @http.route('/custom/survey/submit_feedback', type='http', auth='public', website=True, csrf=True, methods=['POST'], sitemap=False, multilang=False)
    def submit_feedback(self, **post):
        survey_token = post.get('survey_token')
        feedback = post.get('feedback')
        name = post.get('name')

        survey_sudo = self._fetch_from_access_token(survey_token)
        if survey_sudo and survey_sudo.status == 'active' and survey_sudo.from_date <= fields.Date.today() <= survey_sudo.to_date:
            survey_line = []
            survey_line.append((0,0,{'name':name, 'feedback':feedback, 'received_date':fields.Datetime.now()}))
            survey_sudo.line_ids = survey_line
            return request.redirect('/thank_you')
        elif survey_sudo and (survey_sudo.status != 'active' or not survey_sudo.from_date <= fields.Date.today() <= survey_sudo.to_date):
            return request.redirect(CLOSED_URL)
        elif survey_sudo:
            return request.redirect(ALREADY_SUBMITTED_URL)
        else:
            return request.redirect(INVALID_URL_TOKEN)

    @http.route('/thank_you', type='http', auth='public', website=True, sitemap=False, multilang=False)
    def thank_you(self, **post):
        return request.render('cm_survey.thank_you')

    @http.route(CLOSED_URL, type='http', auth='public', website=True, sitemap=False, multilang=False)
    def survey_closed(self, **post):
        return request.render('cm_survey.survey_closed')

    @http.route(ALREADY_SUBMITTED_URL, type='http', auth='public', website=True, sitemap=False, multilang=False)
    def feedback_already_submitted(self, **post):
        return request.render('cm_survey.feedback_already_submitted')

    @http.route(INVALID_URL_TOKEN, type='http', auth='public', website=True, sitemap=False, multilang=False)
    def invalid_transaction_token(self, **post):
        return request.render('cm_survey.invalid_transaction_token')

    @http.route('/404', type='http', auth='public', website=True, sitemap=False, multilang=False)
    def custom_404(self, **post):
        return request.render('cm_survey.custom_404')

    @http.route('/<path:remaining>', type='http', auth='public', website=True, sitemap=False, multilang=False)
    def catch_all(self, remaining, **post):
        return request.redirect('/404')
