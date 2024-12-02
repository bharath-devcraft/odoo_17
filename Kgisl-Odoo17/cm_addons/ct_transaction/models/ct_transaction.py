from odoo import models, fields, api
from odoo.addons.custom_properties.decorators import validation
from dateutil.relativedelta import relativedelta
import time
from datetime import datetime
import logging
from odoo.exceptions import UserError, ValidationError, AccessError, MissingError, AccessDenied, RedirectWarning

_logger = logging.getLogger(__name__)

CT_TRANSACTION = 'ct.transaction'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
    ('draft', "Draft"),
    ('wfa', "WFA"),
    ('approved', "Approved"),
    ('rejected', "Rejected"),
    ('cancelled', "Cancelled")]

PAY_MODE = [('bank','Bank'),
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('neft_rtgs', 'NEFT/RTGS'),
            ('others','Others')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CtTransaction(models.Model):
    _name = 'ct.transaction'
    _description = 'Base Custom Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    
    def _get_dynamic_domain(self):
        """ Dynamic domain """
        if self.env['res.company'].search_count([]) > 0:
            return [('active','=',True)]
        else:
            return []

    name = fields.Char(string='Order No', readonly=True, index=True, copy=False, size=25)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True, copy=False, default='draft')

    entry_date = fields.Date(string="Order Date", copy=False, default=fields.Date.today)
    partner_id = fields.Many2one('res.partner', 
            string="Partner Name", index=True,
            ondelete='restrict', tracking=True,
            domain=lambda self: self._get_dynamic_domain())
    address = fields.Char(string="Address", size=252)
    ap_rej_remark = fields.Char(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Char(string="Cancel Remarks", copy=False)
    note = fields.Html(string="Note", copy=False)
    name_draft = fields.Char(string="Draft No", readonly=True, index=True, copy=False, size=25)
    draft_date = fields.Date(string="Draft Date", copy=False, default=fields.Date.today)
    line_count = fields.Integer(string='Line Count', default=0, compute='_compute_all_line', store=True, copy=False, readonly=True)
    division_id = fields.Many2one('cm.master', string="Division", tracking=True,
               ondelete='restrict', domain=[('status', 'in', ['active']),('active_trans', '=', True)]) # temporary
    department_id = fields.Many2one('cm.master', string="Department", tracking=True, 
               ondelete='restrict', domain=[('status', 'in', ['active']),('active_trans', '=', True)]) # temporary
    pay_mode = fields.Selection(selection=PAY_MODE, string="Mode of Payment", copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True,
                                 copy=False, tracking=True, ondelete='restrict',
                                 default=lambda self: self.env.company.currency_id.id) # temporary
    delivery_date = fields.Date(string="Delivery Date", copy=False, tracking=True)
    
    # Feedback
    rating = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'),
                               ('3', '3'), ('4', '4'), ('5', '5')], string='Rating')
    rating_feedback = fields.Text('Rating Feedback')

    ### Entry Info ###
    active = fields.Boolean(string="Visible", default=True)
    company_id = fields.Many2one('res.company', required=True, copy=False,
                      readonly=True, default=lambda self: self.env.company, ondelete='restrict')
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    active_rpt = fields.Boolean('Visible in Report', default=True)
    active_trans = fields.Boolean('Visible in Transactions', default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", default='manual', copy=False, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", readonly=True, copy=False,
                                ondelete='restrict', default=lambda self: self.env.user.id)
    crt_date = fields.Datetime(string="Creation Date", readonly=True, copy=False, default=fields.Datetime.now)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", readonly=True, 
                                  copy=False, ondelete='restrict')
    confirm_date = fields.Datetime(string="Confirmed Date", readonly=True, copy=False)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved/Reject By", readonly=True, 
                                 copy=False, ondelete='restrict')
    ap_rej_date = fields.Datetime(string="Approved/Reject Date", readonly=True, copy=False)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", readonly=True,
                                 copy=False, ondelete='restrict')
    cancel_date = fields.Datetime(string="Cancelled Date", readonly=True, copy=False)
    update_user_id = fields.Many2one(RES_USERS, string="Last Update By", readonly=True, copy=False,
                                ondelete='restrict')
    update_date = fields.Datetime(string="Last Update Date", readonly=True, copy=False)

    # This trigger_del is for while save record products tab vanished due to one2many trigger
    trigger_del = fields.Boolean(string="Trigger Delete", default=False)
    
    # Footer declaration
    tax_amt = fields.Float(
        string="Tax Amount(+)",
        store=True, compute='_compute_all_line')
    tot_amt = fields.Float(
        string="Total Amount",
        store=True, compute='_compute_all_line')
    other_amt = fields.Float(
        string="Other Charges(+)",
        store=True, compute='_compute_all_line')
    disc_amt = fields.Float(
        string="Discount Amount(-)",
        store=True, compute='_compute_all_line')
    taxable_amt = fields.Float(
        string="Taxable Amount",
        store=True, compute='_compute_all_line')
    round_off_amt = fields.Float(
        string="Round Off Amount(+/-)",
        store=True, compute='_compute_all_line')
    grand_tot_amt = fields.Float(
        string="Grand Amount",
        store=True, compute='_compute_all_line')
    fixed_disc_amt = fields.Float(
        string="Fixed Discount Amount(-)",
        store=True, compute='_compute_all_line')
    net_amt = fields.Float(
        string="Net Amount",
        store=True, compute='_compute_all_line')
    manual_round_off = fields.Boolean(string="Apply Manual Round Off", default=False)
        

    # Child table declaration
    line_ids = fields.One2many('ct.transaction.line', 'header_id', string='Transaction Lines', copy=True)
    line_ids_a = fields.One2many('ct.transaction.attachment.line', 'header_id', string='Transaction Attachment Line', copy=True)
    line_ids_b = fields.One2many('ct.transaction.expenses.line', 'header_id', string='Transaction Expenses Line', copy=True)
    line_ids_c = fields.One2many('ct.transaction.tax.line', 'header_id', string='Transaction Tax Line', copy=True)

    # Many2many table
    product_ids = fields.Many2many(
        'product.product',
        string='Product',
        ondelete='restrict')


    def handle_warnings(self, warning_msg, kw):
        """ Handle and format warning messages """
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(formatted_messages)
            else:
                return [formatted_messages]
        else:
            return False


    def validate_approve_action(self, warning_msg):
        """ Validate specific conditions for approve action """
        res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.rule_checker_transaction')
        is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
        if res_config_rule and self.confirm_user_id == self.env.user and not(is_mgmt):
            warning_msg.append("Confirmed user is not allow to approve the entry")


    def validate_expense_lines(self, warning_msg):
        """ Validate expense lines """
        if self.line_ids_b:
            for exp_line in self.line_ids_b:
                if exp_line.amt <= 0:
                    warning_msg.append("Expense(%s) amount should be greater than zero" % (exp_line.expense_id.name))
                if exp_line.disc_per < 0:
                    warning_msg.append("Expense(%s) discount should be greater than or equal to zero" % (exp_line.expense_id.name))
                if exp_line.disc_per > 100:
                    warning_msg.append("Expense(%s) discount should not be greater than hundred percent" % (exp_line.expense_id.name))


    def validate_serial_lines(self, detail_line, warning_msg):
        """ Validate serial lines for a detail line """
        dub_serial = []
        serial_qty = 0
        for serial_line in detail_line.line_ids:
            serial_qty += serial_line.qty
            if serial_line.qty <= 0:
                warning_msg.append("Product(%s) quantity should be greater than zero in serial no tab %s" % (detail_line.description, serial_line.serial_no))
            if serial_line.serial_no in dub_serial:
                warning_msg.append("%s duplicate serial no not allowed for product(%s)" % (serial_line.serial_no, detail_line.description))
            if serial_line.expiry_date < fields.Date.today():
                warning_msg.append("Product(%s) expiry date should not be less than current date for serial no %s" % (detail_line.description, serial_line.serial_no))
            dub_serial.append(serial_line.serial_no)
        if detail_line.line_ids and serial_qty != detail_line.qty:
            warning_msg.append("Product(%s) sum of serial no quantity should be equal to product quantity" % (detail_line.description))


    def validate_detail_line(self, detail_line, warning_msg):
        """ Validate individual detail line """
        if detail_line.qty <= 0:
            warning_msg.append("Product(%s) quantity should be greater than zero" % (detail_line.description))
        if detail_line.unit_price <= 0:
            warning_msg.append("Product(%s) unit price should be greater than zero" % (detail_line.description))
        if detail_line.disc_per < 0:
            warning_msg.append("Product(%s) discount should be greater than or equal to zero" % (detail_line.description))
        if detail_line.disc_per > 100:
            warning_msg.append("Product(%s) discount should not be greater than hundred percent" % (detail_line.description))
        
        self.validate_serial_lines(detail_line, warning_msg)


    def validate_line_items(self, warning_msg):
        """ Validate line items """
        if not self.line_ids:
            warning_msg.append('System not allow to confirm/approve with empty line details')
        else:
            for detail_line in self.line_ids:
                self.validate_detail_line(detail_line, warning_msg)


    def validate_action(self, kw, warning_msg):
        """ Validate action-related fields """
        action = kw.get('action')
        if action == 'reject':
            if not self.ap_rej_remark or not self.ap_rej_remark.strip():
                warning_msg.append("Reject remark is must. Kindly enter the remarks in Approve / Reject Remarks field")
            if self.ap_rej_remark and len(self.ap_rej_remark.strip()) < 10:
                warning_msg.append("Minimum 10 characters are must for Approve / Reject Remarks")
        elif action == 'cancel':
            if not self.cancel_remark or not self.cancel_remark.strip():
                warning_msg.append("Cancel remark is must. Kindly enter the remarks in Cancel Remarks field")
            if self.cancel_remark and len(self.cancel_remark.strip()) < 10:
                warning_msg.append("Minimum 10 characters are must for cancel remarks")


    def validations(self, **kw):
        """ Validations """
        warning_msg = []

        # Check if action-related validations are needed
        self.validate_action(kw, warning_msg)

        # Validate line items if status is 'draft' or 'wfa'
        if self.status in ('draft', 'wfa'):
            self.validate_line_items(warning_msg)
            self.validate_expense_lines(warning_msg)

        # Approve action validation
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        # Handle warning messages
        return self.handle_warnings(warning_msg, kw)


    ## Sequence no validation##
    def sequence_no_validations(self, **kw):
        """ Sequence no validations """
        warning_msg = []
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

        # Handle warning messages
        return self.handle_warnings(warning_msg, kw)


    def _process_tax_line(self, line, product, tax_line, price_unit, qty, discount, price_subtotal, type_tax_use_dict):
        """ Process individual tax line core functionality"""

        tax_value_return = self.env['account.tax']._convert_to_tax_base_line_dict(
                                            self,
                                            partner=line.header_id.partner_id,
                                            currency=line.header_id.currency_id,
                                            product=product,
                                            taxes=tax_line,
                                            price_unit=price_unit,
                                            quantity=qty,
                                            discount=discount,
                                            price_subtotal=price_subtotal,
                                        )
        tax_results = self.env['account.tax']._compute_taxes([tax_value_return])
        totals = next(iter(tax_results['totals'].values()))
        amount_tax = totals['amount_tax']

        type_tax_use_dict[tax_line.tax_group_id.name] += amount_tax

    def _process_line_items(self, line_items, tax_dict):
        """ Detail tax line """
        for line in line_items:
            if line.unit_price > 0:
                for tax_line in line.taxes_id:
                    self._process_tax_line(line, line.product_id, tax_line, line.unit_price, line.qty, line.disc_per, line.tot_amt, tax_dict)

    def _process_line_items_b(self, line_items_b, tax_dict):
        """ Expense tax line """
        for line in line_items_b:
            if line.amt > 0:
                for tax_line in line.taxes_id:
                    self._process_tax_line(line, None, tax_line, line.amt, 1, line.disc_per, line.line_tot_amt, tax_dict)


    def _initialize_tax_dict(self):
        """ Initialize the tax dictionary with tax group names """
        return {
            record['name']: 0
            for record in self.env['account.tax.group'].read_group([], ['name'], ['name'])
        }

    def _compute_footer_calculation(self):
        """ Compute footer calculations """
        for data in self:
            data.tot_amt = sum(data.line_ids.mapped('tot_amt'))
            data.other_amt = sum(data.line_ids_b.mapped('line_tot_amt'))
            data.disc_amt = sum(data.line_ids.mapped('disc_amt')) + sum(data.line_ids_b.mapped('disc_amt'))
            data.taxable_amt = (data.tot_amt + data.other_amt) - data.disc_amt
            data.tax_amt = sum(data.line_ids.mapped('tax_amt')) + sum(data.line_ids_b.mapped('tax_amt'))

            #Line delete remove the value of round off
            data.round_off_amt, data.fixed_disc_amt, data.manual_round_off = (
                (data.round_off_amt, data.fixed_disc_amt, data.manual_round_off) 
                if data.tot_amt 
                else (0.00, 0.00, False)
            )            
            
            # Auto round off
            if not data.manual_round_off:
                data.round_off_amt = round(data.taxable_amt + data.tax_amt) - (data.taxable_amt + data.tax_amt)
                data.round_off_amt = round(data.round_off_amt, 2)

            data.grand_tot_amt = data.taxable_amt + data.tax_amt + data.round_off_amt
            data.net_amt = data.grand_tot_amt - data.fixed_disc_amt
    
    
    ### Total, Tax amount, Discount amt Calculation ###
    @api.depends('line_ids', 'line_ids_b', 'round_off_amt', 'fixed_disc_amt', 'manual_round_off')
    def _compute_all_line(self):
        """ _compute_all_line """
        for data in self:
            #Line counts
            data.line_count = len(data.line_ids)
            
            # Footer calculations
            data._compute_footer_calculation()
            
            ### Tax breakup update based on taxes ###
            
            # Initialize tax breakdown
            type_tax_use_dict = data._initialize_tax_dict()

            # Process detail line items
            data._process_line_items(data.line_ids, type_tax_use_dict)
            
            # Process other charges line items
            data._process_line_items_b(data.line_ids_b, type_tax_use_dict)

            # Unlink tax breakup values
            data.line_ids_c = [(5, 0, 0)]

            # Tax breakup creation
            tax_values = []
            for tx_name, tx_amt in type_tax_use_dict.items():
                if tx_amt > 0:
                    tax_values.append((0,0,{'tax_name':tx_name,'tax_amt':tx_amt}))
            data.line_ids_c = tax_values

    @api.constrains('draft_date')
    def draft_date_validation(self):
        """ draft_date_validation """
        return True

    @api.onchange('partner_id')
    def onchange_supplier(self):
        """ supplier onchange address load """
        if self.partner_id:
            self.address = self.partner_id.street # temporary

    @api.onchange('delivery_date')
    def onchange_delivery(self):
        """ delivery onchange validation """
        if self.delivery_date and self.entry_date and self.delivery_date < self.entry_date:
            raise UserError("Delivery date should be greater than or equal to order date")

    def common_warning_rule(self):
        """Warning Messages"""
        
        warning_msgs = []
        if not self.note:
            warning_msgs.append("Would you like to continue without notes ?")

        if not self.line_ids_a:
            warning_msgs.append("Kindly check & add attachments, If required.")

        if warning_msgs:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view.id if view else False
            context = {
                'message': "\n\n".join(warning_msgs),
                'transaction_id': self.id,
                'transaction_model': CT_TRANSACTION,
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

    def save_record(self):
        """ save_record """
        
        self.trigger_del = True
        
        for line in self.line_ids:
            line.unlink()

        self.trigger_del = False
        if self.product_ids:
            for line in self.product_ids:
                self.line_ids = [(0,0,{
                                        'product_id': line.id,
                                        'description': line.name,
                                    })]

        return True

    @validation
    def entry_confirm(self):
        """ entry_confirm """
        if self.status == 'draft':
            self.validations()

            if not self.name_draft:
                sequence_id = self.env['ir.sequence'].search(
                        [('code', '=', 'ct.transaction.draft')], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno('%s','%s','%s',%s,%s,'%s') """ %
                        (sequence_id.id,
                         sequence_id.code,
                         self.draft_date,
                         self.company_id.id,
                         self.division_id.id,
                         'division'))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=self.draft_date)

                self.name_draft = sequence

            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

            # Entry confirm mail action
            self.transaction_mail_data_design(
                                            trans_rec = self, entry_action = 'entry_confirm' ,
                                            mail_name = 'Entry Confirm Mail',
                                            subject = '#Transaction %s confirmed' %(self.name_draft),
                                            mail_config_name = 'Transaction Confirm Mail'
                                        )
            
            # Entry confirm sms action
            self.transaction_sms_design(
                                        message_type = 'sms',
                                        trans_rec = self,
                                        sms_name = 'Entry Confirm SMS',
                                        content_text = '#SMS:Transaction %s confirmed' %(self.name_draft),
                                    )
            
            # Entry confirm whatsapp message
            self.transaction_sms_design(
                                        message_type = 'whatsapp',
                                        trans_rec = self,
                                        sms_name = 'Entry Confirm WhatsApp',
                                        content_text = '#WhatsApp:Transaction %s confirmed' %(self.name_draft)
                                    )

        return True

    @validation
    def entry_approve(self):
        """ entry_approve """
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env['ir.sequence'].search(
                        [('code', '=', CT_TRANSACTION)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno('%s','%s','%s',%s,%s,'%s') """ %
                        (sequence_id.id,
                         sequence_id.code,
                         self.entry_date,
                         self.company_id.id,
                         self.division_id.id,
                         'division'))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=self.entry_date)

                self.name = sequence
            
            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

            # Entry approve mail action
            self.transaction_mail_data_design(
                                            trans_rec = self, entry_action = 'entry_approve' ,
                                            mail_name = 'Entry Approve Mail',
                                            subject = '#Transaction %s Approved' %(self.name),
                                            mail_config_name = 'Transaction Approve Mail'
                                        )

        return True
    
    def entry_reject(self):
        """ entry_reject """
        if self.status == 'wfa':
            self.validations(action="reject")
            self.write({'status': 'rejected',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def entry_cancel(self, **kw):
        """ entry_cancel """
        if self.status == 'approved':
            if not kw.get('mode_of_call'):
                self.validations(action="cancel")
            self.write({'status': 'cancelled',
                        'cancel_user_id': self.env.user.id,
                        'cancel_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def entry_feedback(self):
        """ entry_feedback """

        local_context = dict(
            self.env.context,
            default_trans_id=self.id,
        )

        return {
                'type': 'ir.actions.act_window',
                'name': 'Your feedback is more valuable for us !!',
                'res_model': 'ct.transaction.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': local_context,
            }
    
    
    def unlink(self):
        """ Unlink Function """
        for rec in self:
            if rec.status not in ('draft') or rec.entry_mode == 'auto':
                raise UserError("You can't delete other than manually created draft entries")
            if rec.status in ('draft'):
                res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.del_draft_entry')
                is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
                if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
                    raise UserError("You can't delete other users draft entries")
                models.Model.unlink(rec)
        return True

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CtTransaction, self).write(vals)

    # Server Action Domain
    def get_trans_id(self):
        """ Return created user and logged in user same ids to Server Domain"""
        return [rec.id for rec in self.env[CT_TRANSACTION].search([]) if rec.user_id.id == self.env.user.id]


    def  get_entry_mail_ids(self, **kw):
        """Arriving mail to,cc and bcc : trans_id key and value is must"""
        mail_ids = {}
        trans_rec = self.env[CT_TRANSACTION].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.user_id.email]

        return mail_ids
    
    def transaction_mail_data_design(self, **kw):
        """Transaction Mail Design : trans_rec,entry_action,mail_name,subject key and value is must """

        self.env.cr.execute(
            """select custom_transaction_mails(%s,'%s','%s','%s')""" %
            (self.id,self.status,self.name or self.name_draft, self.env.user.partner_id.name,))
        data = self.env.cr.fetchall()

        trans_rec = kw.get('trans_rec', self)
        mail_name = kw.get('mail_name', '')
        mail_config_name = kw.get('mail_config_name', '')
        mail_type = kw.get('mail_type', 'transaction')

        #### Subject ###
        subject = kw.get('subject', '')

        if trans_rec and data[0][0] and mail_name and subject and mail_config_name:

            ### Common mail arriving function ###
            mail_ids = self.get_entry_mail_ids(trans_id=trans_rec.id)
            default_to = mail_ids.get('email_to',[])
            
            ### Mail Configuration ###
            vals = self.env['cp.mail.configuration'].mail_config_mailids_data(mail_type=mail_type,model_name=CT_TRANSACTION,mail_name=mail_config_name)

            email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
            email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
            email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
            email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''

            if trans_rec.line_ids_a:
                attachment = trans_rec.line_ids_a.mapped('attachment')
            else:
                attachment = False

            self.env['cp.mail.queue'].create_mail_queue(
                name = mail_name, trans_rec = trans_rec, mail_from = email_from,
                email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                subject = subject, body = data[0][0], attachment=attachment)

        return True

    def transaction_sms_design(self, **kw):
        """Transaction SMS Design : trans_rec,sms_name,message_type,content_text key and value is must """

        trans_rec = kw.get('trans_rec', self)
        sms_name = kw.get('sms_name', '')
        content_text = kw.get('content_text', '')
        message_type = kw.get('message_type', '')

        if trans_rec and sms_name and content_text and message_type:
            default_mobile = ['9876543210']
            
            ### Mail Configuration ###
            vals = self.env['cp.sms.configuration'].sms_config_data(message_type=message_type, action_name=sms_name)
            mobile_no = ", ".join(set(default_mobile + vals.get('mobile_no', []))) if default_mobile or vals.get('mobile_no') else ''

            self.env['cp.sms.queue'].create_sms_queue(
                message_type = message_type, trans_rec = trans_rec,
                sms_name = sms_name, mobile_no = mobile_no, content_text = content_text)

        return True

    def _get_order_lines_to_report(self) -> None:
        return self.line_ids
    
    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the transaction views.
        """

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
            'my_today_value': 0,
            'today_highest_tot':0,
            'ref_no':'',
            'company_currency_symbol': self.env.company.currency_id.symbol
        }
        
        
        #counts
        ct_trans = self.env[CT_TRANSACTION]
        result['all_draft'] = ct_trans.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_trans.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_trans.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_trans.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_trans.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_trans.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_trans.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_trans.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_trans.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_trans.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_trans.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_today_value'] = self.human_readable_format(sum(ct_trans.search([('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_today_value'] = self.human_readable_format(sum(ct_trans.search([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        max_transaction = max(ct_trans.search([('crt_date', '>=', fields.Date.today()), ('status', '=', 'approved')]), 
                      key=lambda t: t.net_amt, default=None)
        result['today_highest_tot'] = self.human_readable_format(max_transaction.net_amt) if max_transaction else 0
        result['ref_no'] = max_transaction.name if max_transaction else '-'

        return result

    def human_readable_format(self, value, format='%.1f'):
        """
        Convert a large integer to a friendly text representation.
        123456789 -> 123.5 M
        """
        powers = [10**15, 10**12, 10**9, 10**6, 10**3]
        human_powers = ['Qa','T', 'B', 'M', 'K']

        for power, human_power in zip(powers, human_powers):
            if value >= power:
                return format % (float(value) / power) + ' ' + human_power
            else:
                value = round(value,2)
        return str(value)

    def action_transaction_history(self):
        """ Open server action view for history purpose.
            Based on future needs it will change.
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("ct_transaction.ct_transaction_serv_action")

        return action

class CtTransactionWizard(models.TransientModel):
    """ Transaction Wizard """
    _name = "ct.transaction.wizard"
    _description = "Transaction Wizard"
    rating = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'),
                               ('3', '3'), ('4', '4'), ('5', '5')], string='Rating')
    rating_feedback = fields.Text('Rating Feedback')
    trans_id = fields.Many2one(CT_TRANSACTION, string='Transaction')

    def wizard_submit_button(self):
        """ Feedback Wizard """
        active_ids = self._context.get('active_ids')
        transactions = self.env[CT_TRANSACTION].search([('id', 'in', active_ids)])

        # Check for unapproved transactions
        unapproved_transactions = transactions.filtered(lambda t: t.status != 'approved')
        if unapproved_transactions:
            raise UserError('Kindly choose approved status entries alone to process further')

        # Process approved transactions
        for transaction in transactions.filtered(lambda t: t.status == 'approved'):
            transaction.rating = self.rating
            transaction.rating_feedback = self.rating_feedback
            if int(self.rating) <= 3:
                self._validate_feedback()

    def _validate_feedback(self):
        """Validate the feedback for low ratings."""
        if not self.rating_feedback:
            raise UserError('Rating feedback is a must')
        if len(self.rating_feedback) < 15:
            raise UserError('Minimum 15 characters are required for rating feedback')