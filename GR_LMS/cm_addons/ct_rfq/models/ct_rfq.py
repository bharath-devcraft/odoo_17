# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_RFQ = 'ct.rfq'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

RFQ =  [('pi','PI'),
        ('si', 'SI')]

class CtRfq(models.Model):
    _name = 'ct.rfq'
    _description = 'RFQ'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="RFQ No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="RFQ Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    due_date = fields.Date(string="Validity Date", copy=False, tracking=True)
    rfq_name = fields.Char(string="RFQ Name",c_rule=True)
    
    rfq_mode = fields.Selection(selection=RFQ, string="RFQ Mode", copy=False, default="pi", readonly=True, store=True, tracking=True)
    pi_line_ids = fields.Many2many('ct.purchase.request.line', string="Purchase Request Line ", ondelete='restrict', c_rule=True)
    supplier_ids = fields.Many2many('cm.vendor.master', string="Vendor ", ondelete='restrict', c_rule=True)

    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", copy=False, ondelete='restrict', readonly=True)
    cancel_date = fields.Datetime(string="Cancelled Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    trigger_del = fields.Boolean(string="Trigger Delete", default=False)

    line_ids = fields.One2many('ct.rfq.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.rfq.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    def display_warnings(self, warning_msg, kw):
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(_(formatted_messages))
            else:
                return [formatted_messages]
        else:
            return False


    def validate_approve_action(self, warning_msg):
        is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_transaction')
            if res_config_rule and self.confirm_user_id == self.env.user:
                warning_msg.append("Confirmed user is not allow to approve the entry")

    def validate_line_items(self, warning_msg):
        if not self.line_ids:
            warning_msg.append("System not allow to confirm/approve with empty line details")
        else:
            dub_product = set()
            dub_serial = []
            for detail_line in self.line_ids:
                if detail_line.qty <= 0:
                    warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero")
                combination = (
                    detail_line.product_id.id, 
                    detail_line.uom_id.id 
                )
                if combination in dub_product:
                    warning_msg.append(f"Duplicate product are not allowed. Ref : {detail_line.description}")
                else:
                    dub_product.add(combination)


    def validations(self, **kw):
        warning_msg = []
        if self.status in ('draft', 'wfa'):
            self.validate_line_items(warning_msg)
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': 'ct.rfq.draft',
            'approve': CT_RFQ
        }

        action = kw.get('action')
        if action in action_code_map:
            sequence_code = action_code_map[action]
            sequence_id = self.env[IR_SEQUENCE].search([('code', '=', sequence_code)], limit=1)
            if not sequence_id:
                warning_msg.append("The ir sequence has not been created.")
        if kw.get('date'):
            self.env.cr.execute(
                """select value from ir_config_parameter 
                where key = 'custom_properties.seq_num_reset' 
                order by id desc limit 1;
            """)
            seq_reset = self.env.cr.fetchone()
            if not seq_reset or not seq_reset[0]:
                warning_msg.append("The sequence number reset option has not been configured in the custom settings.")
            elif seq_reset[0] == 'fiscal_year':
                fiscal_year = self.env['cm.fiscal.year'].search([
                                ('from_date', '<=', kw.get('date')),('to_date', '>=', kw.get('date')),
                                ('status', '=', 'active'),('active', '=', True)])
                if not fiscal_year:
                    warning_msg.append("The fiscal year has not been created.")

        return self.display_warnings(warning_msg, kw)
    
    @api.depends('line_ids')
    def _compute_all_line(self):
        for data in self:
            data.line_count = len(data.line_ids)

    @api.onchange('due_date')
    def onchange_due(self):
        if self.due_date and self.entry_date and self.due_date < self.entry_date:
            raise UserError(_("Due date should be greater than or equal to entry date"))
    
    
    def save_record(self):
        self.trigger_del = True
        self.line_ids.unlink()  # Unlink all existing lines
        self.trigger_del = False
        if len(self.supplier_ids) < 1:
            raise UserError(_("You must select exactly 1 suppliers."))
		
        if not self.pi_line_ids:
            return True

        for line in self.pi_line_ids:          
            
            rfq_line = self.env['ct.rfq.line'].create({
                'header_id': self.id,
                'pr_line_id': line.id,
                'product_id': line.product_id.id,
                'brand_id': line.brand_id.id,
                'description': line.description,
                'uom_id': line.uom_id.id if line.uom_id else '',
                'qty': line.pending_qty,
                'request_qty': line.qty,
                })
            
            

            for vendor in self.supplier_ids:                
                # Build the address parts with default values
                street = vendor.street or ''
                street1 = vendor.street1 or ''
                city_name = vendor.city_id.name or ''
                state = vendor.state_id.name or ''
                zip_code = vendor.pin_code or ''
                country = vendor.country_id.name or ''

                # Concatenate the address parts
                part_address = f"{street} {street1} {city_name}\n{state} {zip_code}\n{country}"

                # Create the RFQ partner record
                self.env['ct.rfq.partner'].create({
                    'header_id': rfq_line.id,
                    'partner_id': vendor.id,
                    'part_address': part_address,
                    'email': vendor.email,
                    'description': vendor.name,
                    'flag_mail': True,
                })

        return True
    
    def load_vendors(self):        
        if self.supplier_ids and self.line_ids:
            for line in self.line_ids:
                list_part = []
                for vendor in self.supplier_ids:                
					# Build the address parts with default values
                    street = vendor.street or ''
                    street1 = vendor.street1 or ''
                    city_name = vendor.city_id.name or ''
                    state = vendor.state_id.name or ''
                    zip_code = vendor.pin_code or ''
                    country = vendor.country_id.name or ''

                    # Concatenate the address parts
                    part_address = f"{street} {street1} {city_name}\n{state} {zip_code}\n{country}"
                    vals = (0,0,{'header_id':line.id,                                     
                                 'partner_id': vendor.id,
                                 'part_address': part_address,
                                 'email': vendor.email,
                                 'description': vendor.name,
                                 'flag_mail': True,
                                 })
                    list_part.append(vals)
    
    def generate_quotation(self):        
        for vendor in self.supplier_ids:            
            sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', 'ct.quotation.submit')], limit=1)
            if sequence_id:
                self.env.cr.execute(
                    """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
                    (sequence_id.id,
                     sequence_id.code,
                     self.entry_date,
                     None,
                     None,
                     ''))
                sequence = self.env.cr.fetchone()
                sequence = sequence[0]
            else:
                sequence = ''

            # Concatenate the address parts
            part_address = f"{vendor.street or ''} {vendor.street1 or ''} {vendor.city_id.name or ''}\n{vendor.state_id.name or ''} {vendor.pin_code or ''}\n{vendor.country_id.name or ''}"
            submission_line = []
            quotation_id = self.env['ct.quotation.submit'].create({
                'vendor_id': vendor.id,
                'currency_id': self.currency_id.id, 
                'vendor_name':  vendor.name,
                'vendor_address':  part_address,
                'rfq_name': self.rfq_name,
                'name': sequence,
                'due_date': self.due_date,
                'rfq_id': self.id,
                'rfq_mode':self.rfq_mode,
                'entry_mode': 'auto',
                'status':'draft',
                'department_id': self.department_id.id, 
            })
            for line in self.line_ids:
                vals = (0,0,{
                        'header_id': quotation_id.id,
                        'product_id': line.product_id.id,
                        'brand_id': line.brand_id.id,
                        'brand_desc': line.brand_id.name,
                        'description': line.description,
                        'uom_id': line.uom_id.id,
                        'qty': line.qty,
                    })
                submission_line.append(vals)
            quotation_id.line_ids = submission_line   

        return True
    
    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()           

            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_RFQ)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
                        (sequence_id.id,
                         sequence_id.code,
                         self.entry_date,
                         None,
                         None,
                         ''))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=self.entry_date, action='approve')

                self.name = sequence
                
            self.load_vendors()
            self.generate_quotation()
                
            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

        return True
    
    def entry_reject(self):
        if self.status == 'wfa':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.ap_rej_remark or not self.ap_rej_remark.strip():
                raise UserError(_("Reject remarks is must. Kindly enter the remarks in Approve / Reject Remarks field"))
            if self.ap_rej_remark and len(self.ap_rej_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for Approve / Reject Remarks"))
            self.write({'status': 'rejected',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def entry_cancel(self):
        if self.status == 'approved':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.cancel_remark or not self.cancel_remark.strip():
                raise UserError(_("Cancel remarks is must. Kindly enter the remarks in Cancel Remarks field"))
            if self.cancel_remark and len(self.cancel_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for cancel remarks"))
            self.write({'status': 'cancelled',
                        'cancel_user_id': self.env.user.id,
                        'cancel_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def unlink(self):
        for rec in self:
            if rec.status != 'draft' or rec.entry_mode == 'auto':
                raise UserError(_("You can't delete other than manually created draft entries"))
            if rec.status == 'draft':
                is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
                if not is_mgmt:
                    res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.del_self_draft_entry')
                    if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
                        raise UserError(_("You can't delete other users draft entries"))
                models.Model.unlink(rec)
        return True

    def write(self, vals):
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CtRfq, self).write(vals)

    @api.model
    def retrieve_dashboard(self):
        result = {
            'all_draft': 0,
            'all_wfa': 0,
            'all_approved': 0,
            'all_rejected': 0,
            'all_cancelled': 0,
            'my_draft': 0,
            'my_wfa': 0,
            'my_approved': 0,
            'my_rejected': 0,
            'my_cancelled': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0
        }

        ct_rfq_trans = self.env[CT_RFQ]
        result['all_draft'] = ct_rfq_trans.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_rfq_trans.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_rfq_trans.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_rfq_trans.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_rfq_trans.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_rfq_trans.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_rfq_trans.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_rfq_trans.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_rfq_trans.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_rfq_trans.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_rfq_trans.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_rfq_trans.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_rfq_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_rfq_trans.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
