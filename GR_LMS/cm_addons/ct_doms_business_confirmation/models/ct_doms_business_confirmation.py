# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from odoo.exceptions import UserError

CT_DOMS_BUSINESS_CONFIRMATION = 'ct.doms.business.confirmation' 
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'
CT_QUOTATIONS = 'ct.quotations'
CM_SERVICE = 'cm.service'
CM_PRODUCT = 'cm.product'
IR_ATTACHMENT = 'ir.attachment'
CM_DEPOT_LOCATION = 'cm.depot.location'
CM_PORT = 'cm.port'
CM_PORT_TERMINAL = 'cm.port.terminal'
CM_TRANSPORT_ROUTE = 'cm.transport.route'
CM_TANK_LEASE_TARIFF = 'cm.tank.lease.tariff'
CM_TRANSPORT_TARIFF = 'cm.transport.tariff'
RES_COUNTRY_STATE = 'res.country.state'
RES_CURRENCY = 'res.currency'
CM_TRANSPORT_LOCATION = 'cm.transport.location'
CM_CITY = 'cm.city'
CM_PORT_TERMINAL = 'cm.port.terminal'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

CUS_TANK_APPROVAL = [('required','Required'), ('not_required','Not Required')]

DG_PRODUCT = [('yes', 'DG'), ('no', 'Non DG')]

