# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ast import literal_eval

YEARS = [('fiscal_year', "Fiscal Year"),
         ('calendar_year',"Calendar Year")]

IR_CONFIG_PARAMETER = 'ir.config_parameter'

SERVER_SIDE_VALIDATION = 'custom_properties.server_side_validation'
SKIP_CHARS = 'custom_properties.skip_chars'
RULE_CHECKER_MASTER = 'custom_properties.rule_checker_master'
RULE_CHECKER_TRANSACTION = 'custom_properties.rule_checker_transaction'
SEQ_NUM_RESET = 'custom_properties.seq_num_reset'
DEL_SELF_DRAFT_ENTRY = 'custom_properties.del_self_draft_entry'
MIN_CHAR_LENGTH = 'custom_properties.min_char_length'

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    server_side_validation = fields.Boolean("Enabled Server Side Global Validation",\
                     config_parameter=SERVER_SIDE_VALIDATION, default=True)
    skip_chars = fields.Char("Allowed Special Characters",\
                     config_parameter=SKIP_CHARS)
    rule_checker_master  = fields.Boolean("Apply Maker & Checker Rule for Master Forms",\
                     config_parameter=RULE_CHECKER_MASTER, default=True)
    rule_checker_transaction = fields.Boolean("Apply Maker & Checker Rule for Transaction Forms",\
                     config_parameter=RULE_CHECKER_TRANSACTION, default=True)
    seq_num_reset = fields.Selection(selection=YEARS, string="Sequence Number Reset",\
                     config_parameter=SEQ_NUM_RESET, default='fiscal_year')
    del_self_draft_entry = fields.Boolean("Allow to delete draft entries by all",\
                     config_parameter=DEL_SELF_DRAFT_ENTRY, default=True)
    min_char_length = fields.Integer("Enter the allowable minimum characters",\
                     config_parameter=MIN_CHAR_LENGTH, default=15)
                    
    master_search_installed_ids = fields.Many2many('ir.module.module',
        string='Applicable Modules',
        domain="[('state', '=', 'installed'),('category_id.name', '=','custom_modules')]")

    def set_values(self):
       res = super(ResConfigSettings, self).set_values()
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(SERVER_SIDE_VALIDATION, self.server_side_validation)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(DEL_SELF_DRAFT_ENTRY, self.del_self_draft_entry)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(SKIP_CHARS, self.skip_chars)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(RULE_CHECKER_MASTER, self.rule_checker_master)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(RULE_CHECKER_TRANSACTION,\
                                                           self.rule_checker_transaction)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(SEQ_NUM_RESET,\
                                                           self.seq_num_reset)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(MIN_CHAR_LENGTH,\
                                                           self.min_char_length)
       self.env[IR_CONFIG_PARAMETER].sudo().set_param(
            'custom_properties.master_search_installed_ids',
            self.master_search_installed_ids.ids)
                                                
       return res

    @api.model
    def get_values(self):
       res = super(ResConfigSettings, self).get_values()
       icp_sudo = self.env[IR_CONFIG_PARAMETER].sudo()
       res.update(
           server_side_validation=icp_sudo.get_param(SERVER_SIDE_VALIDATION),
           del_self_draft_entry=icp_sudo.get_param(DEL_SELF_DRAFT_ENTRY),
           skip_chars=icp_sudo.get_param(SKIP_CHARS),
           rule_checker_master=icp_sudo.get_param(RULE_CHECKER_MASTER),
           rule_checker_transaction=icp_sudo.get_param(RULE_CHECKER_TRANSACTION),
           seq_num_reset=icp_sudo.get_param(SEQ_NUM_RESET),
           min_char_length=icp_sudo.get_param(MIN_CHAR_LENGTH),
           
       )
       master_search_installed_ids = self.env[
            IR_CONFIG_PARAMETER].sudo().get_param(
            'custom_properties.master_search_installed_ids')
       if master_search_installed_ids:
            res.update({
                'master_search_installed_ids': [
                    (6, 0, literal_eval(master_search_installed_ids))]
            })
       return res