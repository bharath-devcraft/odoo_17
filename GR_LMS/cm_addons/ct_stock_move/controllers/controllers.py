# -*- coding: utf-8 -*-

import json
from odoo import http
import functools
from odoo.exceptions import AccessError, AccessDenied
from odoo.http import request
import secrets

ACCESS_DENIED_MESSAGE = "Access Denied"
INTERNAL_SERVER_ERROR_MESSAGE = "Internal Server Error"
MISSING_ACCESS_TOKEN_MESSAGE = "Missing Access Token"
TOKEN_EXPIRED_MESSAGE = "Access Token Expired"

def validate_token(func):

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get('Authorization')
        if not access_token:
            return {'status':401,'message': MISSING_ACCESS_TOKEN_MESSAGE}
        
        access_token_data = (request.env['api.access_token'].sudo().search([
            ('token', '=', access_token)], order='id DESC', limit=1))
            
        if (access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id)!= access_token):
            return {'status':401,'message': TOKEN_EXPIRED_MESSAGE}

        request.session.uid = access_token_data.user_id.id
        request.update_env(user=access_token_data.user_id)
        return func(self, *args, **kwargs)

    return wrap


class CtNocostTransaction(http.Controller):
    @validate_token
    @http.route('/ct_nocost_transaction/get_api', type='json', auth='none', methods=['GET','OPTIONS'], csrf=False, cors='*', save_session=False)
    def nocost_transaction_get_api(self, **kw):

        try:
            json_data = json.loads(request.httprequest.data)
            search_id = json_data.get('search_id')

            if not search_id:
                return {'status': 200, 'message': "Search ID is must", 'data': [{}]}

            trans_rec = http.request.env['ct.nocost.transaction'].search([('id', '=', search_id)], limit=1)

            return {'status': 200, 'message': "success", 'data': [{'message':f"Testing API - {trans_rec.name}"}]}
        
        except (AccessError, AccessDenied) as e:
            return {'status': 403, 'message': ACCESS_DENIED_MESSAGE, 'data': [{'message': str(e)}]}

        except Exception as e:
            return {'status': 500, 'message': INTERNAL_SERVER_ERROR_MESSAGE, 'data': [{'message': str(e)}]}


    @validate_token
    @http.route('/ct_nocost_transaction/post_cancel_api', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, save_session=False)
    def nocost_transaction_cancel_api(self, **kw):
        try:
            json_data = json.loads(request.httprequest.data)
            remarks = json_data.get('remarks')
            name = json_data.get('name')

            if not (name and remarks):
                return {'status': 400, 'message': "Name and Remarks are required", 'data': [{}]}

            tran_rec = http.request.env['ct.nocost.transaction']
            rec = tran_rec.search([('name', 'like', name)])

            if not rec:
                return {'status': 404, 'message': "No data found", 'data': [{}]}

            rec.cancel_remark = remarks
            rec.entry_cancel()
            return {'status': 200, 'message': "Cancelled successfully", 'data': [{}]}

        except (AccessError, AccessDenied) as e:
            return {'status': 403, 'message': ACCESS_DENIED_MESSAGE, 'data': [{'message': str(e)}]}

        except Exception as e:
            return {'status': 500, 'message': INTERNAL_SERVER_ERROR_MESSAGE, 'data': [{'message': str(e)}]}
        

    @http.route('/dashboard/statistics', type='json', auth='user')
    def get_statistics(self):
        return {
            'average_quantity': secrets.randbelow(9) + 4,
            'average_time': secrets.randbelow(120) + 4,
            'nb_cancelled_orders': secrets.randbelow(50) + 4,
            'nb_new_orders': secrets.randbelow(10) + 4,
            'orders_by_size': {
                'm': secrets.randbelow(150) + 4,
                's': secrets.randbelow(150) + 4,
                'xl': secrets.randbelow(150) + 4,
            },
            'total_amount': secrets.randbelow(1000) + 100
        }
