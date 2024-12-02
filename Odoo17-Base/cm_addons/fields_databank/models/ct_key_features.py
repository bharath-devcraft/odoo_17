# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CT_KEY_FEATURES = 'ct.key.features'
RES_USERS = 'res.users'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

RATING_OPTIONS = [('0','0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]

class CtKeyFeatures(models.Model):
    _name = 'ct.key.features'
    _description = 'Transaction Key Features'

    def _get_dynamic_domain(self):
        if self.env['res.company'].search_count([]) > 0:
            return [('active','=',True)]
        else:
            return []

    name = fields.Char(string="Name", index=True, copy=False, size=30, c_rule=True)
    rating = fields.Selection(selection=RATING_OPTIONS, string="Rating", copy=False)
    rating_feedback = fields.Text(string="Rating Feedback", copy=False)
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    active = fields.Boolean(string="Visible", default=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.constrains('draft_date')
    def draft_date_validation(self):
        return True
    
    def common_warning_rule(self):
        warning_msgs = []
        if not self.note:
            warning_msgs.append("Would you like to continue without notes ?")

        if warning_msgs:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view.id if view else False
            context = {
                'message': "\n\n".join(warning_msgs),
                'transaction_id': self.id,
                'transaction_model': CT_KEY_FEATURES,
                'transaction_stage': self.status
            }
            return {
                'name': 'Warning',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sh.message.wizard',
                'views': [(view_id, 'form')],
                'view_id': view_id,
                'target': 'new',
                'context': context,
            }

        if self.status == 'wfa':
            self.entry_approve()
        
        return True

    def entry_confirm(self):
        self.write({'status': 'wfa',
                    'confirm_user_id': self.env.user.id,
                    'confirm_date': time.strftime(TIME_FORMAT)
                    })
        return True
    
    def entry_approve(self):
        self.write({'status': 'approved',
                    'ap_rej_user_id': self.env.user.id,
                    'ap_rej_date': time.strftime(TIME_FORMAT)
                    })
        return True


    def entry_feedback(self):
        local_context = dict(
            self.env.context,
            default_trans_id=self.id,
        )
        return {
                'type': 'ir.actions.act_window',
                'name': "Your feedback is more valuable for us !!",
                'res_model': 'ct.key.features.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': local_context,
            }
    
    def server_action_dynamic_domain(self):
        return [rec.id for rec in self.env[CT_KEY_FEATURES].search([]) if rec.user_id.id == self.env.user.id]
    
    def action_transaction_history(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('fields_databank.ct_key_features_serv_action')

        return action
    
    def write(self, vals):
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CtKeyFeatures, self).write(vals)

class CtKeyFeaturesWizard(models.TransientModel):
    _name = "ct.key.features.wizard"
    _description = "Transaction Key Features Wizard"
    rating = fields.Selection(selection=RATING_OPTIONS, string="Rating", copy=False)
    rating_feedback = fields.Text(string="Rating Feedback", copy=False)

    def wizard_submit_button(self):
        active_ids = self._context.get('active_ids')
        transactions = self.env[CT_KEY_FEATURES].search([('id', 'in', active_ids)])

        unapproved_transactions = transactions.filtered(lambda t: t.status != 'approved')
        if unapproved_transactions:
            raise UserError(_("Kindly choose approved status entries alone to process further"))

        for transaction in transactions.filtered(lambda t: t.status == 'approved'):
            transaction.rating = self.rating
            transaction.rating_feedback = self.rating_feedback
            if int(self.rating) <= 3:
                self._validate_feedback()

    def _validate_feedback(self):
        if not self.rating_feedback:
            raise UserError(_("Rating feedback is a must"))
        min_char = self.env['ir.config_parameter'].sudo().get_param('custom_properties.min_char_length')
        if len(self.rating_feedback.strip()) < int(min_char):
            raise UserError(_(f"Minimum {min_char} characters are required for rating feedback"))