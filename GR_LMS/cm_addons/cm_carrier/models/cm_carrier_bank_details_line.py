# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_alphabets,valid_account_no
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

CM_CITY = 'cm.city'

ACCOUNT_TYPE_OPTION = [('Current', 'Current'),('savings', 'Savings')] 

class CmCarrierBankDetailsLine(models.Model):
    _name = 'cm.carrier.bank.details.line'
    _description = 'Bank Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.carrier', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    bank_name = fields.Char(string="Bank Name", copy=False, size=252)
    branch_name = fields.Char(string="Branch Name", copy=False, size=252)
    branch_code = fields.Char(string="Branch Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    acc_holder_name = fields.Char(string="Account Holder Name", copy=False, size=252)
    account_type = fields.Selection(selection=ACCOUNT_TYPE_OPTION, string="Account Type", copy=False)    
    account_no = fields.Char(string="Account No", copy=False, size=20, tracking=True)
    ifsc_code = fields.Char(string="IFSC Code", copy=False, size=11)
    micr_no = fields.Integer(string="MICR Number", copy=False)
    swift_code = fields.Char(string="Swift Code", copy=False, size=252)
    iban_no = fields.Char(string="IBAN Number", copy=False, size=252)
        
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    @api.constrains('account_no')
    def account_no_validation(self):
        for line in self:
            if line.account_no:
                if not valid_account_no(line.account_no):
                    raise UserError(_(f"Invalid account number. Please enter the correct bank account number in the bank details tab, Ref: {line.account_no}"))

                duplicate_count = line.search_count([('account_no', '=', line.account_no),('company_id', '=', line.company_id.id)])
                if duplicate_count > 1:
                    raise UserError(_(f"Duplicate account number is not allowed in the bank details tab, Ref: {line.account_no}"))

    @api.constrains('bank_name')
    def bank_name_validation(self):
        for line in self:
            if line.bank_name and not is_alphabets(line.bank_name):
                raise UserError(_(f"Invalid bank name. Bank name should only contain alphabets in bank details tab, Ref : {line.bank_name}") )

    @api.constrains('branch_name')
    def branch_name_validation(self):
        for line in self:
            if line.branch_name and not is_alphabets(line.bank_name):
                raise UserError(_(f"Invalid branch name. Branch name should only contain alphabets in bank details tab, Ref : {line.branch_name}"))
                    

    
    


