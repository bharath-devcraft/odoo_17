#-*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

import logging
from ast import literal_eval
from datetime import date

_logger = logging.getLogger(__name__)

class CustomProperties(http.Controller):

    # Global search related logic.
    @http.route("/master/search", methods=["POST"], type="json", auth="user")
    def master_search(self, search):
        data = []
        if search['query'] != '':
            config_settings = request.env['ir.config_parameter'].sudo().get_param(
                'custom_properties.master_search_installed_ids')
            if search['options'] == "only-name" and config_settings:
                config_settings_str = literal_eval(config_settings)
                config_settings_ids = [int(id_str) for id_str in config_settings_str]
                config_modules = request.env['ir.module.module'].sudo().search([
                    ('id', 'in', config_settings_ids)])
                for module in config_modules:
                    request.env.cr.execute(
                                    "SELECT name,id FROM %s WHERE name ILIKE '%s'" % (
                                        module.name, '%' + search['query'] + '%'))
                    records = request.env.cr.dictfetchall()
                    if records:
                        for record in records:
                            data.append([{
                                        'title': request.env[module.name.replace('_', '.')]._description,
                                        'fieldname': request.env[module.name.replace('_', '.')]._fields['name'].string,
                                        'row_data': record['name'],
                                        'rec_id': request.env[module.name.replace('_', '.')].\
                                 search([('id', '=', record['id'])], limit=1).id,
                                        'model': request.env[module.name.replace('_', '.')]._name
                                    }])
                        request.env.cr.commit()
            elif search['options'] == "global":
                try:
                    request.env.cr.execute("select * from global_search('%s')"%('%'+ search['query'] + '%'))
                    records = request.env.cr.dictfetchall()
                    if records:
                       for rec in records:
                           rec['title'] = request.env[rec['tablename'].replace('_', '.')]._description
                           rec['fieldname'] = request.env[rec['tablename'].replace('_', '.')]._fields[rec['columnname']].string
                           rec['model'] = request.env[rec['tablename'].replace('_', '.')]._name
                           rec['rec_id'] = request.env[rec['tablename'].replace('_', '.')].\
                                 search([(rec['columnname'], '=', rec['row_data'])], limit=1).id
                           data.append([rec])
                    request.env.cr.commit()
                except Exception as e:
                    _logger.debug(e, "Error in the global search endpoint.")
                    request.env.cr.rollback()
        return data
    
    # Pop-up notification today disable.
    @http.route('/custom/popup/disable', type='json', auth='user')
    def disable_popup_notification(self, **kw):
        user_id = kw.get('user_id')
        notify_name = kw.get('notify_name')
        if user_id and notify_name:
            try:
                notify_rec = request.env['cp.popup.notification']
                today_date = date.today()

                existing_record = notify_rec.search([
                    ('name', '=', notify_name),
                    ('user_id', '=', user_id),
                    ('entry_date', '=', today_date)
                ], limit=1)

                if not existing_record:
                    notify_rec.create({
                        'name': notify_name,
                        'user_id': user_id,
                        'entry_date': today_date
                    })

            except Exception as e:
                _logger.error(f"An error occurred: {e}")
