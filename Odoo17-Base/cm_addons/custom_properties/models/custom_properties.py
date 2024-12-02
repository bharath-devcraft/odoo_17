#-*- coding: utf-8 -*-
import odoo.addons
from odoo import models, fields, api, tools
from odoo.exceptions import UserError
import odoo.modules
import os

class CustomProperties(models.Model):
    _name = 'custom.properties'
    _description = 'Custom Properties'

    name = fields.Char()
       
    @api.model
    def auto_execute_psql_procedures(self):
        """ .sql files in the psql_procedures folder will auto execute while module install/upgrade """
        try:
            for root_folder in odoo.addons.__path__:
                file_list = f"{root_folder}/{self._name.replace('.', '_')}/psql_procedures/"
                for sql_file in [files for files in os.listdir(file_list if os.path.exists(file_list)\
                             else None) if files.endswith(".sql")]:
                    f = odoo.tools.misc.file_path(f'{file_list}/{sql_file}')
                    with odoo.tools.misc.file_open(f) as base_sql_file:
                         self.env.cr.execute(base_sql_file.read())
        except FileNotFoundError:
            raise UserError(f"File not found: '.sql' (provided by module '{self._name}').")

    @api.model
    def auto_execute_psql_triggers(self):
        """Automatically executes .sql files in the psql_triggers folder during module installation or upgrade."""
        try:
            for root_folder in odoo.addons.__path__:
                self._execute_sql_files(root_folder, 'psql_triggers')
        except FileNotFoundError as e:
            raise UserError(f"File not found: {str(e)} (provided by module '{self._name}').")
        except Exception as e:
            raise UserError(f"An error occurred during the execution of SQL files: {str(e)}")

    def _execute_sql_files(self, root_folder: str, subfolder: str):
        """Helper method to execute all .sql files in a given subfolder."""
        sql_folder = os.path.join(root_folder, self._name.replace('.', '_'), subfolder)
        if not os.path.exists(sql_folder):
            return

        for sql_file in os.listdir(sql_folder):
            if sql_file.endswith(".sql"):
                sql_file_path = tools.misc.file_path(os.path.join(sql_folder, sql_file))
                with tools.misc.file_open(sql_file_path) as base_sql_file:
                    self.env.cr.execute(base_sql_file.read())


    @api.model
    def retrieve_allowed_char(self):
        return self.env['ir.config_parameter'].sudo().get_param('custom_properties.skip_chars') or ""