PACK_GRP = [('1', 'I'), ('2', 'II'), ('3', 'III')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

PERIOD_CHOICES = [('day', 'Day'), ('month', 'Month'), ('year', 'Year')]

TRAILER_TYPE = [('20_feet', '20 Feet'), ('40_feet', '40 Feet'), ('both', 'Both')]

MODE_OF_PAYMENT = [('cash', 'Cash'),
                    ('credit', 'Credit')]


ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CtDomsBusinessConfirmation(models.Model):
    _name = 'ct.doms.business.confirmation'
    _description = 'Business Conformation'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="BC No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="BC Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)

    po_no = fields.Char(string="Customer PO No", copy=False)
    po_date = fields.Date(string="Customer PO Date", copy=False)
    qs_no = fields.Many2one(CT_QUOTATIONS,string="Quotation No", ondelete='restrict', domain=[('status', '=', 'quotation_sent'),('active_trans', '=', True)], copy=False)
    qs_date = fields.Date(string="Quotation Date", copy=False)
    service_id = fields.Many2one(CM_SERVICE, string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    sales_person_id= fields.Many2one(RES_USERS, string="Sales Person", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ship_term_id = fields.Many2one('cm.shipment.term', string="Shipment Term", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    cus_tank_approval = fields.Selection(selection=CUS_TANK_APPROVAL, string="Customer Tank Approval", copy=False)

    customer_id = fields.Many2one('cm.customer', string="Customer Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    cus_bill_address = fields.Text(string="Billing Address", default=False)
    cus_del_address = fields.Text(string="Delivery Address", default=False)
    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)

    product_id = fields.Many2one(CM_PRODUCT, string="Product Name", copy=False, ondelete='restrict', domain=[('status', 'in', ('active','reject')),('active_trans', '=', True)])
    dg_product = fields.Selection(selection=DG_PRODUCT, string="Product Type" ,copy=False, c_rule=True)
    un_no = fields.Char(string="UN Number", copy=False)
    imo_class = fields.Char(string="IMO Class", size=10)
    pack_grp = fields.Selection(selection=PACK_GRP, string="Packing Group")
    sds_attach_ids = fields.Many2many(IR_ATTACHMENT, string="SDS Document", ondelete='restrict', check_company=True)

    lease_period = fields.Integer(string="Lease Period")
    period_choices = fields.Selection(selection=PERIOD_CHOICES, string="Period Choices")
    tank_qty = fields.Integer(string="Tank Quantity(TEUS)")
    pickup_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Pick Up Depot Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    drop_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Drop Off Depot Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])

    sug_route_id = fields.Many2one("cm.vessel.service.route", string="Route Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])    
    estimated_days = fields.Integer(string="Estimated Days", help="POL Free Days + POD Free Days + Transit Days + Avg T/S Days")
    cleaning_days = fields.Integer(string="Cleaning / Repair / Booking Days", default=15)
    tot_days = fields.Integer(string="Total Days")

    coastal_pol_port_id = fields.Many2one(CM_PORT, string="POL", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '!=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    coastal_pol_terminal_id = fields.Many2one(CM_PORT_TERMINAL, string="POL Terminal", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', coastal_pol_port_id)]")
    coastal_pol_free_days = fields.Integer(string="POL Free Days", default='1')
    coastal_pod_port_id = fields.Many2one(CM_PORT, string="POD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '!=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    coastal_pod_terminal_id = fields.Many2one(CM_PORT_TERMINAL, string="POD Terminal", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', coastal_pol_port_id)]")
    coastal_pod_free_days = fields.Integer(string="POD Free Days", default='1')
    
    rail_pol_port_id = fields.Many2one(CM_PORT, string="POL ICD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    rail_pol_free_days = fields.Integer(string="POL Free Days",  default='1')
    rail_pod_port_id = fields.Many2one(CM_PORT, string="POD ICD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    rail_pod_free_days = fields.Integer(string="POD Free Days", default='1')


    service_ids = fields.Many2many(CM_SERVICE, string="Additional Services", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    spl_req = fields.Text(string="Special Requirements")
    quotation_remark = fields.Text(string="Quotation Remarks")
    mode_of_payment = fields.Selection(MODE_OF_PAYMENT, string="Mode Of Payment", default="cash")
    
    gr_dep_id = fields.Many2one('cm.department', string="GR Sub Department Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    prod_weight_kg = fields.Integer(string="Product Weight(Kgs)")
    dotr_pod_free_days = fields.Integer(string="POD Free Days", default='1')
    dotr_pod_hrs = fields.Integer(string="Hrs")
    dotr_pol_free_days = fields.Integer(string="POL Free Days", default='1')
    dotr_pol_hrs = fields.Integer(string="Hrs")
    trailer_type = fields.Selection(selection=TRAILER_TYPE, string="Trailer Type", default='20_feet')
    free_hrs = fields.Integer(string="Free Hrs", default=24)
    trans_route_id = fields.Many2one(CM_TRANSPORT_ROUTE, string="Transport Route Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    from_trans_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="From Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    from_city_id = fields.Many2one(CM_CITY, string="From City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    from_state_id = fields.Many2one(RES_COUNTRY_STATE, string="From State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_trans_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="To Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_city_id = fields.Many2one(CM_CITY, string="To City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_state_id = fields.Many2one(RES_COUNTRY_STATE, string="To State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    trip_start_date = fields.Date(string="Tentative Trip Start Date")
    trans_pickup_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Empty Pick Up Depot", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    empty_pickup_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="Drop Off Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    load_address = fields.Char(string="Loading Address", size=252)
    load_zip_code = fields.Char(string="Exact Loading Location Zip Code", size=10)
    unload_address = fields.Char(string="Unloading Address", size=252)
    unload_zip_code = fields.Char(string="Exact Unloading Location Zip Code", size=10)
    empty_offload_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="Empty Off Loading Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])


    combined_codes = fields.Char(string="Combined Codes")
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

    tax_amt = fields.Float(string="Tax Amount(+)", store=True, compute='_compute_all_line')	
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')	
    other_amt = fields.Float(string="Other Charges(+)", store=True, compute='_compute_all_line')
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    taxable_amt = fields.Float(string="Taxable Amount", store=True, compute='_compute_all_line')
    round_off_amt = fields.Float(string="Round Off Amount(+/-)", store=True, compute='_compute_all_line')	
    grand_tot_amt = fields.Float(string="Grand Total", store=True, compute='_compute_all_line')
    fixed_disc_amt = fields.Float(string="Fixed Discount Amount(-)", store=True, compute='_compute_all_line')
    net_amt = fields.Float(string="Net Amount", store=True, compute='_compute_all_line')
    manual_round_off = fields.Boolean(string="Apply Manual Round Off", default=False)

    line_ids = fields.One2many('ct.doms.business.confirmation.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.doms.business.confirmation.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.doms.business.confirmation.terms.conditions.line', 'header_id', string="Other Charges", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.doms.business.confirmation.tax.line', 'header_id', string="Tax Breakup", copy=True, c_rule=True)
    line_ids_d = fields.One2many('ct.doms.bus.con.pricing.details.line', 'header_id', string="Pricing Details", copy=True, c_rule=True)
    line_ids_e = fields.One2many('ct.doms.bus.con.cus.pri.details.line', 'header_id', string="Customer Pricing Details", copy=True, c_rule=True)
    

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



 

    def validations(self, **kw):
        warning_msg = []
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': 'ct.doms.business.confirmation.draft',
            'approve': CT_DOMS_BUSINESS_CONFIRMATION
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

    @api.depends('line_ids_e', 'round_off_amt', 'fixed_disc_amt', 'manual_round_off')
    def _compute_all_line(self):
        for data in self:            
            data._compute_footer_calculation()
            type_tax_use_dict = data._initialize_tax_dict()
            data._process_line_items(data.line_ids_e, type_tax_use_dict)
            data.line_ids_c = [(5, 0, 0)]
            tax_values = []
            for tx_name, tx_amt in type_tax_use_dict.items():
                if tx_amt > 0:
                    tax_values.append((0,0,{'tax_name':tx_name,'tax_amt':tx_amt}))
            data.line_ids_c = tax_values 

    def _compute_footer_calculation(self):
        for data in self:
            data.tot_amt = sum(data.line_ids_e.mapped('tot_amt'))
            data.taxable_amt = sum(data.line_ids_e.mapped('taxable_amt'))
            data.disc_amt = sum(data.line_ids_e.mapped('disc_amt'))
            
            old_grand_total = data.taxable_amt + data.tax_amt

            data.taxable_amt = (data.taxable_amt + data.other_amt) - data.disc_amt
            data.tax_amt = sum(data.line_ids_e.mapped('tax_amt'))

            if (old_grand_total != (data.taxable_amt + data.tax_amt)) or (not data.tot_amt):
                data.manual_round_off = False
                data.round_off_amt = 0.00
                data.fixed_disc_amt = 0.00
            
            if not data.manual_round_off:
                data.round_off_amt = round(data.taxable_amt + data.tax_amt) - (data.taxable_amt + data.tax_amt)
                data.round_off_amt = round(data.round_off_amt, 2)

            data.grand_tot_amt = data.tot_amt + data.round_off_amt
            
            data.fixed_disc_amt = 0.00 if data.grand_tot_amt <= 0 else data.fixed_disc_amt
            
            
            data.net_amt = (data.grand_tot_amt) - data.fixed_disc_amt

    def _initialize_tax_dict(self):
        return {
            record['name']: 0
            for record in self.env['account.tax.group'].read_group([], ['name'], ['name'])
        } 

    def _process_line_items(self, line_items, tax_dict):
        for line in line_items:
            if line.unit_price > 0:
                for tax_line in line.tax_ids:
                    self._process_tax_line(line, tax_line, line.unit_price, line.qty, line.disc_per, line.tot_amt, tax_dict)

    def _process_tax_line(self, line, tax_line, price_unit, qty, discount, price_subtotal, type_tax_use_dict):

        tax_value_return = self.env['account.tax']._convert_to_tax_base_line_dict(
                                            self,
                                            partner=False,
                                            currency= line.currency_id,
                                            product=  False,
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

    @api.onchange('round_off_amt')
    def onchange_round_off_amt(self):
        if self.manual_round_off:
            self.fixed_disc_amt = 0.00
            if self.round_off_amt > (self.taxable_amt + self.tax_amt):
                raise UserError(_("Round Off Amount should not be greater than Grand Total"))
            if self.round_off_amt < 0 and self.grand_tot_amt < 0:
                raise UserError(_("Round Off Amount should not be lesser than Grand Total"))
    
    @api.onchange('fixed_disc_amt')
    def onchange_fixed_disc_amt(self):
        if self.fixed_disc_amt:
            if self.fixed_disc_amt < 0:
                raise UserError(_("Fixed Discount Amount should not be lesser than zero"))
            if self.fixed_disc_amt > self.grand_tot_amt:
                raise UserError(_("Fixed Discount Amount should not be greater than Grand Total"))
            

    def auto_doms_bc_entry_creation(self, **kw):
        qs_rec = kw.get('qs_rec', '')

        if qs_rec and qs_rec.service_id.sys_ref in ('DOTR', 'DOTC', 'DOTT', 'DOTL', 'DOTS'):
            doms_bc_model = qs_rec.env['ct.doms.business.confirmation']

            address = ", ".join(filter(None, [
                qs_rec.bkg_party_id.street,
                qs_rec.bkg_party_id.street1,
                qs_rec.bkg_party_id.city_id.name,
                qs_rec.bkg_party_id.state_id.name,
                qs_rec.bkg_party_id.country_id.name,
                qs_rec.bkg_party_id.pin_code
            ]))

            cus_price_rec = [(0, 0, {
                    'chrg_head_id': rec.chrg_head_id.id,
                    'description': rec.description,
                    'uom_id': rec.uom_id.id,
                    'qty': rec.qty,
                    'unit_price': rec.unit_price,
                    'currency_id': rec.currency_id.id,
                    'tax_ids': [(6, 0, rec.tax_ids.ids)],
                    'disc_amt': rec.disc_amt,
                    'disc_per': rec.disc_per,
                    'unitprice_wt': rec.unitprice_wt,
                    'taxable_amt': rec.taxable_amt,
                    'tax_amt': rec.tax_amt,
                    'tot_amt': rec.tot_amt,
                    'line_tot_amt': rec.line_tot_amt,
                }) for rec in qs_rec.line_ids_g]
            price_rec = [(0, 0, {
                    'chrg_head_id': rec.chrg_head_id.id,
                    'entry_seq': rec.entry_seq,
                    'uom_id': rec.uom_id.id,
                    'qty': rec.qty,
                    'unit_price': rec.unit_price,
                    'currency_id': rec.currency_id.id,
                    'tax_ids': [(6, 0, rec.tax_ids.ids)],
                    'disc_amt': rec.disc_amt,
                    'disc_per': rec.disc_per,
                    'unitprice_wt': rec.unitprice_wt,
                    'markup_value': rec.markup_value,
                    'taxable_amt': rec.taxable_amt,
                    'q_currency_id': rec.quotation_currency_id.id,
                    'conversion_rate': rec.conversion_rate,
                    'converted_cost_price': rec.converted_cost_price,
                    'tax_amt': rec.tax_amt,
                    'tot_amt': rec.tot_amt,
                    'line_tot_amt': rec.line_tot_amt,
                    'line_applicable': rec.line_applicable,
                    'grouping': rec.grouping,
                }) for rec in qs_rec.line_ids_c]

            doms_bc_rec = doms_bc_model.create({
                'qs_no': qs_rec.id,
                'qs_date': qs_rec.entry_date,
                'service_id': qs_rec.service_id.id,
                'sales_person_id': qs_rec.generated_user_id.id,
                'ship_term_id': qs_rec.ship_term_id.id,
                'customer_id': qs_rec.bkg_party_id.id,
                'contact_person': qs_rec.bkg_party_id.contact_person,
                'mobile_no': qs_rec.bkg_party_id.mobile_no,
                'email': qs_rec.bkg_party_id.email,
                'cus_bill_address': address,
                'cus_del_address': address,
                'product_id': qs_rec.product_id.id,
                'dg_product': qs_rec.dg_product,
                'un_no': qs_rec.un_no,
                'imo_class': qs_rec.imo_class,
                'pack_grp': qs_rec.pack_grp,
                'sds_attach_ids': qs_rec.sds_attach_ids,
                'lease_period': qs_rec.lease_period,
                'period_choices': qs_rec.period_choices,
                'tank_qty': qs_rec.tank_qty,
                'pickup_depot_id': qs_rec.pickup_depot_id.id,
                'drop_depot_id': qs_rec.drop_depot_id.id,
                'service_ids': qs_rec.service_ids,
                'spl_req': qs_rec.spl_req,
                'mode_of_payment': qs_rec.mode_of_payment,
                'line_ids_e': cus_price_rec,
                'line_ids_d': price_rec,
                'line_ids_b': [(0, 0, line.copy_data()[0]) for line in qs_rec.line_ids_k],
                'line_ids_a': [(0, 0, line.copy_data()[0]) for line in qs_rec.line_ids_a],
                'quotation_remark': qs_rec.remarks,
                'round_off_amt': qs_rec.round_off_amt,
                'net_amt': qs_rec.net_amt,
                'currency_id': qs_rec.quotation_currency_id.id,
                'manual_round_off': qs_rec.manual_round_off,
                'combined_codes': [qs_rec.service_id.sys_ref],
                'entry_mode': 'auto'
            })
            if doms_bc_rec and qs_rec.service_id.sys_ref in ('DOTC','DOTT'):
                doms_bc_rec.write({
                    'sug_route_id': qs_rec.sug_route_id.id,
                    'estimated_days': qs_rec.estimated_days,
                    'cleaning_days': qs_rec.cleaning_days,
                    'tot_days': qs_rec.tot_days,
                })
            if doms_bc_rec and qs_rec.service_id.sys_ref in ('DOTC'):
                doms_bc_rec.write({
                    'coastal_pol_port_id': qs_rec.coastal_pol_port_id.id,
                    'coastal_pol_terminal_id': qs_rec.coastal_pol_terminal_id.id,
                    'coastal_pol_free_days': qs_rec.coastal_pol_free_days,
                    'coastal_pod_port_id': qs_rec.coastal_pod_port_id.id,
                    'coastal_pod_terminal_id': qs_rec.coastal_pod_terminal_id.id,
                    'coastal_pod_free_days': qs_rec.coastal_pod_free_days,
                })
            if doms_bc_rec and qs_rec.service_id.sys_ref in ('DOTT'):
                doms_bc_rec.write({
                    'rail_pol_port_id': qs_rec.rail_pol_port_id.id,
                    'rail_pol_free_days': qs_rec.rail_pol_free_days,
                    'rail_pod_port_id': qs_rec.rail_pod_port_id.id,
                    'rail_pod_free_days': qs_rec.rail_pod_free_days,
                })

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
                        [('code', '=', CT_DOMS_BUSINESS_CONFIRMATION)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s, %s, %s, %s, %s, %s) """ ,
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
            
            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

            self.transaction_mail_data_design(
                                            trans_rec = self, entry_action = 'entry_approve' ,
                                            mail_queue_name = 'Entry Approve Mail',
                                            subject = f"#Transaction {self.name} Approved",
                                            mail_config_name = 'Transaction Approve Mail'
                                        )

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
        return super(CtDomsBusinessConfirmation, self).write(vals)


    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_DOMS_BUSINESS_CONFIRMATION].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.user_id.email]

        return mail_ids
    
    def transaction_mail_data_design(self, **kw):
        self.env.cr.execute(
            """select ctm_template(%s,'%s','%s','%s')""" %
            (self.id,self.status,self.name or self.draft_name, self.env.user.partner_id.name,))
        data = self.env.cr.fetchall()

        trans_rec = kw.get('trans_rec', self)
        mail_queue_name = kw.get('mail_queue_name', '')
        mail_config_name = kw.get('mail_config_name', '')
        mail_type = kw.get('mail_type', 'transaction')

        subject = kw.get('subject', '')

        if trans_rec and data[0][0] and mail_queue_name and subject and mail_config_name:

            mail_ids = self.get_default_mail_ids(trans_id=trans_rec.id)
            default_to = mail_ids.get('email_to',[])

            vals = self.env['cp.mail.configuration'].mail_config_mailids_data(
                mail_type=mail_type, model_name=CT_DOMS_BUSINESS_CONFIRMATION, mail_name=mail_config_name)

            email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
            email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
            email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
            email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''

            if trans_rec.line_ids_a:
                attachment = trans_rec.line_ids_a.mapped('attachment_ids')
            else:
                attachment = False

            self.env['cp.mail.queue'].create_mail_queue(
                name = mail_queue_name, trans_rec = trans_rec, mail_from = email_from,
                email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                subject = subject, body = data[0][0], attachment=attachment)

        return True

    def transaction_sms_design(self, **kw):
        trans_rec = kw.get('trans_rec', self)
        sms_name = kw.get('sms_name', '')
        content_text = kw.get('content_text', '')
        message_type = kw.get('message_type', '')

        if trans_rec and sms_name and content_text and message_type:
            default_mobile = [self.user_id.mobile_no] if self.user_id.mobile_no else []

            vals = self.env['cp.sms.configuration'].sms_config_data(
                message_type=message_type, action_name=sms_name)
            mobile_no = ", ".join(set(default_mobile + vals.get('mobile_no', []))) if default_mobile or vals.get('mobile_no') else ''

            self.env['cp.sms.queue'].create_sms_queue(
                message_type = message_type, trans_rec = trans_rec,
                sms_name = sms_name, mobile_no = mobile_no, content_text = content_text)

        return True

    def value_readable_format(self, value, format='%.1f'):
        powers = [10**15, 10**12, 10**9, 10**6, 10**3]
        human_powers = ['Qa','T', 'B', 'M', 'K']

        for power, human_power in zip(powers, human_powers):
            if value >= power:
                return format % (float(value) / power) + ' ' + human_power
            else:
                value = round(value,2)
        return str(value)

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
            'my_today_value': 0,
            'today_highest_tot':0,
            'ref_no':'',
            'company_currency_symbol': self.env.company.currency_id.symbol
        }

        ct_trans = self.env[CT_DOMS_BUSINESS_CONFIRMATION]
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
        result['all_today_value'] = self.value_readable_format(sum(ct_trans.search([('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_today_value'] = self.value_readable_format(sum(ct_trans.search([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        max_transaction = max(ct_trans.search([('crt_date', '>=', fields.Date.today()), ('status', '=', 'approved')]), 
                      key=lambda t: t.net_amt, default=None)
        result['today_highest_tot'] = self.value_readable_format(max_transaction.net_amt) if max_transaction else 0
        result['ref_no'] = max_transaction.name if max_transaction else '-'

        return result