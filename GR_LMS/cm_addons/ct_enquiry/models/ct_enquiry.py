# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime, timedelta
from odoo.exceptions import UserError

CT_ENQUIRY = 'ct.enquiry'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'
CM_PORT = 'cm.port'
CM_DEPOT_LOCATION = 'cm.depot.location'
CM_TRANSPORT_LOCATION = 'cm.transport.location'
CM_CITY = 'cm.city'
CM_PORT_TERMINAL = 'cm.port.terminal'
CM_SERVICE = 'cm.service'
RES_COUNTRY_STATE = 'res.country.state'
CM_PRODUCT = 'cm.product'
IR_ATTACHMENT = 'ir.attachment'
RES_CURRENCY = 'res.currency'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('rfq_sent', 'RFQ Sent'),
    ('quotation_sent', 'Quotation Sent'),
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('cancelled', 'Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                     ('not_applicable', 'Not Applicable')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

DG_PRODUCT = [('yes', 'DG'), ('no', 'Non DG')]

CONTAINER_CATEGORY = [('laden','Laden'), ('empty', 'Empty')]

TRAILER_TYPE = [('20_feet', '20 Feet'), ('40_feet', '40 Feet'), ('both', 'Both')]

POD_SERVICES = [('disposal', 'Disposal'), ('discharge', 'Discharge'), ('both', 'Both'), ('not_required', 'Not Required')]

INSURANCE = [('customer', 'Customer'), ('gmpl', 'GMPL')]

LOCATION = [('pan_india', 'PAN India'), ('exim', 'Exim(Global)')]

PERIOD_CHOICES = [('day', 'Day'), ('month', 'Month'), ('year', 'Year')]

PACK_GRP = [('1', 'I'), ('2', 'II'), ('3', 'III')]

SDS_STATUS = [('available_valid', 'Available - Valid'),
              ('available_expired', 'Available - Expired'),
              ('not_available', 'New SDS')]

FLEXI_TYPE = [('tltd','TLTD'),
              ('tlbd', 'TLBD'),
              ('blbd', 'BLBD')]

TANK_TYPE = [('20_feet', '20 Feet'), ('40_feet', '40 Feet')]

CLEANING_STATUS = [('cleaned', 'Cleaned'), ('un_cleaned', 'Uncleaned')]

OPERATIONAL_TYPE = [('loading', 'Loading'),
                    ('unloading', 'Unloading'),
                    ('cross_loading', 'Cross Loading'),
                    ('disposal_assistance', 'Disposal Assistance')]

class CtEnquiry(models.Model):
    _name = 'ct.enquiry'
    _description = 'Enquiry'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Enquiry No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    entry_date = fields.Date(string="Enquiry Date", copy=False, default=fields.Date.today)
    service_id = fields.Many2one(CM_SERVICE, string="Service Name",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    generated_user_id = fields.Many2one(RES_USERS, string="Sales Person", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    enq_source_id = fields.Many2one('cm.enquiry.source', string="Enquiry Source",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ref_no = fields.Char(string="Reference Details / Date")
    bkg_party_id = fields.Many2one('cm.customer', string="Booking Party",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    new_bkg_party = fields.Char(string="New Booking Party", )
    bus_vert_id = fields.Many2one('cm.business.vertical', string="Business Vertical",  ondelete='restrict',domain=[('status', '=', 'active'),('active_trans', '=', True)])
    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No",  size=15)
    email = fields.Char(string="Email",size=252)
    shipper_cus_id = fields.Many2one('cm.customer', string="Actual Shipper / Customer", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    new_shipper = fields.Char(string="New Shipper",)
    tank_operator_id = fields.Many2many('cm.tank.operator', string="Tank Operator",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    rebate = fields.Selection(selection=APPLICABLE_OPTION, string="Rebate",)
    cust_rate = fields.Float(string="Customer Indicated Rate")
    currency_id = fields.Many2one(RES_CURRENCY, string="Currency",  ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    expiry_date = fields.Date(string="Last Date to Submit Quote", copy=False)
    project_name = fields.Char(string="Project Name", copy=False)
    lead_remark = fields.Text(string="Lead Remark", copy=False)


    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Empty / Laden", default='laden', c_rule=True)
    cleaning_status = fields.Selection(selection=CLEANING_STATUS, string="Cleaning Status")
    product_id = fields.Many2one(CM_PRODUCT, string="Product Name", ondelete='restrict', domain=[('status', 'in', ('active','reject')),('active_trans', '=', True)])
    product = fields.Char(string="New Product Name", )
    product_status = fields.Char(string="Product Status", )
    ap_rej_note = fields.Text(string="Approval/Rejection Notes",)
    mfg_id = fields.Many2one('cm.product.manufacturer', string="Manufacturer Name",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    sds_status = fields.Selection(selection=SDS_STATUS, string="SDS Status",)
    dg_product = fields.Selection(selection=DG_PRODUCT, string="Product Type" , c_rule=True)
    un_no = fields.Char(string="UN Number",)
    imo_class = fields.Char(string="IMO Class", size=10)
    sub_class1 = fields.Char(string="Sub Class I", size=10)
    sub_class2 = fields.Char(string="Sub Class II", size=10)
    tank_tcode_id = fields.Many2one('cm.tank.tcode', string="Tank T Code", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pack_grp = fields.Selection(selection=PACK_GRP, string="Packing Group")
    mar_poll = fields.Selection(selection=YES_OR_NO, string="Marine Pollutant")
    tank_capacity = fields.Integer(string="Tank Capacity(KL)",)
    tank_qty = fields.Integer(string="Tank Quantity(TEUS)", default='1')
    sds_attach_ids = fields.Many2many(
        IR_ATTACHMENT,
        'ct_enquiry_ir_attachment_sds_rel',
        'ct_enquiry_id',
        'ir_attachment_id',
        string="SDS Document",
        ondelete='restrict',
        check_company=True
    )


    service_ids = fields.Many2many(CM_SERVICE, string="Additional Services", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('id', '!=', service_id)]")
    spl_req = fields.Text(string="Special Requirements",)
    ship_term_id = fields.Many2one('cm.shipment.term', string="Shipment Term", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ship_term = fields.Char(string="Shipment Term", )


    src_address = fields.Char(string="Source Address", size=252)
    dest_address = fields.Char(string="Destination Address", size=252)
    switch_bl_req = fields.Selection(selection=YES_OR_NO, string="Switch BL Required",  default='no')
    same_as_poo = fields.Boolean(string="Same as POO", default=False, help="Click to apply same POO to POL")
    poo_port_id = fields.Many2one(CM_PORT, string="POO", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    pol_port_id = fields.Many2one(CM_PORT, string="POL", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    pol_terminal_id = fields.Many2one(CM_PORT_TERMINAL, string="POL Terminal", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', pol_port_id)]")
    pol_free_days = fields.Integer(string="POL Free Days",)
    same_as_pod = fields.Boolean(string="Same as POD", default=False, help="Click to apply same POD to FPOD")
    pod_port_id = fields.Many2one(CM_PORT, string="POD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    pod_terminal_id = fields.Many2one(CM_PORT_TERMINAL, string="POD Terminal",  ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', pod_port_id)]")
    fpod_port_id = fields.Many2one(CM_PORT, string="FPOD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    pod_free_days = fields.Integer(string="POD Free Days",)
    trip_pickup_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Pick Up Depot Location",ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    payment_centre_port_id = fields.Many2one(CM_PORT, string="Payment Centre Port",  ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    empty_or_laden = fields.Selection(selection=CONTAINER_CATEGORY, string="Empty / Laden", c_rule=True)
    pol_detention = fields.Float(string="POL Detention")
    pod_detention = fields.Float(string="POD Detention")
    pol_pod_currency_id = fields.Many2one(RES_CURRENCY, string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ind_slot_rate = fields.Float(string="Indicated Slot Rate")
    ind_slot_currency_id = fields.Many2one(RES_CURRENCY, string="Currency",  ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    nomination_port_id = fields.Many2one(CM_PORT, string="Nomination Port",  ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")

    
    
    
    lease_period = fields.Integer(string="Lease Period", copy=False)
    period_choices = fields.Selection(selection=PERIOD_CHOICES, string="Lease Period", copy=False)
    pickup_port_id = fields.Many2one(CM_PORT, string="Pick Up Port Location", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    pickup_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Pick Up Depot Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    drop_port_id = fields.Many2one(CM_PORT, string="Drop Off Port Location", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('sanctioned_port', '=', 'yes')]")
    drop_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Drop Off Depot Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])



    gr_dep_id = fields.Many2one('cm.department', string="GR Sub Department Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    prod_weight_kg = fields.Integer(string="Product Weight(Kgs)",)
    dotr_pod_free_days = fields.Integer(string="POD Free Days", default='1')
    dotr_pod_hrs = fields.Integer(string="Hrs",)
    dotr_pol_free_days = fields.Integer(string="POL Free Days", default='1')
    dotr_pol_hrs = fields.Integer(string="Hrs")
    trailer_type = fields.Selection(selection=TRAILER_TYPE, string="Trailer Type",  default='20_feet')
    free_hrs = fields.Integer(string="Free Hrs", default=24)
    trans_route_id = fields.Many2one('cm.transport.route', string="Transport Route Name",ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    from_trans_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="From Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    from_city_id = fields.Many2one(CM_CITY, string="From City", ondelete='restrict',  domain=[('status', '=', 'active'),('active_trans', '=', True)])
    from_state_id = fields.Many2one(RES_COUNTRY_STATE, string="From State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_trans_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="To Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_city_id = fields.Many2one(CM_CITY, string="To City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_state_id = fields.Many2one(RES_COUNTRY_STATE, string="To State",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    trip_start_date = fields.Date(string="Tentative Trip Start Date",)
    trans_pickup_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Empty Pick Up Depot",ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    empty_pickup_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="Drop Off Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    load_address = fields.Char(string="Loading Address", size=252)
    load_zip_code = fields.Char(string="Exact Loading Location Zip Code", size=10)
    unload_address = fields.Char(string="Unloading Address", size=252)
    unload_zip_code = fields.Char(string="Exact Unloading Location Zip Code", size=10)
    empty_offload_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="Empty Off Loading Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])



    flexi_type = fields.Selection(selection=FLEXI_TYPE, string="Flexi Type")
    flexi_layer_type_id = fields.Many2one('cm.flexi.layer.type', string="Layer Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    flexi_capacity_id = fields.Many2one('cm.flexi.capacity', string="Capacity", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bag_qty = fields.Float(string="Bag Quantity(Nos)", digits=(2, 3))
    del_address = fields.Char(string="Delivery Address", size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True)]")
    same_as_delivery = fields.Boolean(string="Same As Delivery Address")
    stuff_address = fields.Char(string="Exact Stuffing Address", size=252)
    bag_req_date = fields.Date(string="Bag Required Date")
    vendor_id = fields.Many2one('cm.vendor.master', string="Preferred Vendor", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    accessories_req = fields.Selection(selection=YES_OR_NO, string="Accessories Required", default='yes')
    pod_services = fields.Selection(selection=POD_SERVICES, string="POD Services")


    operational_type = fields.Selection(selection=OPERATIONAL_TYPE, string="Operational Type")
    flexi_stuff_qty = fields.Float(string="Flexi Stuffing Qty", digits=(2, 3))	    
    stuff_date = fields.Date(string="Stuffing Date", )


    carrier_id = fields.Many2one('cm.carrier', string="Carrier Name", ondelete='restrict',domain=[('status', '=', 'active'),('active_trans', '=', True)])
    insurance = fields.Selection(selection=INSURANCE, string="Insurance", default='customer')
    tank_test_cert_ids = fields.Many2many(IR_ATTACHMENT, string="Tank Periodic Test Certificate", ondelete='restrict', check_company=True)
    tank_clean_cert_ids = fields.Many2many(IR_ATTACHMENT, 'ir_attachment_tank_clean_cert', 'enq_id', 'ir_attach_id', string="Tank Cleaning Certificate", ondelete='restrict', check_company=True)


    rail_pol_port_id = fields.Many2one(CM_PORT, string="POL ICD",  ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    rail_pol_free_days = fields.Integer(string="POL Free Days", default='1')
    rail_pod_port_id = fields.Many2one(CM_PORT, string="POD ICD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    rail_pod_free_days = fields.Integer(string="POD Free Days", default='1')



    end_gr_dep_id = fields.Many2one('cm.department', string="GR Sub Department Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_prod_weight_kg = fields.Integer(string="Product Weight(Kgs)",)
    end_dotr_pod_free_days = fields.Integer(string="POD Free Days", default='1')
    end_dotr_pod_hrs = fields.Integer(string="Hrs", )
    end_dotr_pol_free_days = fields.Integer(string="POL Free Days",  default='1')
    end_dotr_pol_hrs = fields.Integer(string="Hrs", )
    end_trailer_type = fields.Selection(selection=TRAILER_TYPE, string="Trailer Type",default='20_feet')
    end_free_hrs = fields.Integer(string="Free Hrs", default=24)
    end_trans_route_id = fields.Many2one('cm.transport.route', string="Transport Route Name",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_from_trans_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="From Location",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_from_city_id = fields.Many2one(CM_CITY, string="From City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_from_state_id = fields.Many2one(RES_COUNTRY_STATE, string="From State",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_to_trans_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="To Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_to_city_id = fields.Many2one(CM_CITY, string="To City",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_to_state_id = fields.Many2one(RES_COUNTRY_STATE, string="To State",  ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_trip_start_date = fields.Date(string="Tentative Trip Start Date",)
    end_trans_pickup_depot_id = fields.Many2one(CM_DEPOT_LOCATION, string="Empty Pick Up Depot", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_empty_pickup_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="Drop Off Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    end_load_address = fields.Char(string="Loading Address", size=252)
    end_load_zip_code = fields.Char(string="Exact Loading Location Zip Code", size=10)
    end_unload_address = fields.Char(string="Unloading Address", size=252)
    end_unload_zip_code = fields.Char(string="Exact Unloading Location Zip Code",  size=10)
    end_empty_offload_loc_id = fields.Many2one(CM_TRANSPORT_LOCATION, string="Empty Off Loading Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])



    coastal_pol_port_id = fields.Many2one(CM_PORT, string="POL", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '!=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    coastal_pol_terminal_id = fields.Many2one(CM_PORT_TERMINAL, string="POL Terminal", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', coastal_pol_port_id)]")
    coastal_pol_free_days = fields.Integer(string="POL Free Days", default='1')
    coastal_pod_port_id = fields.Many2one(CM_PORT, string="POD",  ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '!=', 'dry_port'),('sanctioned_port', '=', 'yes')]")
    coastal_pod_terminal_id = fields.Many2one(CM_PORT_TERMINAL, string="POD Terminal", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', coastal_pod_port_id)]")
    coastal_pod_free_days = fields.Integer(string="POD Free Days", default='1')

    

    tank_type = fields.Selection(selection=TANK_TYPE, string="Tank Type", default='20_feet')
    tank_sale_qty = fields.Integer(string="Tank Quantity(TEUS)",)
    tank_sale_product_id = fields.Many2one(CM_PRODUCT, string="Product Name", ondelete='restrict', domain=[('status', 'in', ('active','reject')),('active_trans', '=', True)])
    tank_sale_product = fields.Char(string="New Product Name",)
    tank_sale_dg_product = fields.Selection(selection=DG_PRODUCT, string="Product Type" ,c_rule=True)
    year_built = fields.Integer(string="Manufacturing Year")
    depot_ids = fields.Many2many(CM_DEPOT_LOCATION, string="Depot Empty Pick Up Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])


    executed_user_id = fields.Many2one(RES_USERS, string="Executed By", default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    bus_location = fields.Selection(selection=LOCATION, string="Business Location")
    sales_lead_id = fields.Many2one('ct.sales.lead', string="Lead No", copy=False, ondelete='restrict')


    rej_remark_id = fields.Many2one('cm.rejection.remark', string="Reason", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    cancel_remark = fields.Text(string="Remark")
    remarks = fields.Text(string="Remarks", copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status",  default="draft", readonly=True, store=True, tracking=True, copy=False)
    combined_codes = fields.Char(string="Combined Codes", readonly=True)

    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", copy=False, ondelete='restrict', readonly=True)
    cancel_date = fields.Datetime(string="Cancelled Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids = fields.One2many('ct.enquiry.flexi.acc.line', 'header_id', string="Flexi Accessories", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.enquiry.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    @api.onchange('service_id')
    def onchange_service_id(self):
        if self.service_id:
            self.bus_location = self.service_id.bus_location
            if self.service_id.sys_ref in ('ISTL', 'DOTL'):
                self.container_category = 'empty'
            else:
                self.container_category = 'laden'
                self.empty_or_laden = 'empty'
            if self.service_id.sys_ref == 'DOTL':
                tank_rec = self.env['cm.tank.operator'].search(
                    [('short_name', '=', 'GMPL'), ('status', '=', 'active'), 
                    ('active_trans', '=', True)], limit=1
                )
                self.tank_operator_id = [(6, 0, self.tank_operator_id.ids + [tank_rec.id])] if tank_rec else []
            else:
                self.tank_operator_id = False

    @api.onchange('service_id', 'service_ids')
    def onchange_service_ids(self):
        codes = []
        if self.service_id:
            codes.append(self.service_id.sys_ref)
            if self.entry_mode == 'auto':
                self.onchange_service_id()
        if self.service_ids:
            codes.extend(self.service_ids.mapped('sys_ref'))
        self.combined_codes = list(set(codes))

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.dg_product = self.product_id.dg_product
            self.un_no = self.product_id.un_no
            self.imo_class = self.product_id.imo_class
            self.sub_class1 = self.product_id.sub_class1
            self.sub_class2 = self.product_id.sub_class2
            self.tank_tcode_id = self.product_id.tank_t_codes if len(self.product_id.tank_t_codes) == 1 else [(5, 0, 0)]
            self.pack_grp = self.product_id.pack_grp
            self.mar_poll = self.product_id.mar_poll
            self.product = False
            self.product_status = 'Active' if self.product_id.status == 'active' else 'Reject'
            if (self.product_id.bus_location == 'pan_india' and self.service_id
                and self.service_id.bus_location == 'exim'):
                raise UserError(_("This product can be eligible only for PAN India business."))
            elif (self.product_id.bus_location == 'exim' and self.service_id
                and self.service_id.bus_location == 'pan_india'):
                raise UserError(_("This product can be eligible only for Exim business."))
            else:
                self.ap_rej_note = self.product_id.ap_rej_note
        else:
            self.dg_product = False
            self.un_no = False
            self.imo_class = False
            self.sub_class1 = False
            self.sub_class2 = False
            self.tank_tcode_id = False
            self.mar_poll = False
            self.product_status = False
            self.ap_rej_note = False
            self.sds_attach_ids = [(5, 0, 0)]

    @api.onchange('dg_product')
    def onchange_dg_product(self):
        if not self.product_id:
            self.un_no = False
            self.imo_class = False
            self.sub_class1 = False
            self.sub_class2 = False
            self.tank_tcode_id = False
            self.pack_grp = False
            self.mar_poll = False
    
    @api.onchange('trans_route_id')
    def onchange_route_name(self):
        if self.trans_route_id:
            self.from_trans_loc_id = self.trans_route_id.from_location_id.id
            self.to_trans_loc_id = self.trans_route_id.to_location_id.id
            self.empty_pickup_loc_id = self.trans_route_id.from_location_id.id
            self.load_address = self.trans_route_id.from_location_id.street
            self.load_zip_code = self.trans_route_id.from_location_id.pin_code
            self.unload_address = self.trans_route_id.to_location_id.street
            self.unload_zip_code = self.trans_route_id.to_location_id.pin_code
            self.empty_offload_loc_id = self.trans_route_id.from_location_id.id
        else:
            self.from_trans_loc_id = False
            self.to_trans_loc_id = False
            self.empty_pickup_loc_id = False
            self.load_address = False
            self.load_zip_code = False
            self.unload_address = False
            self.unload_zip_code = False
            self.empty_offload_loc_id = False
    
    @api.onchange('from_trans_loc_id')
    def onchange_from_location(self):
        if self.from_trans_loc_id:
            self.from_city_id = self.from_trans_loc_id.city_id.id
            self.from_state_id = self.from_trans_loc_id.state_id.id
        else:
            self.from_city_id = False
            self.from_state_id = False
    
    @api.onchange('to_trans_loc_id')
    def onchange_to_location(self):
        if self.to_trans_loc_id:
            self.to_city_id = self.to_trans_loc_id.city_id.id
            self.to_state_id = self.to_trans_loc_id.state_id.id
        else:
            self.to_city_id = False
            self.to_state_id = False

    @api.onchange('bkg_party_id')
    def onchange_booking_party(self):
        if self.bkg_party_id:
            if self.bkg_party_id.bus_vert_ids and len(self.bkg_party_id.bus_vert_ids) == 1:
                self.bus_vert_id = self.bkg_party_id.bus_vert_ids.id
            else:
                self.bus_vert_id = False
            self.contact_person = self.bkg_party_id.contact_person
            self.mobile_no = self.bkg_party_id.mobile_no
            self.email = self.bkg_party_id.email
            if self.service_id.sys_ref == 'DOTL':
                self.shipper_cus_id = self.bkg_party_id.id
            self.new_bkg_party = False
        else:
            self.bus_vert_id = False
            self.contact_person = False
            self.mobile_no = False
            self.email = False
            self.shipper_cus_id = False

    @api.onchange('combined_codes')
    def onchange_combined_codes(self):
        if 'FLAS' not in self.combined_codes:
            self.line_ids = [(5, 0, 0)]
    
    @api.onchange('same_as_delivery', 'del_address')
    def onchange_same_as_delivery(self):
        if self.same_as_delivery:
            self.stuff_address = self.del_address
        else:
            self.stuff_address = False
    
    @api.onchange('same_as_poo','poo_port_id')
    def onchange_same_as_poo(self):
        if self.same_as_poo:
            self.pol_port_id = self.poo_port_id.id
        else:
            self.pol_port_id = False
    
    @api.onchange('same_as_pod','pod_port_id')
    def onchange_same_as_pod(self):
        if self.same_as_pod:
            self.fpod_port_id = self.pod_port_id.id
        else:
            self.fpod_port_id = False
    
    @api.onchange('pol_port_id')
    def onchange_pol_port_id(self):
        if self.pol_port_id:
            record = self.env[CM_PORT_TERMINAL].search([('status', '=', 'active'), 
                      ('active_trans', '=', True), 
                      ('port_id', '=', self.pol_port_id.id)], limit=2)
            if record and len(record) == 1:
                self.pol_terminal_id = record.id
            else:
                self.pol_terminal_id = False

    @api.onchange('pod_port_id')
    def onchange_pod_port_id(self):
        if self.pod_port_id:
            record = self.env[CM_PORT_TERMINAL].search([('status', '=', 'active'), 
                      ('active_trans', '=', True), 
                      ('port_id', '=', self.pod_port_id.id)], limit=2)
            if record and len(record) == 1:
                self.pod_terminal_id = record.id
            else:
                self.pod_terminal_id = False     

    @api.onchange('ship_term_id')
    def onchange_ship_term_id(self):
        self.src_address = False    
        self.dest_address = False   
        self.ship_term = self.ship_term_id.sys_ref if self.ship_term_id else False

    @api.onchange('mfg_id', 'product_id', 'product')
    def onchange_mfg_id(self):
        self.sds_attach_ids = [(5, 0, 0)]
        if self.product_id and self.mfg_id:
            records = self.env['cm.sds.product'].search([
                    ('status', 'in', ('active', 'expired')), 
                    ('active_trans', '=', True), 
                    ('product_id', '=', self.product_id.id),
                    ('mfg_id', '=', self.mfg_id.id)])
            statuses = {rec.status for rec in records}
            if 'active' in statuses:
                self.sds_status = 'available_valid'
            elif 'expired' in statuses:
                self.sds_status = 'available_expired'
            else:
                self.sds_status = 'not_available'

            sds_rec = self.env['cm.sds.product'].search([
                ('status', '=', 'active'), 
                ('active_trans', '=', True), 
                ('product_id', '=', self.product_id.id),
                ('mfg_id', '=', self.mfg_id.id)
            ], limit=1)
            self.sds_attach_ids = sds_rec.attachment_ids
        elif (not self.product_id and self.product) or (self.product_id and not self.mfg_id):
            self.sds_status = 'not_available'
        else:
            self.sds_status = False


    @api.onchange('tank_sale_product_id')
    def onchange_tank_sale_product(self):
        if self.tank_sale_product_id:
            self.tank_sale_dg_product = self.tank_sale_product_id.dg_product
        else:
            self.tank_sale_dg_product = False

    @api.onchange('coastal_pol_port_id')
    def onchange_coastal_pol_port_id(self):
        if self.coastal_pol_port_id:
            record = self.env[CM_PORT_TERMINAL].search([('status', '=', 'active'), 
                      ('active_trans', '=', True), 
                      ('port_id', '=', self.coastal_pol_port_id.id)], limit=2)
            if record and len(record) == 1:
                self.coastal_pol_terminal_id = record.id
            else:
                self.coastal_pol_terminal_id = False

    @api.onchange('coastal_pod_port_id')
    def onchange_coastal_pod_port_id(self):
        if self.coastal_pod_port_id:
            record = self.env[CM_PORT_TERMINAL].search([('status', '=', 'active'), 
                      ('active_trans', '=', True), 
                      ('port_id', '=', self.coastal_pod_port_id.id)], limit=2)
            if record and len(record) == 1:
                self.coastal_pod_terminal_id = record.id
            else:
                self.coastal_pod_terminal_id = False  

    @api.onchange('end_trans_route_id')
    def onchange_end_route_name(self):
        if self.end_trans_route_id:
            self.end_from_trans_loc_id = self.end_trans_route_id.from_location_id.id
            self.end_to_trans_loc_id = self.end_trans_route_id.to_location_id.id
            self.end_empty_pickup_loc_id = self.end_trans_route_id.from_location_id.id
            self.end_load_address = self.end_trans_route_id.from_location_id.street
            self.end_load_zip_code = self.end_trans_route_id.from_location_id.pin_code
            self.end_unload_address = self.end_trans_route_id.to_location_id.street
            self.end_unload_zip_code = self.end_trans_route_id.to_location_id.pin_code
            self.end_empty_offload_loc_id = self.end_trans_route_id.from_location_id.id
        else:
            self.end_from_trans_loc_id = False
            self.end_to_trans_loc_id = False
            self.end_empty_pickup_loc_id = False
            self.end_load_address = False
            self.end_load_zip_code = False
            self.end_unload_address = False
            self.end_unload_zip_code = False
            self.end_empty_offload_loc_id = False
    
    @api.onchange('end_from_trans_loc_id')
    def onchange_end_from_location(self):
        if self.end_from_trans_loc_id:
            self.end_from_city_id = self.end_from_trans_loc_id.city_id.id
            self.end_from_state_id = self.end_from_trans_loc_id.state_id.id
        else:
            self.end_from_city_id = False
            self.end_from_state_id = False
    
    @api.onchange('end_to_trans_loc_id')
    def onchange_end_to_location(self):
        if self.end_to_trans_loc_id:
            self.end_to_city_id = self.end_to_trans_loc_id.city_id.id
            self.end_to_state_id = self.end_to_trans_loc_id.state_id.id
        else:
            self.end_to_city_id = False
            self.end_to_state_id = False

    @api.onchange('dotr_pol_free_days')
    def onchange_dotr_pol_free_days(self):
        if self.dotr_pol_free_days and self.dotr_pol_free_days > 0:
            self.dotr_pol_hrs = self.dotr_pol_free_days * 24
            self.end_dotr_pol_free_days = self.dotr_pol_free_days
        else:
            self.dotr_pol_hrs = False
            self.end_dotr_pol_free_days = False

    @api.onchange('dotr_pod_free_days')
    def onchange_dotr_pod_free_days(self):
        if self.dotr_pod_free_days and self.dotr_pod_free_days > 0:
            self.dotr_pod_hrs = self.dotr_pod_free_days * 24
            self.end_dotr_pod_free_days = self.dotr_pod_free_days
        else:
            self.dotr_pod_hrs = False
            self.end_dotr_pod_free_days = False

    @api.onchange('end_dotr_pol_free_days')
    def onchange_end_dotr_pol_free_days(self):
        if self.end_dotr_pol_free_days and self.end_dotr_pol_free_days > 0:
            self.end_dotr_pol_hrs = self.end_dotr_pol_free_days * 24
        else:
            self.end_dotr_pol_hrs = False

    @api.onchange('end_dotr_pod_free_days')
    def onchange_end_dotr_pod_free_days(self):
        if self.end_dotr_pod_free_days and self.end_dotr_pod_free_days > 0:
            self.end_dotr_pod_hrs = self.end_dotr_pod_free_days * 24
        else:
            self.end_dotr_pod_hrs = False

    @api.onchange('gr_dep_id')
    def onchange_gr_dep_id(self):
        if self.gr_dep_id:
            self.end_gr_dep_id = self.gr_dep_id.id
        else:
            self.end_gr_dep_id = False

    @api.onchange('prod_weight_kg')
    def onchange_prod_weight_kg(self):
        if self.prod_weight_kg:
            self.end_prod_weight_kg = self.prod_weight_kg
        else:
            self.end_prod_weight_kg = False

    @api.onchange('trailer_type')
    def onchange_trailer_type(self):
        if self.trailer_type:
            self.end_trailer_type = self.trailer_type
        else:
            self.trailer_type = False
            
    @api.onchange('pol_detention','pod_detention')
    def onchange_pol_detention(self):
        if self.pol_detention > 0 or self.pod_detention > 0:
            self.pol_pod_currency_id = self.env.ref('base.USD').id
        else:
            self.pol_pod_currency_id = False

    @api.onchange('container_category')
    def onchange_empty_or_laden(self):
        self.cleaning_status = False
        self.common_product_onchange()

    @api.onchange('cleaning_status')
    def onchange_cleaning_status(self):
        self.common_product_onchange()

    def common_product_onchange(self):
        self.product_id = False
        self.product = False
        self.mfg_id = False
        self.dg_product = False
        self.tank_tcode_id = False
        self.tank_qty = 1
        self.pol_free_days = False
        self.pod_free_days = False
        self.pol_detention = False
        self.pod_detention = False
        self.pol_pod_currency_id = False
        if 'SOCR' in (self.combined_codes or '') and self.container_category:
            if self.container_category == 'empty':
                self.empty_or_laden = 'laden'
            elif self.container_category == 'laden':
                self.empty_or_laden = 'empty'
        else:
            self.empty_or_laden = False

    @api.onchange('empty_pickup_loc_id')
    def onchange_empty_pickup_loc_id(self):
        if self.empty_pickup_loc_id:
            self.load_address = self.empty_pickup_loc_id.street
            self.load_zip_code = self.empty_pickup_loc_id.pin_code
        else:
            self.load_address = False
            self.load_zip_code = False

    @api.onchange('end_empty_pickup_loc_id')
    def onchange_end_empty_pickup_loc_id(self):
        if self.end_empty_pickup_loc_id:
            self.end_load_address = self.end_empty_pickup_loc_id.street
            self.end_load_zip_code = self.end_empty_pickup_loc_id.pin_code
        else:
            self.end_load_address = False
            self.end_load_zip_code = False

    @api.constrains('sds_attach_ids')
    def check_sds_attach_ids(self):
        for record in self:
            for attachment in record.sds_attach_ids:
                if attachment.mimetype != 'application/pdf':
                    raise UserError(_("Only PDF file is allowed in the SDS Document field."))

    def validations(self, **kw):
        warning_msg = []
        
        self.validate_exclusive_fields(warning_msg)
        if self.combined_codes:
            self.validate_combined_code_rules(warning_msg)
        self.check_negative_values(warning_msg, skip_fields=['lease_period'])
        self.check_product_restriction(warning_msg)
        self.validate_flbs_service(warning_msg)
        self.validate_flas_service(warning_msg)
        self.validate_flos_service(warning_msg)
        self.validate_dots_service(warning_msg)
        
        return self.display_warnings(warning_msg, kw)

    def validate_exclusive_fields(self, warning_msg):
        if self.validate_fields(self.bkg_party_id, self.new_bkg_party):
            warning_msg.append("Either booking party or new booking party is must. Both and both are empty is not allowed")
        if (self.shipper_cus_id or self.new_shipper) and self.validate_fields(self.shipper_cus_id, self.new_shipper):
            warning_msg.append("Both the actual shipper / customer and the new shipper are not allowed.")
        if any(code in self.combined_codes for code in (
                'DOTR', 'DOTC', 'DOTT', 'DOTL', 
                'OSTE', 'OSTI', 'ISTL', 'SOCE', 
                'TRAN', 'FLBS', 'OSNR', 'OSNB',
                'SOCI','SOCR')
        ) and (self.container_category == 'laden' or (self.container_category == 'empty' and self.cleaning_status == 'un_cleaned')):
            if self.validate_fields(self.product_id, self.product):
                warning_msg.append("Either product name or new product name only required, not both.")
            if self.sds_status == 'not_available' and not self.sds_attach_ids:
                warning_msg.append("SDS is not available. So, SDS document is required.")
            if 'FLBS' in self.combined_codes and self.dg_product == 'yes':
                warning_msg.append("Flexi service is not applicable for DG type product.")
            if self.tank_qty <= 0:
                warning_msg.append("Tank quantity should be greater than zero.")
            
            if (self.product_id and self.product_id.bus_location == 'pan_india' and self.service_id
                and self.service_id.bus_location == 'exim'):
                warning_msg.append("The product can be eligible only for PAN India business.")
            elif (self.product_id and self.product_id.bus_location == 'exim' and self.service_id
                and self.service_id.bus_location == 'pan_india'):
                warning_msg.append("The product can be eligible only for Exim business.")
        
        if any(code in self.combined_codes for code in ('DOTR', 'TRAN')):
            if self.trip_start_date and self.trip_start_date < fields.Date.today():
                warning_msg.append("Transport details tentative trip start date should not be less than current date.")

        elif any(code in self.combined_codes for code in ('DOTT', 'DOTC')):
            if self.ship_term in ('CYDO', 'DOCY', 'DRDR') and self.trip_start_date and self.trip_start_date < fields.Date.today():
                warning_msg.append("Transport details tentative trip start date should not be less than current date.")

        if any(code in self.combined_codes for code in ('DOTT', 'DOTC')):
            if self.ship_term == 'DRDR' and self.end_trip_start_date and self.end_trip_start_date < fields.Date.today():
                warning_msg.append("Transport details - POD tentative trip start date should not be less than current date.")

        if self.expiry_date and self.expiry_date < fields.Date.today():
            warning_msg.append("Last date to submit quote should not be less than current date.")

    def validate_fields(self, *fields):
        return not any(fields) or all(fields)

    def validate_combined_code_rules(self, warning_msg):
        if any(code in self.combined_codes for code in ('ISTL', 'DOTL')):
            if self.validate_fields(self.pickup_port_id, self.pickup_depot_id):
                warning_msg.append("Either pick up port location or pick up depot location only required, not both or neither.")
            if self.lease_period <= 0:
                warning_msg.append("Lease period should be greater than zero.")

        if any(code in self.combined_codes for code in ['OSTE', 'OSTI', 'SOCE', 'OSNR', 'OSNB', 'SOCI', 'SOCR']):
            valid_ports = [self.poo_port_id, self.pol_port_id, self.fpod_port_id]
            valid_port_ids = [port.id for port in valid_ports if port]
            if self.payment_centre_port_id and self.payment_centre_port_id.id not in valid_port_ids:
                warning_msg.append("Payment centre port is invalid. It can be either POL or POD")
            if (self.pol_port_id and self.pol_port_id.id) == (self.pod_port_id and self.pod_port_id.id):
                warning_msg.append("POL and POD should not be the same.")
            # if (self.poo_port_id and self.poo_port_id.country_id.id) != (self.pol_port_id and self.pol_port_id.country_id.id):
            #     warning_msg.append("POO and POL should be in the same country.")
            # if (self.pod_port_id and self.pod_port_id.country_id.id) != (self.fpod_port_id and self.fpod_port_id.country_id.id):
            #     warning_msg.append("POD and FPOD should be in the same country.")
        self.validate_nomination_port(warning_msg)

    def validate_nomination_port(self, warning_msg):
        if 'OSNB' in self.combined_codes and self.nomination_port_id:
            pol_port_id = self.pol_port_id.id if self.pol_port_id else None
            pod_port_id = self.pod_port_id.id if self.pod_port_id else None
            if self.nomination_port_id.id in {pol_port_id, pod_port_id}:
                warning_msg.append(
                    "Nomination port must be different from the POL and POD ports."
                )

    def validate_flbs_service(self, warning_msg):
        if 'FLBS' in self.combined_codes:
            if self.bag_qty < 1:
                warning_msg.append("Bag quantity should be greater than zero.")
            if self.bag_req_date < fields.Date.today():
                warning_msg.append("Bag required date should not be less than current date.")
    
    def validate_flas_service(self, warning_msg):
        if 'FLAS' in self.combined_codes:
            if not self.line_ids:
                warning_msg.append("System does not allow to confirm with empty flexi accessories details.")
            if len(self.line_ids) > 1:
                warning_msg.append("System does not allow to confirm more than one flexi accessories details line.")
            if any(qty < 1 for qty in self.line_ids.mapped('accessory_set_qty')):
                warning_msg.append("Flexi accessories details set qty should be greater than zero.")
            if not any(line.line_ids for line in self.line_ids):
                warning_msg.append("System does not allow without accessories details.")
            for line in self.line_ids:
                accessories_ids = [sub_line.accessories_id.id for sub_line in line.line_ids if sub_line.accessories_id]
                if len(accessories_ids) > len(set(accessories_ids)):
                    warning_msg.append("Duplicate accessories details are not allowed.")
                    break 

    def validate_flos_service(self, warning_msg):
        if 'FLOS' in self.combined_codes:
            if self.flexi_stuff_qty < 1:
                warning_msg.append("Flexi stuffing qty should be greater than zero.")
            if self.stuff_date < fields.Date.today():
                warning_msg.append("Stuffing date should not be less than current date.")

    def validate_dots_service(self, warning_msg):
        if 'DOTS' in self.combined_codes:
            if self.validate_fields(self.tank_sale_product_id, self.tank_sale_product):
                warning_msg.append("Either tank sale product name or new product name only required, not both.")
            if self.tank_sale_qty < 1:
                warning_msg.append("Tank quantity should be greater than zero.")                

    def check_negative_values(self, warning_msg, skip_fields=None):
        skip_fields = skip_fields or []
        for field in self._fields.values():
            if field.name in skip_fields:
                continue
            if isinstance(field, (fields.Integer, fields.Float)):
                value = getattr(self, field.name, None)
                if value is not None and value < 0:
                    field_label = field.string
                    warning_msg.append(f"{field_label} cannot be less than zero.")

    def check_product_restriction(self, warning_msg):
        if not self.product_id:
            return

        domain_base = [
            ('status', '=', 'active'),
            ('active_trans', '=', True),
            ('product_id', '=', self.product_id.id),
            ('bus_location', '=', self.service_id.bus_location),
        ]

        if self.service_id.sys_ref in ('OSTE', 'SOCE', 'OSNB', 'OSCT', 'OSNR'):
            domain_base += [('shipment_type', 'in', ('export', 'all')),]
        elif self.service_id.sys_ref in ('OSTI', 'SOCI'):
            domain_base += [('shipment_type', 'in', ('import', 'all')),]
        elif self.service_id.sys_ref == 'SOCR':
            domain_base += [('shipment_type', 'in', ('import', 'export', 'all')),]
        restriction_model = self.env['cm.port.product.restriction']

        if self.mfg_id:
            vendor_restricted = restriction_model.search_count(
                domain_base + [('mfg_id', '=', self.mfg_id.id)], limit=1
            )
            if vendor_restricted:
                warning_msg.append("The product is restricted for this manufacturer in the product restriction.")

        if self.tank_operator_id:
            operator_restricted = restriction_model.search_count(
                domain_base + [('tank_operator_id', 'in', self.tank_operator_id.ids)], limit=1
            )
            if operator_restricted:
                warning_msg.append("The product is restricted for this operator in the product restriction.")

        if self.pod_port_id:
            port_restricted = restriction_model.search_count(
                domain_base + [('port_id', '=', self.pod_port_id.id)], limit=1
            )
            if port_restricted:
                warning_msg.append("The product is restricted for this port in the product restriction.")


    def display_warnings(self, warning_msg, kw):
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(_(formatted_messages))
            else:
                return [formatted_messages]
        else:
            return False

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': CT_ENQUIRY
        }

        action = kw.get('action')
        if action in action_code_map:
            sequence_code = action_code_map[action]
            sequence_id = self.env[IR_SEQUENCE].search([('code', '=', sequence_code)], limit=1)
            if not sequence_id:
                warning_msg.append("Sequence number configuration issue. Kindly contact LMS team.")
        if kw.get('date'):
            self.env.cr.execute(
                """select value from ir_config_parameter 
                where key = 'custom_properties.seq_num_reset' 
                order by id desc limit 1;
            """)
            seq_reset = self.env.cr.fetchone()
            if not seq_reset or not seq_reset[0]:
                warning_msg.append("The sequence number reset option has not been configured. Kindly contact LMS team.")
            elif seq_reset[0] == 'fiscal_year':
                fiscal_year = self.env['cm.fiscal.year'].search([
                                ('from_date', '<=', kw.get('date')),('to_date', '>=', kw.get('date')),
                                ('status', '=', 'active'),('active', '=', True)])
                if not fiscal_year:
                    warning_msg.append("Financial year is not configured. Kindly contact LMS team.")

        return self.display_warnings(warning_msg, kw)

    def confirm_warning_rule(self):
        
        warning_msgs = []
        self.check_pol_pod_zero_value(warning_msgs)

        if warning_msgs:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view.id if view else False
            context = {
                'message': "\n".join(warning_msgs),
                'transaction_id': self.id,
                'transaction_model': CT_ENQUIRY,
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

        if self.status  == 'draft':
            self.entry_confirm()
        
        return True

    def check_pol_pod_zero_value(self, warning_msgs):
        message = "POL or POD free days is zero. Would you like to proceed with zero value ?"
        checks = [
            (('OSTE', 'OSNB', 'OSTI', 'OSNR', 'SOCE', 'SOCI', 'SOCR'), self.container_category != 'empty', [
                (self.pol_free_days),
                (self.pod_free_days)
            ]),
            (('DOTT', 'DOTC'), self.ship_term in ('CYDO', 'DOCY', 'DRDR'), [
                (self.dotr_pol_free_days),
                (self.dotr_pod_free_days),
                (self.end_dotr_pol_free_days),
                (self.end_dotr_pod_free_days)
            ]),
            (('DOTR',), True, [
                (self.dotr_pol_free_days),
                (self.dotr_pod_free_days)]),
            (('DOTT',), True, [
                (self.rail_pol_free_days),
                (self.rail_pod_free_days)
            ]),
            (('DOTC',), True, [
                (self.coastal_pol_free_days),
                (self.coastal_pod_free_days)
            ])
        ]

        for codes, extra_condition, conditions in checks:
            if any(code in self.combined_codes for code in codes) and extra_condition:
                for value in conditions:
                    if value == 0:
                        warning_msgs.append(message)
                        return


    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_ENQUIRY)], limit=1)
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
                    self.sequence_no_validations(date=self.entry_date, action='confirm')

                self.name = sequence
                
            self.create_quotations()
            if self.entry_mode == 'auto':
                self.sales_lead_id.progress_status = 'quotation_draft'
            self.write({'status': 'rfq_sent',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

            self.enquiry_mail_data_design(
                trans_rec = self,
                mail_queue_name = 'Enquiry Confirm Mail',
                subject = f"#new-enquiry# {self.service_id.name}",
                mail_config_name = 'Enquiry Confirm Mail',
                mail_action = 'confirm_mail'
            )

            if self.product and not self.product_id:
                self.new_product_creation()
                self.enquiry_mail_data_design(
                    trans_rec = self,
                    mail_queue_name = 'Enquiry New Product Confirm Mail',
                    subject = f"#enquiry-new-product# {self.product} - {'DG' if self.dg_product == 'yes' else 'Non DG'}",
                    mail_config_name = 'Enquiry New Product Confirm Mail',
                    mail_action = 'new_product_confirm_mail'
                )

        return True

                      
    def entry_cancel(self):
        if self.status in ('rfq_sent', 'quotation_sent'):
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.rej_remark_id or (not self.cancel_remark or not self.cancel_remark.strip()):
                raise UserError(_("Cancel reason is must. Kindly enter the cancel reason and remark in cancel reason tab"))
            if self.cancel_remark and len(self.cancel_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters are must for cancel remarks"))
            if self.entry_mode == 'auto':
                self.sales_lead_id.progress_status = 'enquiry_cancelled'
            self.quotation_cancel()
            self.write({'status': 'cancelled',
                        'cancel_user_id': self.env.user.id,
                        'cancel_date': time.strftime(TIME_FORMAT)
                        })
        return True

    def quotation_cancel(self):
        qs_recs = self.env['ct.quotations'].search([
            ('enquiry_no', '=', self.name)
        ])

        approved_qs = []
        cancelable_qs = []
        
        for rec in qs_recs:
            if rec.status in ('wfa', 'quotation_sent', 'order_released'):
                approved_qs.append(rec.name)
            elif rec.status == 'draft':
                cancelable_qs.append(rec)

        if approved_qs:
            raise UserError(_("Unable to cancel. This enquiry related quotation has been approved. Ref: {}").format(", ".join(approved_qs)))

        if cancelable_qs:
            qs_recs.write({
                'rej_remark_id': self.rej_remark_id.id,
                'cancel_remark' : self.cancel_remark,
                'status': 'cancelled',
                'cancel_user_id': self.env.user.id,
                'cancel_date': time.strftime(TIME_FORMAT)
            })


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
        return super(CtEnquiry, self).write(vals)

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_ENQUIRY].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids

    def execute_mail_query(self, kw):
        data = []
        mail_action = kw.get('mail_action', '')
        if mail_action == 'confirm_mail':
            self.env.cr.execute(
                "SELECT ctm_enquiry_confirm_mail(%s, %s, %s, %s, %s)",
                (self.id, self.status, self.name, self.env.user.partner_id.name, 'enquiry_confirm')
            )
            data = self.env.cr.fetchall()
        elif mail_action == 'new_product_confirm_mail':
            self.env.cr.execute(
                "SELECT ctm_enquiry_new_product_confirm_mail(%s, %s, %s, %s)",
                (self.id, self.status, self.name, self.env.user.partner_id.name)
            )
            data = self.env.cr.fetchall()
        elif mail_action == 'enquiry_quotation_overdue_mail':
            trans_rec = kw.get('trans_rec', '')
            if trans_rec:
                self.env.cr.execute(
                    "SELECT ctm_enquiry_confirm_mail(%s, %s, %s, %s, %s)",
                    (trans_rec.id, trans_rec.status, trans_rec.name, trans_rec.confirm_user_id.name, 'enquiry_quotation_overdue')
                )
                data = self.env.cr.fetchall()

        return data

    def enquiry_mail_data_design(self, **kw):
        data = self.execute_mail_query(kw)

        trans_rec = kw.get('trans_rec', self)
        mail_queue_name = kw.get('mail_queue_name', '')
        mail_config_name = kw.get('mail_config_name', '')
        mail_type = kw.get('mail_type', 'transaction')

        subject = kw.get('subject', '')

        if trans_rec and (data and data[0][0]) and mail_queue_name and subject and mail_config_name:

            mail_ids = self.get_default_mail_ids(trans_id=trans_rec.id)
            default_to = mail_ids.get('email_to',[])

            vals = self.env['cp.mail.configuration'].mail_config_mailids_data(
                mail_type=mail_type, model_name=CT_ENQUIRY, mail_name=mail_config_name)

            email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
            email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
            email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
            email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''

            attachment = trans_rec.sds_attach_ids if trans_rec.sds_attach_ids else False

            self.env['cp.mail.queue'].create_mail_queue(
                name = mail_queue_name, trans_rec = trans_rec, mail_from = email_from,
                email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                subject = subject, body = data[0][0], attachment=attachment)
    
        return True


    def enquiry_quotation_overdue_scheduler_mail(self):

        current_date = fields.Datetime.now()
        two_working_days_ago = current_date - timedelta(days=2)
        while two_working_days_ago.weekday() in [5, 6]:
            two_working_days_ago -= timedelta(days=1)

        qs_recs = self.env['ct.quotations'].read_group(
            domain=[
                ('enquiry_no', '!=', False),
                ('entry_mode', '=', 'auto'),
                ('status', 'in', ('draft', 'wfa')),
                ('enquiry_date', '<', two_working_days_ago),
                ('enquiry_date', '>', '2025-03-01')
            ],
            fields=['enquiry_no'],
            groupby=['enquiry_no']
        )
        enquiry_nos = [rec['enquiry_no'] for rec in qs_recs if rec['enquiry_no']]

        if enquiry_nos:
            enq_recs = self.env['ct.enquiry'].search([('name', 'in', enquiry_nos)])
            for enq in enq_recs:
                tat_days = 0
                temp_date = enq.confirm_date
                while temp_date.date() < current_date.date():
                    if temp_date.weekday() not in [5, 6]:
                        tat_days += 1
                    temp_date += timedelta(days=1)
                self.enquiry_mail_data_design(
                    trans_rec=enq,
                    mail_queue_name='Enquiry Quotation Overdue',
                    subject=f"#enquiry-quotation-overdue# {enq.name} - TAT : {tat_days} days",
                    mail_config_name='Enquiry Quotation Overdue Mail',
                    mail_action='enquiry_quotation_overdue_mail',
                    mail_type='scheduler'
                )
        return True

    def new_product_creation(self):
        draft_prod = self.env[CM_PRODUCT].create({
            'name' : self.product,
            'dg_product' : self.dg_product,
            'un_no' : self.un_no,
            'imo_class' : self.imo_class,
            'sub_class1' : self.sub_class1,
            'sub_class2' : self.sub_class2,
            'pack_grp' : self.pack_grp,
            'mar_poll' : self.mar_poll,
            'entry_mode' : 'auto'

        })

        line_vals = [
            {
                'header_id': draft_prod.id,
                'attach_desc': line.attach_desc,
                'attachment_ids': [(6, 0, line.attachment_ids.ids)]
            }
            for line in self.line_ids_a
        ]
        if line_vals:
            draft_prod.line_ids.create(line_vals)


    def _istl_line_creation(self, quotation_record):
        quotation_record.update({
                    "lease_period" : self.lease_period,
                    "period_choices" : self.period_choices,
                    "pickup_port_id" : self.pickup_port_id.id,
                    "pickup_depot_id" : self.pickup_depot_id.id,                    
                    "drop_port_id" : self.drop_port_id.id,
                    "drop_depot_id" : self.drop_depot_id.id,
                    "estimated_days": self.env['ct.quotations'].days_conversion(self.period_choices, self.lease_period)                  
                    })
        if self.tank_operator_id and [tank_operator for tank_operator in self.tank_operator_id if tank_operator.short_name == 'GSCS']:
            quotation_record['price_owner'] = 'operator'
            self.env['ct.quotations'].create(quotation_record)
            quotation_record['is_parent'] = True
                
        quotation_id = self.env['ct.quotations'].create(quotation_record) 
        quotation_id._compute_entry_category()
        return True

    def _flbs_line_creation(self, quotation_record):
        quotation_record.update({
                    "flexi_type" : self.flexi_type,
                    "bag_qty" : self.bag_qty,
                    "del_address" : self.del_address,
                    "city_id" : self.city_id.id,
                    "same_as_delivery" : self.same_as_delivery,    
                    "stuff_address" : self.stuff_address,
                    "bag_req_date" : self.bag_req_date,
                    "accessories_req" : self.accessories_req,
                    "pod_services" : self.pod_services,
                    'flexi_layer_type_id': self.flexi_layer_type_id.id,
                    'flexi_capacity_id': self.flexi_capacity_id.id,
                    'vendor_id': self.vendor_id.id                                                         
                 })
        
        flbs_draft_quotation = self.env['ct.quotations'].create(quotation_record) 
        quotations_flexi_bag_pricing = self.env['ct.quotations.flexi.bag.pricing.line']
        quotations_flexi_bag_pricing.create(flbs_draft_quotation.flbs_flexi_bag_pricing(self.flexi_type, self.bag_qty, flbs_draft_quotation.id))
        return True        
    
    def _flas_line_creation(self, quotation_record):
        quotation_record.update({
                    "city_id": self.city_id.id,
                    'flexi_type': self.flexi_type,
                    'flexi_layer_type_id': self.flexi_layer_type_id.id,
                    'flexi_capacity_id': self.flexi_capacity_id.id,
                    'vendor_id': self.vendor_id,                    
                    "line_ids" : [(0,0,{'flexi_type': line.flexi_type,
                                        'flexi_layer_type_id': line.flexi_layer_type_id.id,
                                        'flexi_capacity_id': line.flexi_capacity_id.id,
                                        'vendor_id': line.vendor_id.id,
                                        'accessory_set_qty': line.accessory_set_qty,
                                        'line_ids': [(0,0,{
                                             'accessories_id': acc_line.accessories_id.id,
                                             'uom_id': acc_line.uom_id.id,
                                             'qty': acc_line.qty}) for acc_line in line.line_ids]}) for line in self.line_ids],                                  
                 })
        self.env['ct.quotations'].create(quotation_record)
        return True     
    
    def _flos_line_creation(self, quotation_record):
        quotation_record.update({
                    "flexi_stuff_qty" : self.flexi_stuff_qty,
                    "stuff_date" : self.stuff_date,
                    "operational_type": self.operational_type,
                    "stuff_address" : self.stuff_address                                  
                 })
        self.env['ct.quotations'].create(quotation_record) 
        return True
    
    def _trans_line_creation(self, quotation_record, sys_ref=False):
        quotation_record.update({
                    "gr_dep_id" : self.end_gr_dep_id.id if sys_ref == 'DRDR' else self.gr_dep_id.id,
                    "prod_weight_kg" : self.end_prod_weight_kg if sys_ref == 'DRDR' else self.prod_weight_kg,
                    "trans_pickup_depot_id": self.end_trans_pickup_depot_id.id if sys_ref == 'DRDR' else self.trans_pickup_depot_id.id,
                    "trailer_type" : self.end_trailer_type if sys_ref == 'DRDR' else self.trailer_type,
                    "free_hrs" : self.end_free_hrs  if sys_ref == 'DRDR' else self.free_hrs,
                    "trans_route_id" : self.end_trans_route_id.id if sys_ref == 'DRDR' else self.trans_route_id.id,
                    "from_trans_loc_id" : self.end_from_trans_loc_id.id  if sys_ref == 'DRDR' else self.from_trans_loc_id.id,
                    "from_city_id" : self.end_from_city_id.id if sys_ref == 'DRDR' else self.from_city_id.id,
                    "from_state_id" : self.end_from_state_id.id if sys_ref == 'DRDR' else self.from_state_id.id,
                    "to_trans_loc_id" : self.end_to_trans_loc_id.id if sys_ref == 'DRDR' else self.to_trans_loc_id.id,
                    "to_city_id" : self.end_to_city_id.id if sys_ref == 'DRDR' else self.to_city_id.id,
                    "to_state_id" : self.end_to_state_id.id  if sys_ref == 'DRDR' else self.to_state_id.id,
                    "empty_pickup_loc_id" : self.end_empty_pickup_loc_id.id if sys_ref == 'DRDR' else self.empty_pickup_loc_id.id,
                    "load_address" : self.end_load_address if sys_ref == 'DRDR' else self.load_address,
                    "load_zip_code" : self.end_load_zip_code if sys_ref == 'DRDR' else self.load_zip_code,
                    "unload_address" : self.end_unload_address if sys_ref == 'DRDR' else self.unload_address,
                    "unload_zip_code" : self.end_unload_zip_code if sys_ref == 'DRDR' else self.unload_zip_code,
                    "trip_start_date" : self.end_trip_start_date if sys_ref == 'DRDR' else self.trip_start_date,
                    "empty_offload_loc_id":self.end_empty_offload_loc_id.id if sys_ref == 'DRDR' else self.empty_offload_loc_id.id,
                    "tot_trip":  self.trans_route_id.total_trip,
                    "tot_transit_days": self.trans_route_id.trip_days,
                    "avg_mileage": self.env['cm.transport.tariff'].search([('status', '=', 'active'),('active_trans', '=', True)], limit=1, order='eff_from_date desc').avg_mileage,                                                                                                                                                                                                                                                                                                                                     
                 })
        quotation_record = self.env['ct.quotations'].create(quotation_record) 
        quotation_record._compute_entry_category()
        return True
    
    def _oste_line_creation(self, quotation_record):
        quotation_record.update({
                    "ship_term_id" : self.ship_term_id.id,
                    "switch_bl_req" : self.switch_bl_req,
                    "pol_port_id" : self.pol_port_id.id,
                    "pol_free_days" : self.pol_free_days,
                    "pod_port_id" : self.pod_port_id.id,
                    "pod_free_days" : self.pod_free_days,
                    "trip_pickup_depot_id" : self.trip_pickup_depot_id.id,
                    "dest_address" : self.dest_address,
                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                      
                 })
        oste_draft_quotations = self.env['ct.quotations'].create(quotation_record)
        oste_draft_quotations.load_carrier_price()
        oste_draft_quotations.additional_cost_creation(oste_draft_quotations.enquiry_no)
        oste_draft_quotations.onchange_poo_port_id()
        oste_draft_quotations.onchange_fpod_port_id()        
        return True  
    
    def _soce_line_creation(self, quotation_record):
        quotation_record.update({
                    "ship_term_id" : self.ship_term_id.id,
                    "switch_bl_req" : self.switch_bl_req,
                    "pol_port_id" : self.pol_port_id.id,
                    "pol_free_days" : self.pol_free_days,
                    "pod_port_id" : self.pod_port_id.id,
                    "pod_free_days" : self.pod_free_days,
                    "trip_pickup_depot_id" : self.trip_pickup_depot_id.id,
                    "carrier_id": self.carrier_id.id,
                    "insurance": self.insurance,
                    "tank_test_cert_ids": self.tank_test_cert_ids,
                    "tank_clean_cert_ids": self.tank_clean_cert_ids                                                                                                                                                                                                                                                                                           
                 })
        if not quotation_record['is_parent']:
            quotation_record['pol_port_id'] = self.pod_port_id.id
            quotation_record['pod_port_id'] = self.pol_port_id.id
            quotation_record['poo_port_id'] = self.pod_port_id.id
            quotation_record['fpod_port_id'] = self.pol_port_id.id            
        soce_draft_quotations = self.env['ct.quotations'].create(quotation_record) 
        soce_draft_quotations.load_carrier_price()  
        soce_draft_quotations.onchange_poo_port_id()
        soce_draft_quotations.onchange_fpod_port_id()      
        return True  
    
    def _osnr_line_creation(self, quotation_record):
        quotation_record.update({
                    "ship_term_id" : self.ship_term_id.id,
                    "switch_bl_req" : self.switch_bl_req,
                    "pol_port_id" : self.pol_port_id.id,
                    "pol_free_days" : self.pol_free_days,
                    "pod_port_id" : self.pod_port_id.id,
                    "pod_free_days" : self.pod_free_days,
                    "trip_pickup_depot_id" : self.trip_pickup_depot_id.id,
                    "carrier_id": self.carrier_id.id,
                    "insurance": self.insurance,
                    "tank_test_cert_ids": self.tank_test_cert_ids,
                    "tank_clean_cert_ids": self.tank_clean_cert_ids                                                                                                                                                                                                                                                                                            
                 })
        osnr_draft_quotations = self.env['ct.quotations'].create(quotation_record)
        osnr_draft_quotations.load_carrier_price()

         
        return True      
    
    def _dots_line_creation(self, quotation_record):
        quotation_record.update({
                    "tank_type" : self.tank_type,
                    "tank_sale_qty" : self.tank_sale_qty,
                    "tank_sale_product_id" : self.tank_sale_product_id.id,
                    "tank_sale_dg_product" : self.tank_sale_dg_product,
                    "tank_sale_product" : self.tank_sale_product,                                                                                                                                                                                                                                                                                           
                 })
        dots_draft = self.env['ct.quotations'].create(quotation_record)
        tanks = self.env['cm.tank.master'].search([('depot_id', 'in', [depot.id for depot in self.depot_ids]), ('age', '>', 25)])
        if tanks:
           dots_draft.line_ids_t = [(0, 0,{"tank_no_id": tank.id}) for tank in tanks]
        return True              

    def _dotr_line_creation(self, quotation_record):
        tank_lease_tariff = self.env['cm.tank.lease.tariff'].search([('business_location','=', self.bus_location),\
                  ('status', '=', 'active'),('active_trans', '=', True)], limit=1, order='eff_from_date desc')
        free_hrs_day = 1
        quotation_record.update({
                    "gr_dep_id" : self.gr_dep_id.id,
                    "prod_weight_kg" : self.prod_weight_kg,
                    "trailer_type" : self.trailer_type,
                    "free_hrs" : self.free_hrs,
                    "trans_route_id" : self.trans_route_id.id,
                    "from_trans_loc_id" : self.from_trans_loc_id.id,
                    "from_city_id" : self.from_city_id.id,
                    "from_state_id" : self.from_state_id.id,
                    "to_trans_loc_id" : self.to_trans_loc_id.id,
                    "to_city_id" : self.to_city_id.id,
                    "to_state_id" : self.to_state_id.id,
                    "empty_pickup_loc_id" : self.empty_pickup_loc_id.id,
                    "load_address" : self.load_address,
                    "load_zip_code" : self.load_zip_code,
                    "unload_address" : self.unload_address,
                    "unload_zip_code" : self.unload_zip_code,
                    "trip_start_date" : self.trip_start_date, 
                    "trip_pickup_depot_id" : self.trip_pickup_depot_id.id,
                    "empty_offload_loc_id": self.empty_offload_loc_id.id,
                    "trans_pickup_depot_id": self.trans_pickup_depot_id.id,
                    "tot_trip":  self.trans_route_id.total_trip, 
                    "tot_transit_days": self.trans_route_id.trip_days + self.dotr_pol_free_days + \
            self.dotr_pod_free_days + tank_lease_tariff.re_use_days + free_hrs_day,
                    "dotr_pod_free_days" : self.dotr_pod_free_days,
                    "dotr_pol_free_days" : self.dotr_pol_free_days,
                    "avg_mileage": self.env['cm.transport.tariff'].search([('status', '=', 'active'),('active_trans', '=', True)], limit=1, order='eff_from_date desc').avg_mileage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                 })
        
        self.env['ct.quotations'].create(quotation_record)
        return True
    
    def _dott_line_creation(self, quotation_record):
        quotation_record.update({
                    "ship_term_id" : self.ship_term_id.id,
                    "gr_dep_id" : self.gr_dep_id.id,
                    "prod_weight_kg" : self.prod_weight_kg,
                    "trailer_type" : self.trailer_type,
                    "free_hrs" : self.free_hrs,
                    "trans_route_id" : self.trans_route_id.id,
                    "from_trans_loc_id" : self.from_trans_loc_id.id,
                    "from_city_id" : self.from_city_id.id,
                    "from_state_id" : self.from_state_id.id,
                    "to_trans_loc_id" : self.to_trans_loc_id.id,
                    "to_city_id" : self.to_city_id.id,
                    "to_state_id" : self.to_state_id.id,
                    "empty_pickup_loc_id" : self.empty_pickup_loc_id.id,
                    "load_address" : self.load_address,
                    "load_zip_code" : self.load_zip_code,
                    "unload_address" : self.unload_address,
                    "unload_zip_code" : self.unload_zip_code,
                    "trip_start_date" : self.trip_start_date,
                    "empty_offload_loc_id": self.empty_offload_loc_id.id,
                    "trans_pickup_depot_id": self.trans_pickup_depot_id.id,                    
                    "bus_location": self.bus_location,
                    "end_gr_dep_id" : self.end_gr_dep_id.id,
                    "end_prod_weight_kg" : self.end_prod_weight_kg,
                    "end_trailer_type" : self.end_trailer_type,
                    "end_free_hrs" : self.end_free_hrs,
                    "end_trans_route_id" : self.end_trans_route_id.id,
                    "end_from_trans_loc_id" : self.end_from_trans_loc_id.id,
                    "end_from_city_id" : self.end_from_city_id.id,
                    "end_from_state_id" : self.end_from_state_id.id,
                    "end_to_trans_loc_id" : self.end_to_trans_loc_id.id,
                    "end_to_city_id" : self.end_to_city_id.id,
                    "end_to_state_id" : self.end_to_state_id.id,
                    "end_empty_pickup_loc_id" : self.end_empty_pickup_loc_id.id,
                    "end_load_address" : self.end_load_address,
                    "end_load_zip_code" : self.end_load_zip_code,
                    "end_unload_address" : self.end_unload_address,
                    "end_unload_zip_code" : self.end_unload_zip_code,
                    "end_trip_start_date" : self.end_trip_start_date,
                    "end_empty_offload_loc_id": self.end_empty_offload_loc_id.id,
                    "end_trans_pickup_depot_id": self.end_trans_pickup_depot_id.id,
                    "dotr_pol_free_days" : self.dotr_pol_free_days,
                    "dotr_pod_free_days" : self.dotr_pod_free_days,
                    "end_dotr_pol_free_days" : self.end_dotr_pol_free_days,                  
                    "end_dotr_pod_free_days" : self.end_dotr_pod_free_days                                                                                                                                                                                                                                                                                                                                                                                                                       
                 })
        if 'DOTT' in self.combined_codes:
            quotation_record.update({                           
                    "rail_pol_port_id" : self.rail_pol_port_id.id,
                    "rail_pol_free_days" : self.rail_pol_free_days,
                    "rail_pod_port_id" : self.rail_pod_port_id.id,
                    "rail_pod_free_days" : self.rail_pod_free_days})
        if 'DOTC' in self.combined_codes:
            quotation_record.update({            
                    "coastal_pol_port_id" : self.coastal_pol_port_id.id,
                    "coastal_pol_free_days" : self.coastal_pol_free_days,
                    "coastal_pod_port_id" : self.coastal_pod_port_id.id,
                    "coastal_pod_free_days" : self.coastal_pod_free_days})            
        quotation_draft = self.env['ct.quotations'].create(quotation_record)   
        quotation_draft._compute_entry_category()    
        return True

    def create_quotations(self):
        def safe_get_id(field):
            return field.id if field else False

        quotation_record = {
            "enquiry_no": self.name,
            "enquiry_date": self.entry_date,
            "service_id": safe_get_id(self.service_id),
            "enq_source_id": safe_get_id(self.enq_source_id),
            "ref_no": self.ref_no,
            "bkg_party_id": safe_get_id(self.bkg_party_id),
            "new_bkg_party": self.new_bkg_party,
            "shipper_cus_id": safe_get_id(self.shipper_cus_id),
            "new_shipper": self.new_shipper,
            "rebate": self.rebate,
            "cust_rate": self.cust_rate,
            "currency_id": safe_get_id(self.currency_id),
            "expiry_date": self.expiry_date,
            "product_id": safe_get_id(self.product_id),
            "product": self.product,
            "dg_product": self.dg_product,
            "cleaning_status": self.cleaning_status,
            "un_no": self.un_no,
            "imo_class": self.imo_class,
            "sub_class1": self.sub_class1,
            "sub_class2": self.sub_class2,
            "pack_grp": self.pack_grp,
            "mar_poll" : self.mar_poll,
            "tank_tcode_id": self.tank_tcode_id.id,
            "tank_capacity": self.tank_capacity,
            "tank_qty": self.tank_qty,
            "container_category": self.container_category,
            "service_ids": [(6, 0, [service_id.id for service_id in self.service_ids])] if self.service_ids else False,
            "spl_req": self.spl_req,
            "generated_user_id": safe_get_id(self.generated_user_id),
            "executed_user_id": safe_get_id(self.executed_user_id),
            "bus_location": self.bus_location,
            "bus_vert_id": safe_get_id(self.bus_vert_id),
            "entry_mode": "auto",
            "contact_person": self.contact_person,
            "mobile_no": self.mobile_no,
            "email": self.email,
            "quotation_currency_id": self.env['res.currency'].search([('status', '=', 'active'),('active_trans', '=', True),\
                ('short_name', '=', 'INR')], limit=1).id if self.bus_location == 'pan_india' else False,
            "line_ids_a": [(0, 0, {
                "attach_desc": att_line.attach_desc,
                "attachment_ids": [(6, 0, [att.id for att in att_line.attachment_ids])],
                "attach_user_id": att_line.attach_user_id.id,
                "attach_date": att_line.attach_date
                }) for att_line in self.line_ids_a], 
            "del_address": self.del_address,
            "city_id": self.city_id.id,
            "sds_status" : self.sds_status,
            "mfg_id" : self.mfg_id.id,
            "poo_port_id": self.poo_port_id.id,
            "fpod_port_id": self.fpod_port_id.id,
            "payment_centre_port_id": self.payment_centre_port_id.id,
            "lead_no": self.sales_lead_id.name if self.sales_lead_id else None,
            "sds_status": self.sds_status,
            "sds_attach_ids": self.sds_attach_ids,
            "payment_term_id": self.service_id.payment_term_id.id,
            "src_address": self.src_address,
            "dest_address": self.dest_address,
            "tank_detention_rate": self.pol_detention,
            "tank_detention_currency_id" : self.pol_pod_currency_id.id,
            "project_name": self.project_name,
            "tank_detention_rate_pod": self.pod_detention,  
            "ind_slot_rate": self.ind_slot_rate,
            "ind_slot_currency_id": self.ind_slot_currency_id.id,
            "nomination_port_id": self.nomination_port_id.id,
            "pol_terminal_id": self.pol_terminal_id.id,
            "pod_terminal_id": self.pod_terminal_id.id,
            "coastal_pol_terminal_id": self.coastal_pol_terminal_id.id,            
            "coastal_pod_terminal_id": self.coastal_pod_terminal_id.id,
            
        }
        
        def create_teams_conditions(quotation_service_id, quotation_service_ids):
            teams_line = []
            if quotation_service_id:
                teams_line = teams_line + self.env['ct.quotations'].create_teams_and_conditions_line(quotation_service_id)
            if  quotation_service_ids:
                for service_id in quotation_service_ids:
                    teams_line = teams_line + self.env['ct.quotations'].create_teams_and_conditions_line(service_id.id)
            quotation_record['line_ids_k'] = teams_line
            
        service_object = self.env[CM_SERVICE]
        if 'ISTL' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'ISTL')], limit=1).id
            if self.service_ids:
                quotation_record["is_parent"] = True if self.service_id.sys_ref == 'ISTL' else False
            quotation_record['combined_codes'] = "['ISTL']"
            quotation_record["estimated_days"] = self.env['ct.quotations'].days_conversion(self.period_choices, self.lease_period)  
            create_teams_conditions(quotation_record["service_id"], self.service_ids) 
            quotation_record['price_owner'] = 'agent'   
            self._istl_line_creation(quotation_record)
        if 'DOTL' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'DOTL')], limit=1).id
            if self.service_ids:           
                quotation_record["is_parent"] = True if self.service_id.sys_ref == 'DOTL' else False            
            quotation_record['combined_codes'] = "['DOTL']"
            quotation_record["is_parent"] = True
            quotation_record["estimated_days"] = self.env['ct.quotations'].days_conversion(self.period_choices, self.lease_period)  
            create_teams_conditions(quotation_record["service_id"], self.service_ids) 
            self._istl_line_creation(quotation_record)         
        if 'FLBS' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'FLBS')], limit=1).id
            if self.service_ids:
                quotation_record["is_parent"] = True if self.service_id.sys_ref == 'FLBS' else False             
            quotation_record['combined_codes'] = "['FLBS']" 
            quotation_record["is_parent"] = True 
            create_teams_conditions(quotation_record["service_id"], self.service_ids)                       
            self._flbs_line_creation(quotation_record) 
        if 'FLAS' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'FLAS')], limit=1).id
            if self.service_ids:            
                quotation_record["is_parent"] = True if self.service_id.sys_ref == 'FLAS' else False              
            quotation_record['combined_codes'] = "['FLAS']"  
            quotation_record["is_parent"] = True          
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._flas_line_creation(quotation_record)  
        if 'FLOS' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'FLOS')], limit=1).id
            if self.service_ids:            
                quotation_record["is_parent"] = True if self.service_id.sys_ref == 'FLOS' else False              
            quotation_record['combined_codes'] = "['FLOS']"
            quotation_record["is_parent"] = True
            create_teams_conditions(quotation_record["service_id"], self.service_ids)                       
            self._flos_line_creation(quotation_record)
        if 'TRAN' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'TRAN')], limit=1).id
            if self.service_ids:            
                quotation_record["is_parent"] = True if self.service_id.sys_ref == 'TRAN' else False               
            quotation_record['combined_codes'] = "['TRAN']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._trans_line_creation(quotation_record)
        if 'OSTE' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'OSTE')], limit=1).id
            quotation_record['combined_codes'] = "['OSTE']"
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'OSTE' else False            
            quotation_record['price_owner'] = "agent"
            create_teams_conditions(quotation_record["service_id"], self.service_ids) 
            self._oste_line_creation(quotation_record)            
            if self.tank_operator_id and [tank_operator for tank_operator in self.tank_operator_id if tank_operator.short_name == 'GSCS']:                        
                quotation_record['price_owner'] = "operator"
                quotation_record["is_parent"] = False                        
                quotation_record['combined_codes'] = "['OSTE']"
                quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                        'pod_port_id': self.pod_port_id.id})
                create_teams_conditions(quotation_record["service_id"], self.service_ids)             
                self._oste_line_creation(quotation_record)
        if 'OSTI' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'OSTI')], limit=1).id
            quotation_record['combined_codes'] = "['OSTI']"
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'OSTI' else False            
            quotation_record['price_owner'] = "agent"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._oste_line_creation(quotation_record)
            if self.tank_operator_id and [tank_operator for tank_operator in self.tank_operator_id if tank_operator.short_name == 'GSCS']:
                quotation_record['price_owner'] = "operator"
                quotation_record["is_parent"] = False                        
                quotation_record['combined_codes'] = "['OSTI']"
                quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                        'pod_port_id': self.pod_port_id.id})
                create_teams_conditions(quotation_record["service_id"], self.service_ids)             
                self._oste_line_creation(quotation_record)            
        if 'DOTR' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'DOTR')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'DOTR' else False               
            quotation_record['combined_codes'] = "['DOTR']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._dotr_line_creation(quotation_record)
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'TRAN')], limit=1).id            
            quotation_record["is_parent"] = False               
            quotation_record['combined_codes'] = "['TRAN']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._dotr_line_creation(quotation_record)      
        if 'SOCE' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'SOCE')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'SOCE' else False             
            quotation_record['combined_codes'] = "['SOCE']"
            quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                     'pod_port_id': self.pod_port_id.id}) 
            create_teams_conditions(quotation_record["service_id"], self.service_ids)                       
            self._soce_line_creation(quotation_record)
        if 'DOTT' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'DOTT')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'DOTT' else False 
            quotation_record['combined_codes'] = "['DOTT']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._dott_line_creation(quotation_record)
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'TRAN')], limit=1).id           
            quotation_record["is_parent"] = False               
            quotation_record['combined_codes'] = "['TRAN']"
            if 'DOCY' == self.ship_term_id.sys_ref or 'CYDO' == self.ship_term_id.sys_ref or 'DRDR' == self.ship_term_id.sys_ref:
                create_teams_conditions(quotation_record["service_id"], self.service_ids) 
                quotation_record['dotr_pol_free_days'] = self.dotr_pol_free_days
                quotation_record['dotr_pod_free_days'] = self.dotr_pod_free_days       
                self._trans_line_creation(quotation_record)
                if self.ship_term_id.sys_ref == 'DRDR':
                    quotation_record["is_parent"] = False               
                    quotation_record['combined_codes'] = "['TRAN']"
                    create_teams_conditions(quotation_record["service_id"], self.service_ids) 
                    quotation_record['dotr_pol_free_days'] = self.end_dotr_pol_free_days
                    quotation_record['dotr_pod_free_days'] = self.end_dotr_pod_free_days                     
                    self._trans_line_creation(quotation_record, 'DRDR') 
        if 'DOTC' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'DOTC')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'DOTC' else False 
            quotation_record['combined_codes'] = "['DOTC']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._dott_line_creation(quotation_record)
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'TRAN')], limit=1).id           
            quotation_record["is_parent"] = False        
            quotation_record['combined_codes'] = "['TRAN']"
            if 'DOCY' == self.ship_term_id.sys_ref or 'CYDO' == self.ship_term_id.sys_ref or 'DRDR' == self.ship_term_id.sys_ref:
                create_teams_conditions(quotation_record["service_id"], self.service_ids)
                quotation_record['dotr_pol_free_days'] = self.dotr_pol_free_days
                quotation_record['dotr_pod_free_days'] = self.dotr_pod_free_days                                  
                self._trans_line_creation(quotation_record)
                if self.ship_term_id.sys_ref == 'DRDR':
                    quotation_record["is_parent"] = False               
                    quotation_record['combined_codes'] = "['TRAN']"
                    create_teams_conditions(quotation_record["service_id"], self.service_ids)
                    quotation_record['dotr_pol_free_days'] = self.end_dotr_pol_free_days
                    quotation_record['dotr_pod_free_days'] = self.end_dotr_pod_free_days                                         
                    self._trans_line_creation(quotation_record, 'DRDR')
        if 'DOTS' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'DOTS')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'DOTS' else False             
            quotation_record['combined_codes'] = "['DOTS']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._dots_line_creation(quotation_record)   
        if 'OSNR' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'OSNR')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'OSNR' else False  
            quotation_record['price_owner'] = "agent"                       
            quotation_record['combined_codes'] = "['OSNR']"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._osnr_line_creation(quotation_record)  
            if self.tank_operator_id and [tank_operator for tank_operator in self.tank_operator_id if tank_operator.short_name == 'GSCS']:      
                quotation_record['price_owner'] = "operator"
                quotation_record["is_parent"] = False                        
                quotation_record['combined_codes'] = "['OSNR']"
                quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                        'pod_port_id': self.pod_port_id.id}) 
                create_teams_conditions(quotation_record["service_id"], self.service_ids)             
                self._osnr_line_creation(quotation_record)
        if 'SOCI' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'SOCI')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'SOCI' else False             
            quotation_record['combined_codes'] = "['SOCI']"
            quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                     'pod_port_id': self.pod_port_id.id})   
            create_teams_conditions(quotation_record["service_id"], self.service_ids)                  
            self._soce_line_creation(quotation_record)    
        if 'SOCR' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'SOCR')], limit=1).id
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'SOCR' else False             
            quotation_record['combined_codes'] = "['SOCR']"
            quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                     'pod_port_id': self.pod_port_id.id})
            create_teams_conditions(quotation_record["service_id"], self.service_ids)                
            self._soce_line_creation(quotation_record)                                                                                                           
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'SOCI')], limit=1).id
            quotation_record["is_parent"] =  False                  
            quotation_record['combined_codes'] = "['SOCI']"
            quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pod_port_id.id,
                                                                                                     'pod_port_id': self.pol_port_id.id})
            create_teams_conditions(quotation_record["service_id"], self.service_ids)                      
            self._soce_line_creation(quotation_record)  
        if 'OSNB' in self.combined_codes:
            quotation_record["service_id"] = service_object.search([('status', '=', 'active'),('active_trans', '=', True),\
                ('sys_ref', '=', 'OSNB')], limit=1).id
            quotation_record['combined_codes'] = "['OSNB']"
            quotation_record["is_parent"] = True if self.service_id.sys_ref == 'OSNB' else False            
            quotation_record['price_owner'] = "agent"
            create_teams_conditions(quotation_record["service_id"], self.service_ids)             
            self._oste_line_creation(quotation_record)
            if self.tank_operator_id and [tank_operator for tank_operator in self.tank_operator_id if tank_operator.short_name == 'GSCS']:
                quotation_record['price_owner'] = "operator"
                quotation_record["is_parent"] = False                        
                quotation_record['combined_codes'] = "['OSNB']"
                quotation_record['line_ids_m'] = self.env['ct.quotations'].create_route_suggestion_line({'pol_port_id': self.pol_port_id.id,
                                                                                                        'pod_port_id': self.pod_port_id.id})
                create_teams_conditions(quotation_record["service_id"], self.service_ids)             
                self._oste_line_creation(quotation_record)                                                                                                        
        return True   

    @api.model
    def retrieve_dashboard(self):
        result = {
            'all_draft': 0,
            'all_rfq_sent': 0,
            'all_quotation_sent': 0,
            'all_won': 0,
            'all_lost': 0,
            'all_cancelled':0,
            'my_draft': 0,
            'my_rfq_sent': 0,
            'my_quotation_sent': 0,
            'my_won': 0,
            'my_lost': 0,
            'my_cancelled':0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0
        }

        enquiry = self.env[CT_ENQUIRY]
        result['all_draft'] = enquiry.search_count([('status', '=', 'draft')])
        result['all_rfq_sent'] = enquiry.search_count([('status', '=', 'rfq_sent')])
        result['all_quotation_sent'] = enquiry.search_count([('status', '=', 'quotation_sent')])
        result['all_won'] = enquiry.search_count([('status', '=', 'won')])
        result['all_lost'] = enquiry.search_count([('status', '=', 'lost')])
        result['all_cancelled'] = enquiry.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = enquiry.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_rfq_sent'] = enquiry.search_count([('status', '=', 'rfq_sent'), ('user_id', '=', self.env.uid)])
        result['my_quotation_sent'] = enquiry.search_count([('status', '=', 'quotation_sent'), ('user_id', '=', self.env.uid)])
        result['my_won'] = enquiry.search_count([('status', '=', 'won'), ('user_id', '=', self.env.uid)])
        result['my_lost'] = enquiry.search_count([('status', '=', 'lost'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = enquiry.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = enquiry.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = enquiry.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = enquiry.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = enquiry.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
