import time
import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CmProfileMasterBankDetails(models.Model):
    _name = 'cm.profile.master.bank.details.line'
    _description = 'Bank Details'

    header_id = fields.Many2one('cm.profile.master', string='Master Head Reference',
                                index=True, required=True, ondelete='cascade')
    account_no = fields.Char(string="Account No", copy=False, tracking=True, size = 20)
    acc_holder_name = fields.Char(string='Account Holder Name', help="Account holder name, in case it is different than the name of the Account Holder", readonly=False)
    bank_name = fields.Char(string='Bank Name')
    ifsc_code = fields.Char(string='IFSC Code',size=11)
    branch_name = fields.Char(string='Branch Name',size=250)
    
    @api.constrains('account_no')
    def _check_account_no(self):
        if self.account_no:
            if not ((len(str(self.account_no)) >= 8 and len(str(self.account_no)) <= 20) and self.account_no.isdigit() == True):
                raise UserError(
                    _('Invalid account number. Please enter the correct bank account number in bank details tab, Ref : %s')% self.account_no)
                    
            self.env.cr.execute(""" select account_no
            from cm_profile_master_bank_details_line where account_no='%s'""" %(self.account_no))
            acc_data = self.env.cr.dictfetchall()
            if len(acc_data) > 1:
                raise UserError(_('Duplicate account no is not allowed in bank details tab, Ref : %s')% self.account_no)

    @api.constrains('bank_name')
    def _check_bank_name(self):
        if self.bank_name:
            pattern = r"^[A-Za-z]+$"
            if not (re.match(pattern, self.bank_name)):
                raise UserError(
                    _('Invalid bank name. Bank name should only contain alphabets in bank details tab, Ref : %s')% self.bank_name)

    @api.constrains('branch_name')
    def _check_branch_name(self):
        if self.branch_name:
            pattern = r"^[A-Za-z]+$"
            if not (re.match(pattern, self.branch_name)):
                raise UserError(
                    _('Invalid branch name. Branch name should only contain alphabets in bank details tab, Ref : %s')% self.branch_name)
                    

    
    


