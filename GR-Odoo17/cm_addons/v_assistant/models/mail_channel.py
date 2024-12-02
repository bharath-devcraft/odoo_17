# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)


from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo import tools

from . import brain

class Channel(models.Model):
    _inherit = 'discuss.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        
        print("hey hari,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",message)

        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        
        v_assistant_channel_id = self.env.ref('v_assistant.channel_v_assistant')
        user_v_assistant = self.env.ref("v_assistant.user_v_assistant")
        partner_v_assistant = self.env.ref("v_assistant.partner_v_assistant")
        author_id = msg_vals.get('author_id')
        assistant_name = str(partner_v_assistant.name or '') + ', '
        print("sssssssssassistant_name",assistant_name)
        print("msg_vals.get('record_name', '')",msg_vals.get('record_name', ''))
        prompt = msg_vals.get('body')

        if not prompt:
           return rdata
        Partner = self.env['res.partner']


        if author_id:
           partner_id = Partner.browse(author_id)
           
        if author_id != partner_v_assistant.id: #and assistant_name in msg_vals.get('record_name', '') or 'V Assistant,' in msg_vals.get('record_name', '') and self.channel_type == 'channel':
            try:
                res = self._get_ai_response(prompt=prompt)
                res_html = tools.plaintext2html(res)
                self.with_user(user_v_assistant).message_post(body=res_html, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                 raise UserError(_(e))

        elif author_id != partner_v_assistant.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == v_assistant_channel_id.id:
            try:
                res = self._get_ai_response(prompt=prompt)
                v_assistant_channel_id.with_user(user_v_assistant).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))
                
        return rdata

    def _get_ai_response(self, prompt):
        return brain.run_alexa(self.env,prompt)
