from datetime import datetime
import pytz
from odoo import fields, models

class APIAccessToken(models.Model):
    _name = 'api.access_token'

    token = fields.Char(string="Access Token", required=True)
    user_id = fields.Many2one('res.users', string="User", required=True)
    expires = fields.Datetime(string="Expires", required=True)


    def find_one_or_create_token(self, user_id=None, create=False):
        if not user_id:
            user_id = self.env.user.id
        access_token = (
            self.env['api.access_token'].sudo().search([('user_id', '=', user_id)], order='id DESC', limit=1)
        )
        if access_token:
            access_token = access_token[0]
            if access_token.has_expired():
                access_token = None
        if not access_token:
            return None
        return access_token.token

    def has_expired(self):
        self.ensure_one()

        local_tz = pytz.timezone('Asia/Kolkata')
        current_datetime = datetime.now(pytz.utc).astimezone(local_tz).replace(tzinfo=None)

        return current_datetime > self.expires
