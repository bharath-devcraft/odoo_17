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
DRAFT_WATERMARK = 'custom_properties.draft_watermark'
REJECT_WATERMARK = 'custom_properties.reject_watermark'
CANCEL_WATERMARK = 'custom_properties.cancel_watermark'


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

    draft_watermark = fields.Binary(
        string="Draft Watermark",
        help="Upload a watermark image for PDF reports in the draft stage."
    )

    draft_watermark_name = fields.Char(
        string="Draft Watermark Filename"
    )
    reject_watermark = fields.Binary(
        string="Rejected Watermark",
        help="Upload a watermark image for rejected stage."
    )
    reject_watermark_name = fields.Char(
        string="Rejected Watermark Filename"
    )
    cancel_watermark = fields.Binary(
        string="Cancelled Watermark",
        help="Upload a watermark image for cancelled stage."
    )
    cancel_watermark_name = fields.Char(
        string="Cancelled Watermark Filename"
    )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        settings = self.env['res.config.settings'].sudo().search([], limit=1)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(SERVER_SIDE_VALIDATION, self.server_side_validation)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(DEL_SELF_DRAFT_ENTRY, self.del_self_draft_entry)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(SKIP_CHARS, self.skip_chars)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(RULE_CHECKER_MASTER, self.rule_checker_master)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(RULE_CHECKER_TRANSACTION, \
                                                       self.rule_checker_transaction)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(SEQ_NUM_RESET, \
                                                       self.seq_num_reset)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(MIN_CHAR_LENGTH, \
                                                       self.min_char_length)
        self.env[IR_CONFIG_PARAMETER].sudo().set_param(
            'custom_properties.master_search_installed_ids',
            self.master_search_installed_ids.ids)
        settings = self.env['res.config.settings'].sudo().search([], limit=1)
        if settings:
            settings.write({
                'draft_watermark': self.draft_watermark,
                'draft_watermark_name': self.draft_watermark_name,
                'reject_watermark': self.reject_watermark,
                'reject_watermark_name': self.reject_watermark_name,
                'cancel_watermark': self.cancel_watermark,
                'cancel_watermark_name': self.cancel_watermark_name
            })
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
            draft_watermark=self.env['res.config.settings'].sudo().search([], limit=1).draft_watermark,
            reject_watermark=self.env['res.config.settings'].sudo().search([], limit=1).reject_watermark,
            cancel_watermark=self.env['res.config.settings'].sudo().search([], limit=1).cancel_watermark,

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
