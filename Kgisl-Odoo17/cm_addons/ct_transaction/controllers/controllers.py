import base64
from datetime import datetime
import json
from odoo import http
from werkzeug.exceptions import BadRequest
import werkzeug.wrappers
import functools
import logging
from odoo.exceptions import AccessError, MissingError, AccessDenied
from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _


_logger = logging.getLogger(__name__)

ACCESS_DENIED_MESSAGE = 'Access Denied'
INTERNAL_SERVER_ERROR_MESSAGE = 'Internal Server Error'
MISSING_ACCESS_TOKEN_MESSAGE = 'Missing Access Token'


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def validate_token(func):
    """."""

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        access_token = request.httprequest.headers.get("Authorization")
        if not access_token:
            return {'status':401,'message': MISSING_ACCESS_TOKEN_MESSAGE}
        
        access_token_data = (request.env["api.access_token"].sudo().search([
            ("token", "=", access_token)], order="id DESC", limit=1))
            
        if (access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id)!= access_token):
            return {'status':401,'message': MISSING_ACCESS_TOKEN_MESSAGE}

        request.session.uid = access_token_data.user_id.id
        request.update_env(user=access_token_data.user_id)
        return func(self, *args, **kwargs)

    return wrap


class CtTransaction(http.Controller):
    @validate_token
    @http.route('/ct_transaction/get_api', type='json', auth='none', methods=['GET','OPTIONS'], csrf=False, cors='*', save_session=False)
    def index(self, **kw):

        try:
            # Clear cookies to avoid session issues
            request.session.logout()
            
            # Parse the JSON data from the request
            json_data = json.loads(request.httprequest.data)
            search_id = json_data.get('search_id')

            if not search_id:
                return {'status': 200, 'message': 'Search ID is must', 'data': [{}]}

            # Fetch the user record
            http.request.env['sale.order'].search([('id', '=', search_id)]) #21

            # Return the response
            return {'status': 200, 'message': 'success', 'data': [{'message':'Hello, World!'}]}
        
        except AccessError as e:
            # Handle AccessError and return a proper message
            return {'status': 403, 'message': ACCESS_DENIED_MESSAGE, 'data': [{'message': str(e)}]}

        except AccessDenied as e:
            # Handle AccessDenied separately if needed
            return {'status': 403, 'message': ACCESS_DENIED_MESSAGE, 'data': [{'message': str(e)}]}
        
        except Exception as e:
            # Handle other exceptions and return a proper message
            return {'status': 500, 'message': INTERNAL_SERVER_ERROR_MESSAGE, 'data': [{'message': str(e)}]}


    @validate_token
    @http.route('/ct_transaction/post_cancel_api', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, save_session=False)
    def cancel_api(self, **kw):
        try:
            # Clear cookies to avoid session issues
            request.session.logout()
            
            # Parse the JSON data from the request
            json_data = json.loads(request.httprequest.data)
            remarks = json_data.get('remarks')
            name = json_data.get('name')

            if name and remarks:
                tran_rec = http.request.env['ct.transaction']
                rec = tran_rec.search([('name', '=', name)])
                if rec:
                    rec.cancel_remark = remarks
                    validation = rec.validations(action='cancel',mode_of_call='Mobile')
                    if not validation:
                        rec.entry_cancel()
                        return {'status': 200, 'message': 'Cancelled successfully', 'data': [{}]}
                    else:
                        return {'status': 200, 'message': validation, 'data': [{}]}
                else:
                    return {'status': 200, 'message': 'No data found', 'data': [{}]}
            else:
                return {'status': 200, 'message': 'Name and Remarks is must', 'data': [{}]}
        
        except AccessError as e:
            # Handle AccessError and return a proper message
            return {'status': 403, 'message': ACCESS_DENIED_MESSAGE, 'data': [{'message': str(e)}]}

        except AccessDenied as e:
            # Handle AccessDenied separately if needed
            return {'status': 403, 'message': ACCESS_DENIED_MESSAGE, 'data': [{'message': str(e)}]}
        
        except Exception as e:
            # Handle other exceptions and return a proper message
            return {'status': 500, 'message': INTERNAL_SERVER_ERROR_MESSAGE, 'data': [{'message': str(e)}]}