import json
import pytz
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
import secrets

class AccessToken(http.Controller):
    @http.route('/api/login', methods=['POST','OPTIONS'], type='json', auth='none', csrf=False, cors='*')
    def token(self, **kw):
        json_data = json.loads(request.httprequest.data)
        input_user_name = json_data.get('username')
        input_password = json_data.get('password')

        if not (input_user_name and input_password):
            return {'status': 401, 'message': "Username and Password are required", 'data': [{}]}

        res_users = request.env['res.users'].sudo().search([
            ('status', '=', 'active'),('login', '=', input_user_name)], limit=1)
        
        if not res_users:
            return {'status': 401, 'message': "Wrong Username and Password", 'data': [{}]}

        query = """SELECT COALESCE(password, '') FROM res_users WHERE id=%s"""
        request.env.cr.execute(query, (res_users.id,))
        [hashed] = request.env.cr.fetchone()

        valid = res_users._crypt_context().verify_and_update(input_password, hashed)
        if not valid[0]:
            return {'status':401, 'message': "Wrong Username and Password", 'data':[{}]}
        
        local_tz = pytz.timezone('Asia/Kolkata')
        current_datetime = datetime.now(pytz.utc).astimezone(local_tz).replace(tzinfo=None)
        expire_datetime = current_datetime + timedelta(days=30)

        new_token = secrets.token_urlsafe(32)
        request.env['api.access_token'].sudo().create({
                    'user_id': res_users.id,
                    'expires': expire_datetime,
                    'token': new_token})

        return {
            'status': 200,
            'message': "Success",
            'data': [{
                'user_id': res_users.id,
                'username': input_user_name,
                'access_token': new_token,
            }]
        }


    @http.route('/api/login', methods=['DELETE'], type='json', auth='none', csrf=False, cors='*')
    def delete(self, **kw):
        _token = request.env['api.access_token']
        access_token = request.httprequest.headers.get('Authorization')
        access_token = _token.sudo().search([('token', '=', access_token)])
        if not access_token:
            return {'status':400, 'message':"No access token was provided in request", 'data':[{}]}
        for token in access_token:
            token.unlink()
        return {'status':200, 'message':"Token successfully deleted", 'data':[{}], 'delete': True}