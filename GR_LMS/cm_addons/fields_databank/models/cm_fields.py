# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api
from odoo.addons.custom_properties.decorators import validation

RES_USERS = 'res.users'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'
RES_CURRENCY = 'res.currency'
CM_VENDOR_TYPE = 'cm.vendor.type'
CM_CUSTOMER = 'cm.customer'
CM_EMPLOYEE = 'cm.employee'
RES_PARTNER = 'res.partner'
CM_PORT = 'cm.port'
ACCOUNT_TAX = 'account.tax'
IR_ATTACHMENT= 'ir.attachment'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('closed', 'Closed'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

PAY_MODE_OPTIONS = [('bank', 'Bank'),
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('neft_rtgs', 'NEFT/RTGS'),
            ('others', 'Others')]

TRANS_STATUS = [('direct', 'Direct'),
                ('from_po', 'From PO')]

ENTRY_MODE =  [('manual', 'Manual'),
               ('auto', 'Auto')]

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

MAIL_SMS_STATUS = [('pending', 'Pending'),
                   ('sent', 'Sent'),
                   ('re_sent', 'Re-Send'),('not_applicable', 'Not Applicable')]

JC_STATUS = [('applicable', 'Applicable'),
             ('not_applicable', 'Not Applicable'),
             ('jc_open', 'JC Open'),
             ('jc_closed', 'JC Closed')]

YEARS = [('fiscal_year', 'Fiscal Year'),
         ('calendar_year','Calendar Year')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

GST_OPTIONS = [('registered', 'Registered'), ('un_registered', 'Un Registered')]

GRADE_OPTIONS = [('a', 'A'), ('b', 'B'), ('c', 'C')]

RATING_OPTIONS = [('0','0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]

FORMAT_TYPE_OPTIONS = [('excel', 'Excel'),('pdf', 'PDF')]

CONTRACT_TYPE = [('own', 'Own'), ('lease', 'Lease'), ('rent', 'Rent')]

CONTAINER_TYPE = [('tank_only', 'Tank Only'), ('dry', 'Dry'), ('all', 'All')]

CONTAINER_SIZE = [('20_teu', '20 TEU'), ('40_teu', '40 TEU'), ('both', 'Both')]

PAVER_BLOCKED = [('full', 'Full'), ('partially', 'partially')]

MAINTENANCE_CONTRACT = [('no_contract', 'No Contract'), ('active', 'Active'), ('expired', 'Expired')]

PORT_TYPE = [('seaport', 'Seaport'), ('airport', 'Airport'), ('dry_port', 'Dry(ICD) Port')]

LOCATION = [('pan_india', 'PAN India'), ('exim', 'Exim')]

CHARGES_CATEGORY = [('container_basis', 'Container Basis')]

FLEXI_TYPE = [('tltd', 'TLTD (Top Loading Top Discharge)'), ('tlbd', 'TLBD (Top Loading Botton Discharge)'), ('blbd', 'BLBD (Bottom Load Bottom Discharge)')]

LAYER_TYPE = [('3_layer', '3 Layer'), ('4_layer', '4 Layer'), ('5_layer', '5 Layer')]

CAPACITY = [('16kl', '16KL'), ('18kl', '18KL'), ('20kl', '20KL'), ('22kl', '22KL'), ('24kl', '24KL')]

VALVE_TYPE = [('3_butterfly', '3"" Butterfly'), ('3_ball_valve', '3"" Ball valve'), ('both', 'Both')]

BAG_COSTING_METHOD = [('with_accessories', 'With Accessories'), ('without_accessories', 'Without Accessories')]

MOC = [('pp', 'PP(Polypropylene)'), ('pe', 'PE(Polyethylene)')]

INTEREST_CAL = [('from_invoice_date', 'From Invoice Date'), (' from_due_date', ' From Due Date')]

SUB_TYPE = [('liquid', 'Liquid'), ('gas', 'Gas'), ('cryogenic', 'Cryogenic')]

TANK_T_CODE = [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'), ('t4', 'T4'), ('t5', 'T5'), ('t6', 'T6'), ('t7', 'T7'), ('t8', 'T8'), 
     ('t9', 'T9'), ('t10', 'T10'), ('t11', 'T11'), ('t12', 'T12'), ('t13', 'T13'), ('t14', 'T14'), ('t15', 'T15'), 
     ('t16', 'T16'), ('t17', 'T17'), ('t18', 'T18'), ('t19', 'T19'), ('t20', 'T20'), ('t21', 'T21'), ('t22', 'T22'), 
     ('t23', 'T23'), ('t50', 'T50'), ('t75', 'T75')]

SUB_TYPE2 = [('swap_body', 'Swap Body'), ('buffle', 'Buffle'), ('foodgrade', 'Foodgrade'), ('industrial', 'Industrial')]

PORT_CATEGORY = [('seaport', 'Seaport'), ('airport', 'Airport'), ('dry_port', 'Dry(ICD) port')]
    
AGENT_TYPE = [('internal', 'Internal'), ('external', 'External'), ('no_agent', 'No Agent')]

BOUND_OPTIONS = [('east', 'East'), ('west', 'West')]

SERVICE_AVAILABILITY_OPTION = [('all_days','All Days'),
    ('specific_days','Specific Days'),
    ('weekly','Weekly'),('monthly','Monthly'),
    ('weekly_twice','Weekly Twice'),('daily', 'Daily'),
    ('weekdays_only','Weekdays Only(Monday-Friday)'),
    ('weekends_only','Weekends Only')]

VESSEL_SERVICE_PROVIDERS = [('feeder', 'Feeder'), ('mlo', 'MLO'),
    ('costal', 'Costal'), ('all', 'All')]

VESSEL_TYPE = [('container_vessels','Container Vessels'),
    ('bulk_carriers', 'Bulk Carriers'),
    ('tankers', 'Tankers'),
    ('ro_ro_vessels', 'Ro-Ro Vessels(Roll-on/Roll-off)'),
    ('general_cargo_vessels', 'General Cargo Vessels')]   

TERMINAL_TYPE = [('container_terminal','Container Terminal'),
    ('break_bulk_terminals','Break-Bulk Terminals'),
    ('neo_bulk_terminals', 'Neo-Bulk Terminals'),
    ('oil_terminal', 'Oil Terminal')]

RESTRICTED_CATEGORY = [('tank_operator','Tank Operator'),
    ('carrier', 'Carrier'),
    ('port', 'Port'),
    ('others', 'Others')]

SERVICE_PROVIDER = [('internal_team','Internal Team'),
    ('external_vendor', 'External Vendor')]

MANDATORY = [('yes','Yes'), ('no', 'No'), ('term', 'Term')]

IMPORT_EXPORT =  [('import','Import'), ('export', 'Export'), ('both', 'Both')]

CONTAINER_CATEGORY = [('laden','Laden'), ('empty', 'Empty')]

CARGO_CATEGORY =  [('dg','DG'), ('non_dg', 'Non DG'),
                    ('shutout', 'Shutout'), ('shutout_dg', 'Shutout DG')]

ENTRY_TYPE = [('new','New'), ('name_change', 'Name Change')]

VALIDITY_RANGE = [('perpetual', 'Perpetual'), ('limited', 'Limited')]

LICENSE_TYPE = [('lmv_tr', 'LMV-TR'),
                ('hmv_tr', 'HMV-TR'),
                ('both', 'Both')]

OFFICIAL_DOC_OPTIONS = [('visible', 'Visible'),
                        ('not_visible', 'Not Visible')]

COMPANY_TYPE =  [('proprietary','Proprietary'),
                           ('partnership', 'Partnership'),
                           ('private', 'Private'),
                           ('public', 'Public Limited')]

BUSINESS_CATEGORY =  [('entry_level','Entry Level'),
                           ('silver', 'Silver'),
                           ('gold', 'Gold'),
                           ('platinum', 'Platinum'),
                           ('diamond', 'Diamond')]

BUSINESS_GRADE =  [('no_risk','No Risk'),
                           ('low_risk', 'Low Risk'),
                           ('medium_risk', 'Medium Risk'),
                           ('high_risk', 'High Risk')]

BUSINESS_SEGMENTS =  [('increased','Increased'),
                           ('steep_fall', 'Steep Fall'),
                           ('averaged_out', 'Averaged Out'),
                           ('dormant', 'Dormant')]

PAYMENT_TYPE = [('cash', 'Cash'), ('credit', 'Credit')]

AGENT_CATEGORY = [('external', 'External'), ('internal', 'Internal')]

PROVIDING_SERVICES =  [('transportation','Transportation'),
                           ('warehousing', 'Warehousing'),
                           ('custom_clearance', 'Customs Clearance'),
                           ('shipment', 'Shipment')]

DAY = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')]

FUEL_TYPE_OPTION = [('diesel', 'Diesel'), ('petrol', 'Petrol'), ('gasoline', 'Gasoline'), ('electric', 'Electric')]

TRANSMISSION_OPTION = [('auto', 'Auto'), ('manual', 'Manual'), ('both', 'Both')]

AXLE_OPTION = [('single', 'Single'), ('multi', 'Multi'), ('double', 'Double'), ('Trible', 'Trible')]

VALIDITY_OPTION = [('perpetual','Perpetual'), ('limited','Limited')]

STAGE_OPTIONS = [('enquiry', 'Enquiry'), ('quotation', 'Quotation')]

CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('costal', 'Costal'), ('all', 'All')]

FREQUENCY_OF_SAILING_OPTION = [('weekly', 'Weekly'), ('bi_weekly', 'Bi-Weekly'), ('monthly', 'Monthly'), ('etc', 'etc.')]

LEVEL_OF_SERVICE_PROVIDER_OPTION = [('1pl', '1PL'), ('2pl', '2PL'), ('3pl', '3PL'), ('4pl', '4PL'), ('5pl', '5PL')]

DIGITAL_SERVICE_NAME_OPTION = [('mobile_app', 'Mobile App')]

TRAVEL_TYPE_OPTION = [('empty', 'Empty'), ('laden', 'Laden')]

TYPE_OF_COMPANY_OPTION = [('private_Ltd', 'Private Ltd'),('public_ltd', 'Public Ltd')]

FEEDBACK_TYPE_OPTION = [('legals', 'Legals'),('transportation_cost', 'Transportation Cost'),
                        ('service_performance', 'Service Performance'), ('reliability', 'Reliability'),
                        ('accessibility', 'Accessibility'), ('capability', 'Capability'),
                        ('security', 'security'), ('past_incident', 'Past Incident')]

RELATIONSHIP_TYPE = [('mother', 'Mother'), ('father', 'Father'),
                     ('brother', 'Brother'), ('sister', 'Sister'),
                     ('wife', 'Wife'), ('son', 'Son'), ('guardian', 'Guardian')]






class FieldsDatabank(models.TransientModel):
    _name = 'fields.databank'
    _description = 'Fields Databank'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    #Char
    name = fields.Char(string="Name", readonly=True, index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    quote_ref = fields.Char(string="Quotation Ref", copy=False, size=15, tracking=True)
    address = fields.Char(string="Address", size=252)
    del_address = fields.Char(string="Delivery Address", size=252)
    entry_spec = fields.Char(string="Specification")
    mobile_no = fields.Char(string="Mobile No", size=15)
    mobile_no1 = fields.Char(string="Mobile No 1", size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12)
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    vendor_inv_no = fields.Char(string="Supplier / Vendor Invoice No", copy=False, size=15, tracking=True)
    ref_no = fields.Char(string="Customer Reference", copy=False, size=15, tracking=True)
    draft_name = fields.Char(string="Draft No", copy=False, index=True, readonly=True, size=30)
    ack_no = fields.Char(string="Acknowledgement No", copy=False, size=15, tracking=True)	
    cheque_favor = fields.Char(string="Cheque In Favor Of", copy=False, size=252, tracking=True)	
    tin_no = fields.Char(string="TIN No", copy=False, size=18)
    pan_no = fields.Char(string="PAN No", copy=False, size=10)	
    cst_no = fields.Char(string="CST No", copy=False, size=20)
    vat_no = fields.Char(string="VAT No", copy=False, size=20)
    purpose = fields.Char(string="Purpose", copy=False, side=252)
    description = fields.Char(string="Description", size=252)
    attach_desc = fields.Char(string="Description", size=252)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    invoice_status = fields.Char(string="Invoice Status", copy=False, default="Pending",readonly=True, size=15)
    payment_status = fields.Char(string="Payment Status", copy=False, default="Pending", readonly=True, size=15)
    contact_person = fields.Char(string="Contact Person", size=50)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    website = fields.Char(string="Website", copy=False, size=100)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    tan_no = fields.Char(string="TAN", size=20)
    aadhaar_no = fields.Char(string="Aadhaar No", copy=False, size=12, tracking=True)
    account_no = fields.Char(string="Account No", copy=False, size=20, tracking=True)
    landmark = fields.Char(string="Landmark", size=252)
    state_code = fields.Char(string="State Code", copy=False, readonly=True, size=252)
    acc_holder_name = fields.Char(string="Account Holder Name", copy=False, size=252)
    alias_name = fields.Char(string="Alias Name", copy=False, size=252)
    bank_name = fields.Char(string="Bank Name", copy=False, size=252)
    ifsc_code = fields.Char(string="IFSC Code", copy=False, size=11)
    branch_name = fields.Char(string="Branch Name", copy=False, size=252)
    cin_no = fields.Char(string="CIN No", copy=False, size=21)
    tax_name = fields.Char(string="Tax Name", copy=False, size=252)
    serial_no = fields.Char(string="Serial No", copy=False, size=252)
    mail_from = fields.Char(string="From", copy=False, size=252)
    mail_to = fields.Char(string="To", copy=False, size=252)
    mail_cc = fields.Char(string="Cc", copy=False, size=252)
    mail_bcc = fields.Char(string="Bcc", copy=False, size=252)
    from_mail_id = fields.Char(string="From Email-ID", copy=False, size=252)
    subject = fields.Char(string="Subject", copy=False, size=252)
    watcher_mail_id = fields.Char(string="Watcher Mail ID", copy=False, size=252)
    ext_no = fields.Char(string="Ext No", copy=False, size=15)
    seq_month = fields.Char(string="Sequence Month", copy=False, size=252)
    seq_year = fields.Char(string="Sequence Year", copy=False, size=252)
    fiscal_year_code = fields.Char(string="Fiscal Year Code", copy=False, size=5)
    
    #Catalyst 
    iom_no = fields.Char(string="IMO Number", copy=False, size=7)
    other_facility = fields.Char(string="Other Facility", copy=False, size=252)
    continent = fields.Char(string="Continent", copy=False, size=252)
    usci_no= fields.Char(string="USCI No", copy=False, size=252)
    fmc_no = fields.Char(string="FMC No", copy=False, size=252)
    thickness = fields.Char(string="Thickness", copy=False, size=252)
    dry_box_type = fields.Char(string="Dry Box Type", default="20 Feet Heavy Duty", copy=False, size=252)
    owner_name = fields.Char(string="Original Owner Name", copy=False, size=252)
    container_no = fields.Char(string="Number", copy=False, size=252)
    iso_code = fields.Char(string="ISO Code", copy=False, size=252)
    working_day_hrs = fields.Char(string="Working Day / Hrs", copy=False, size=15)
    annual_turnover  = fields.Char(string="Annual Turnover", copy=False, size=50)
    iec_no = fields.Char(string="IEC No", copy=False, size=20)
    dpd = fields.Char(string="DPD", copy=False, size=20)
    dpd_cfs = fields.Char(string="DPD - CFS", copy=False, size=20)
    designation = fields.Char(string="Designation", copy=False, size=50)
    micr_no = fields.Char(string="MICR Number", copy=False, size=11)
    swift_code = fields.Char(string="Swift Code", copy=False, size=252)
    iban_no = fields.Char(string="IBAN Number", copy=False, size=11)
    work_location = fields.Char(string="Work Location", copy=False, size=50)
    exp_years = fields.Char(string="Industry Experience", copy=False, size=15)
    whatsapp_no = fields.Char(string="Whats App No",copy=False, size=15)
    secondary_mobile_no = fields.Char(string="Secondary Contact No",copy=False, size=15)
    occasion = fields.Char(string="Occasion", copy=False, size=252)
    term_name = fields.Char(string="Term Name", index=True, copy=False, side=252)
    engine_no = fields.Char(string="Engine No", copy=False, size=252)
    chassis_no = fields.Char(string="Chassis Number", copy=False, size=252)
    ins_company_name = fields.Char(string="Insurance Company Name", copy=False, size=252)
    trc_no = fields.Char(string="Tax Reg No(TRC)", copy=False, size=252)
    certification_no = fields.Char(string="Certification No", copy=False, size=15)
    edi_code = fields.Char(string="EDI Code", index=True, copy=False, size=252)
    skype = fields.Char(string="Skype ID", copy=False, size=50)
    dep_name = fields.Char(string="Department", copy=False, size=50)
    specific_days = fields.Char(string="Specific Days", copy=False, size=252)
    stage = fields.Char(string="Stage", index=True, copy=False, size=252)
    terminal_restrictions = fields.Char(string="Terminal Restrictions", copy=False, size=252)
    tax_reg_no = fields.Char(string="Tax Reg No(TRC)", copy=False, size=20)
    branch_code = fields.Char(string="Branch Code", copy=False, size=252)
    driver_lic_no = fields.Char(string="Driver License No", size=252)
    blood_group = fields.Char(string="Blood Group", size=252)
	
    #Selection
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    pay_mode = fields.Selection(selection=PAY_MODE_OPTIONS, string="Mode Of Payment", copy=False, tracking=True)
    grn_type = fields.Selection(selection=TRANS_STATUS, string="GRN Type", copy=False)
    entry_from = fields.Selection(selection=TRANS_STATUS, string="Entry From", copy=False, tracking=True)
    invoice_control = fields.Selection(selection=TRANS_STATUS, string="Invoice / Billing Status", copy=False)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    wages_type = fields.Selection(selection=TRANS_STATUS, string="Wages Type", copy=False)
    priority = fields.Selection(selection=TRANS_STATUS, string="Priority", tracking=True)
    warranty = fields.Selection(selection=APPLICABLE_OPTION, string="Warranty", copy=False, tracking=True)
    email_status = fields.Selection(selection=MAIL_SMS_STATUS, string="Email Status", copy=False)
    sms_status = fields.Selection(selection=MAIL_SMS_STATUS, string="SMS Status", copy=False)
    jc_status = fields.Selection(selection=JC_STATUS, string="Job Card Status", copy=False)
    seq_num_reset = fields.Selection(selection=YEARS, string="Sequence Number Reset")
    tds = fields.Selection(selection=YES_OR_NO, string="TDS Applicable", copy=False)
    gst_category = fields.Selection(selection=GST_OPTIONS, string="GST Category", copy=False)
    grade = fields.Selection(selection=GRADE_OPTIONS, string="Grade", copy=False)
    rating = fields.Selection(selection=RATING_OPTIONS, string="Rating", copy=False)
    format_type = fields.Selection(selection=FORMAT_TYPE_OPTIONS, string="Format Type", nolabel=True, widget='selection')
    
    #Catalyst
    transport_service = fields.Selection(selection=YES_OR_NO, string="Transport Service", copy=False)
    contract_type = fields.Selection(selection=CONTRACT_TYPE, string="Contract Type", copy=False)
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", copy=False)
    paver_blocked = fields.Selection(selection=PAVER_BLOCKED, string="Paver Blocked", copy=False)
    package_deal = fields.Selection(selection=APPLICABLE_OPTION, string="Package Deal", copy=False)
    surveillance_systems = fields.Selection(selection=YES_OR_NO, string="Surveillance Systems", copy=False)
    pub_transport_avl = fields.Selection(selection=YES_OR_NO, string="Public Transport Availability", copy=False)
    inv_track_sys = fields.Selection(selection=YES_OR_NO, string="Inventory Tracking System", copy=False)
    eva_procedure = fields.Selection(selection=YES_OR_NO, string="Evacuation Procedures", copy=False)
    waste_disp_procedure = fields.Selection(selection=YES_OR_NO, string="Waste Disposal Procedures", copy=False)
    steam_heat_fac = fields.Selection(selection=YES_OR_NO, string="Steam Heating Facility", copy=False)
    laden_storage_fac = fields.Selection(selection=YES_OR_NO, string="Laden Storage Facility", copy=False)
    degas_fac = fields.Selection(selection=YES_OR_NO, string="De-Gassing Facility", copy=False)
    halal_wash = fields.Selection(selection=YES_OR_NO, string="Halal Wash", copy=False)
    kosher_wash = fields.Selection(selection=YES_OR_NO, string="Kosher Wash", copy=False)
    emergency_plan = fields.Selection(selection=YES_OR_NO, string="Emergency Plan", copy=False)
    compt_cert = fields.Selection(selection=YES_OR_NO, string="Competence Certificate", copy=False)
    etp= fields.Selection(selection=YES_OR_NO, string="ETP( Effluent Treatment Plants )", copy=False)
    periodic_audit = fields.Selection(selection=APPLICABLE_OPTION, string="Periodic Audit", copy=False)
    port_type = fields.Selection(selection=PORT_TYPE, string="Port Type", copy=False)
    bus_location = fields.Selection(selection=LOCATION, string="Location", copy=False)
    charges_category = fields.Selection(selection=CHARGES_CATEGORY, string="Charges Category",copy=False, default='container_basis')
    flexi_type = fields.Selection(selection=FLEXI_TYPE, string="Flexi Type", copy=False)
    layer_type = fields.Selection(selection=LAYER_TYPE, string="Layer Type", copy=False)
    capacity = fields.Selection(selection=CAPACITY, string="Capacity(L)", copy=False)
    valve_type = fields.Selection(selection=VALVE_TYPE, string="Valve Type", copy=False)
    halal_certification = fields.Selection(selection=APPLICABLE_OPTION, string="Halal Certification", copy=False)
    bag_costing_method = fields.Selection(selection=BAG_COSTING_METHOD, string="Bag Costing Method", copy=False)
    moc_val= fields.Selection(selection=MOC, string="Material of Construction(MOC)", copy=False)
    dg_product = fields.Selection(selection=YES_OR_NO, string="Dangerous Goods" ,copy=False, default="no")
    pdc_waived = fields.Selection(selection=YES_OR_NO, string="PDC To Be Waived / Obtained", copy=False)
    security_chk_obt = fields.Selection(selection=YES_OR_NO, string="Security Cheque To Be Obtained / Waived", copy=False)
    cheque_bounced = fields.Selection(selection=YES_OR_NO, string="Has Party Cheque Bounced in Last 6 Months?", copy=False)
    credit_agreement = fields.Selection(selection=APPLICABLE_OPTION, string="Credit Agreement", copy=False)
    interest_cal_date = fields.Selection(selection=INTEREST_CAL, string="Interest Calculation Date", copy=False)
    auto_draft_inv = fields.Selection(selection=YES_OR_NO, string="Automate Draft Invoice", copy=False)
    profit_share = fields.Selection(selection=APPLICABLE_OPTION, string="Vendor Profit Sharing", copy=False)
    tank_t_code = fields.Selection(selection=TANK_T_CODE, string="Tank T Code", copy=False)
    sub_type = fields.Selection(selection=SUB_TYPE, string="Sub Type", copy=False)
    sub_type2 = fields.Selection(selection=SUB_TYPE2, string="Sub Type 2", copy=False)
    company_type = fields.Selection(selection=COMPANY_TYPE, string="Company Type", copy=False, tracking=True)
    sez_zone = fields.Selection(selection=YES_OR_NO, string="Comes Under SEZ", copy=False)
    business_category = fields.Selection(selection=BUSINESS_CATEGORY, string="Business Category", copy=False)
    business_grade = fields.Selection(selection=BUSINESS_GRADE, string="Business Grade", copy=False)
    business_segments = fields.Selection(selection=BUSINESS_SEGMENTS, string="Business Segments", copy=False)
    contract_customer = fields.Selection(selection=YES_OR_NO, string="Contract Customer", copy=False)
    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type", copy=False)
    agent_category = fields.Selection(selection=AGENT_CATEGORY, string="Agent Category", copy=False)
    providing_services = fields.Selection(selection=PROVIDING_SERVICES, string="Providing Services", copy=False) 
    past_legal_action = fields.Selection(selection=YES_OR_NO, string="Past Legal Actions", copy=False) #50
    week_day = fields.Selection(selection=DAY, string="Day", copy=False)
    visible_official_doc = fields.Selection(selection=OFFICIAL_DOC_OPTIONS, string="Visible In Official Document", copy=False, default="not_visible")
    fuel_type = fields.Selection(selection=FUEL_TYPE_OPTION, string="Fuel Type", copy=False)
    transmission = fields.Selection(selection=TRANSMISSION_OPTION, string="Transmission", copy=False)
    axle = fields.Selection(selection=AXLE_OPTION, string="Transmission", copy=False) 
    gps_enabled = fields.Selection(selection=YES_OR_NO, string="GPS Enabled", copy=False)
    first_aid_box = fields.Selection(selection=YES_OR_NO, string="First Aid Box", copy=False)
    driver_mon_sys = fields.Selection(selection=YES_OR_NO, string="Driver Monitoring System", copy=False)
    fire_ext = fields.Selection(selection=YES_OR_NO, string="Fire Extinguisher In Vehicle", copy=False)
    ppe_kit = fields.Selection(selection=YES_OR_NO, string="PPE Kits In Vehicle", copy=False)
    diesel_tk_saft_gurd = fields.Selection(selection=YES_OR_NO, string="Diesel Tank Safety Guard", copy=False)
    battery_saft_gurd = fields.Selection(selection=YES_OR_NO, string="Battery Safety Guard", copy=False)
    spill_kit = fields.Selection(selection=YES_OR_NO, string="Spill Kit", copy=False)
    mudguard = fields.Selection(selection=YES_OR_NO, string="Mudguard", copy=False)
    insurance = fields.Selection(selection=APPLICABLE_OPTION, string="Insurance", copy=False)
    permit = fields.Selection(selection=APPLICABLE_OPTION, string="Permit", copy=False)
    national_permit = fields.Selection(selection=APPLICABLE_OPTION, string="Permit", copy=False)
    fc = fields.Selection(selection=APPLICABLE_OPTION, string="FC", copy=False)
    road_tax = fields.Selection(selection=APPLICABLE_OPTION, string="Road Tax", copy=False) 
    puc = fields.Selection(selection=APPLICABLE_OPTION, string="PUC", copy=False)
    green_tax = fields.Selection(selection=APPLICABLE_OPTION, string="Green Tax", copy=False)
    speed_govener = fields.Selection(selection=APPLICABLE_OPTION, string="Speed Govener", copy=False)
    amc = fields.Selection(selection=APPLICABLE_OPTION, string="AMC", copy=False)
    validity = fields.Selection(selection=VALIDITY_OPTION, string="Validity", copy=False, tracking=True)
    process_name = fields.Selection(selection=STAGE_OPTIONS, string="Stage", copy=False)
    carrier_type = fields.Selection(selection=CARRIER_TYPE_OPTIONS, string="Carrier Type", copy=False)
    frequency_of_sailing = fields.Selection(selection=FREQUENCY_OF_SAILING_OPTION, string="Frequency Of Sailing", copy=False)
    service_prov_level = fields.Selection(selection=LEVEL_OF_SERVICE_PROVIDER_OPTION, string="Level Of Service Provider", copy=False)
    digital_service_name = fields.Selection(selection=DIGITAL_SERVICE_NAME_OPTION, string="Digital Service Name", copy=False)
    toll_plaza = fields.Selection(selection=APPLICABLE_OPTION, string="Toll Plaza", copy=False)
    travel_type = fields.Selection(selection=TRAVEL_TYPE_OPTION, string="Travel Type", copy=False)
    entry_type = fields.Selection(selection=ENTRY_TYPE,default="new", string="Entry Type", copy=False, tracking=True)
    type_of_company = fields.Selection(selection=TYPE_OF_COMPANY_OPTION, string="Type Of Company", copy=False)
    iso_certified = fields.Selection(selection=YES_OR_NO, string="ISO Certified", copy=False)
    dg_trained_drivers = fields.Selection(selection=YES_OR_NO, string="DG Trained Drivers", copy=False)
    driver_periodic_mhc = fields.Selection(selection=YES_OR_NO, string="Driver Periodic Health Checkup", copy=False)
    safty_tra_prog = fields.Selection(selection=YES_OR_NO, string="Safety Training Program", copy=False)
    depot_service = fields.Selection(selection=YES_OR_NO, string="Deport Vendor Name", copy=False)
    feedback_type = fields.Selection(selection=FEEDBACK_TYPE_OPTION, string="Feedback Type", copy=False)
    relationship = fields.Selection(selection=RELATIONSHIP_TYPE, string="Relationship", copy=False)
    health_certificate = fields.Selection(selection=YES_OR_NO, string="Health Certificate", copy=False)
    health_insurance = fields.Selection(selection=YES_OR_NO, string="Health Insurance", copy=False)
    license_type = fields.Selection(selection=LICENSE_TYPE, string="License Type", copy=False)
    port_category = fields.Selection(selection=PORT_CATEGORY, string="Port Category", copy=False)
    icd_connected = fields.Selection(selection=YES_OR_NO, string="Is ICD Connected", copy=False)
    sea_connected = fields.Selection(selection=YES_OR_NO, string="Is Seaport Connected", copy=False)
    free_zone = fields.Selection(selection=YES_OR_NO, string="Is Free Zone Port", copy=False)
    sanctioned_port = fields.Selection(selection=YES_OR_NO, string="Sanctioned Port", copy=False, default='yes')
    agent_type = fields.Selection(selection=AGENT_TYPE, string="Agent Type", copy=False)
    discount_provision = fields.Selection(selection=YES_OR_NO, string="Discount Provision", copy=False) #100
    emergency_plan = fields.Selection(selection=YES_OR_NO, string="Emergency Plan", copy=False)
    port_bound = fields.Selection(selection=BOUND_OPTIONS, string="Bound", copy=False, tracking=True)
    service_availability = fields.Selection(selection=SERVICE_AVAILABILITY_OPTION, string="Service Availability", copy=False)
    vessel_service_providers = fields.Selection(selection=VESSEL_SERVICE_PROVIDERS, string="Vessel Service Providers", copy=False)
    vessel_type = fields.Selection(selection=VESSEL_TYPE, string="Vessel Type", copy=False, tracking=True)
    stcw_huwet_training = fields.Selection(selection=YES_OR_NO, string="STCW / HUWET Training", copy=False)
    terminal_type = fields.Selection(selection=TERMINAL_TYPE, string="Terminal Type", copy=False, tracking=True)
    safety_manual = fields.Selection(selection=YES_OR_NO, string="Safety Manual", copy=False, tracking=True)
    restricted_category = fields.Selection(selection=RESTRICTED_CATEGORY, string="Restricted Category", copy=False)
    service_provider = fields.Selection(selection=SERVICE_PROVIDER, string="Service Provider", copy=False)
    mandatory = fields.Selection(selection=MANDATORY, string="Mandatory", copy=False, default='yes')
    import_export = fields.Selection(selection=IMPORT_EXPORT, string="Import / Export", copy=False)              
    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Container Category", copy=False)
    cargo_category = fields.Selection(selection=CARGO_CATEGORY, string="Cargo Category", copy=False) 
    is_registered = fields.Selection(selection=YES_OR_NO, string="Is Registered Tank Operator", copy=False)
    agent_service = fields.Selection(selection=APPLICABLE_OPTION, string="Agent Service", copy=False)
    contract_agree = fields.Selection(selection=YES_OR_NO, string="Contractual Agreements", copy=False)
    validity_range = fields.Selection(selection=VALIDITY_RANGE, string="Validity Range", copy=False)
    
    #Boolean 
    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    manual_round_off = fields.Boolean(string="Apply Manual Round Off", default=False)
    trigger_del = fields.Boolean(string="Trigger Delete", default=False)

    #Catalyst
    sun = fields.Boolean(string="Sun", copy=False, default=False)
    mon = fields.Boolean(string="Mon", copy=False, default=False)
    tue = fields.Boolean(string="Tue", copy=False, default=False)
    wed = fields.Boolean(string="Wed", copy=False, default=False)
    thu = fields.Boolean(string="Thu", copy=False, default=False)
    fri = fields.Boolean(string="Fri", copy=False, default=False)
    sat = fields.Boolean(string="Sat", copy=False, default=False)
    external = fields.Boolean(string="External", copy=False, default=False)
    cleaning = fields.Boolean(string="Cleaning", copy=False, default=False)
    condition = fields.Boolean(string="Condition", copy=False, default=False)
    on_hire = fields.Boolean(string="On Hire", copy=False, default=False)
    off_hire = fields.Boolean(string="Off Hire", copy=False, default=False)
    lang_read = fields.Boolean(string="Read",copy=False, default=False)
    lang_write = fields.Boolean(string="Write",copy=False, default=False)
    lang_speak = fields.Boolean(string="Speak",copy=False, default=False)
    repair_stage_inspect = fields.Boolean(string="Repair & Stage Wise Inspection", copy=False, default=False)

    #Many2one
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


    #Float
    qty = fields.Float(string="Quantity", digits=(2, 3))	
    bal_qty = fields.Float(string="Inward Pending Qty", digits=(2, 3), store=True, compute='_compute_all_line')	
    rec_qty = fields.Float(string="Received Quantity", digits=(2, 3), store=True)
    approve_qty = fields.Float(string="Approved Quantity", digits=(2, 3))
    reject_qty = fields.Float(string="Rejected Quantity", digits=(2, 3), store=True)
    unit_price = fields.Float(string="Unit Price")	
    unitprice_wt = fields.Float(string="Unit Price(WT)", help="Unit price with Taxes", store=True, compute='_compute_all_line')	
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    disc_per = fields.Float(string="Discount(%)")
    amt = fields.Float(string="Amount",store=True, compute='_compute_all_line')	
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')	
    net_amt = fields.Float(string="Net Amount", store=True, compute='_compute_all_line')
    tax_amt = fields.Float(string="Tax Amount(+)", store=True, compute='_compute_all_line')	
    bal_amt = fields.Float(string="Balance Amount", store=True)	
    other_amt = fields.Float(string="Other Charges(+)", store=True, compute='_compute_all_line')
    line_tot_amt = fields.Float(string="Line Total", store=True, compute='_compute_all_line')
    tds_amt = fields.Float(string="TDS Amount")	
    freight_amt = fields.Float(string="Freight Amount")	
    amc_period = fields.Float(string="AMC Period(Months)")	
    tot_dis_amt = fields.Float(string="Total Discount Amount", store=True, compute='_compute_all_line')
    taxable_amt = fields.Float(string="Taxable Amount", store=True, compute='_compute_all_line')
    round_off_amt = fields.Float(string="Round Off Amount(+/-)", store=True, compute='_compute_all_line')	
    cgst_amt = fields.Float(string="CGST Amount", store=True, compute='_compute_all_line')
    sgst_amt = fields.Float(string="SGST Amount", store=True, compute='_compute_all_line')
    igst_amt = fields.Float(string="IGST Amount", store=True, compute='_compute_all_line')
    fixed_disc_amt = fields.Float(string="Fixed Discount Amount(-)", store=True, compute='_compute_all_line')
    grand_tot_amt = fields.Float(string="Grand Total", store=True, compute='_compute_all_line')
    border_entry_fee = fields.Float(string="Border Entry Fee(INR)", copy=False)

    
    #Catalyst
    operating_hrs_start = fields.Float(string="Operating Hrs Start", copy=False)
    operating_hrs_end = fields.Float(string="Operating Hrs End", copy=False)
    weight = fields.Float(string="Weight(Kg)", copy=False)
    paid_up_capital = fields.Float(string="Paid-up Capital", copy=False)
    proj_bus_volume = fields.Float(string="Projected Volume of Business", copy=False)
    credit_limit = fields.Float(string="Number", copy=False)
    profit_val = fields.Float(string="Profit(%)", copy=False)
    unit_value = fields.Float(string="Tentative Value", copy=False)    
    maximum_cost = fields.Float(string="Maximum Cost", copy=False)
    actual_cost = fields.Float(string="Actual Cost", copy=False)
    gr_cost = fields.Float(string="GR Cost", copy=False)
    

    
    #Integer
    entry_seq = fields.Integer(string="Sequence", copy=False)
    version_no = fields.Integer(string="Version No", copy=False, readonly=True)
    cr_days = fields.Integer(string="Credit Days", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    revise_version = fields.Integer(string="Revise Version", copy=False, readonly=True)
    seq_next_number = fields.Integer(string="Sequence Next Number", copy=False)
    distance = fields.Integer(string="Distance KM", copy=False)


    #Catalyst
    no_of_employee = fields.Integer(string="No. Of Employees", copy=False)
    msme_no = fields.Integer(string="MSME No", copy=False)
    total_area = fields.Integer(string="Total Area(Sqft)", copy=False)
    escalation_days = fields.Integer(string="Escalation Days", copy=False, default=15)
    lease_duration = fields.Integer(string="Lease Duration(Months)", copy=False)
    rental_value = fields.Integer(string="Rental Value", copy=False)
    warranty_period = fields.Integer(string="Warranty Periods(Months)", copy=False)
    mfg_lead_time = fields.Integer(string="Manufacturing Lead Time(Days)", copy=False)
    credit_days = fields.Integer(string="Credit Days", copy=False)
    tentative_value = fields.Integer(string="Tentative Value", copy=False)    
    vehicle_age = fields.Integer(string="Vehicle Age", copy=False)
    engine_capacity = fields.Integer(string="Engine Capacity", copy=False)
    vehicle_tare_weight = fields.Integer(string="Vehicle Age", copy=False)
    vehicle_gross_weight = fields.Integer(string="Vehicle Gross Weight", copy=False)
    standard_mileage = fields.Integer(string="Standard Mileage", copy=False)
    validity_months = fields.Integer(string="Validity (Months)", copy=False)
    validity_days = fields.Integer(string="Validity (Days)", copy=False)
    nat_validity_month = fields.Integer(string="Validity (Months)", copy=False)
    nat_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    nat_esc_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)    
    fc_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    fc_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    fc_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)
    rt_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    rt_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    rt_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)
    puc_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    puc_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    puc_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)
    green_tax_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    green_tax_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    green_tax_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)    
    speed_limit_per = fields.Integer(string="Speed Limit Per Hr.", copy=False)
    speed_govener_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    speed_govener_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    speed_govener_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)    
    amc_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    amc_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    amc_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False)
    validity_period = fields.Integer(string="Validity Period(Months)", copy=False)
    minimum = fields.Integer(string="Minimum KM", copy=False)
    maximum = fields.Integer(string="Maximum KM", copy=False)
    fuel_avg_cost = fields.Integer(string="Fuel Avg Cost (Per Ltr)", copy=False)
    vehicle_avg_mileage_empty = fields.Integer(string="Vehicle Avg Mileage (Empty) ", copy=False)
    vehicle_avg_mileage_laden = fields.Integer(string="Vehicle Avg Mileage (Laden)", copy=False)
    avg_mileage = fields.Integer(string="Avg Mileage", copy=False)
    per_day_trip_margin = fields.Integer(string="Per Day Trip Margin(INR)", copy=False)
    trip_duration = fields.Integer(string="Trip Duration(Hrs.)", copy=False)
    toll_fee = fields.Integer(string="Toll Fee(INR)", copy=False)
    total_trip = fields.Integer(string="Total Trip(Km)", copy=False)
    own_trailer_count = fields.Integer(string="Own Trailer Count", copy=False)
    attached_trailer_count = fields.Integer(string="Attached Trailer Count", copy=False)
    monthly_salary = fields.Integer(string="Monthly Salary", copy=False)
    berthing_days = fields.Integer(string="Berthing Days", copy=False)
    trans_days = fields.Integer(string="Transshipment Days", copy=False)
    avg_time = fields.Integer(string="Average Time Taken", copy=False)
    vessel_capacity = fields.Integer(string="Vessel Capacity", copy=False)
    year_built = fields.Integer(string="Year Built", copy=False)
    time_duration = fields.Integer(string="Time Duration(Hrs.)", copy=False)
    minimum_days = fields.Integer(string="Minimum days", copy=False)
    maximum_days = fields.Integer(string="Maximum days", copy=False)
    interval = fields.Integer(string="Interval", copy=False)


    #Text
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    round_off_remark = fields.Text(string="Round Off Remarks", copy=False)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    closer_note = fields.Text(string="Closer Notes", copy=False)
    batch_info = fields.Text(string="Info", copy=False)
    feedback = fields.Text(string="Rating Feedback", copy=False)
    nature_of_work = fields.Text(string="Nature Of Work")
    revise_remark = fields.Text(string="Revise Remarks", copy=False)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    remark = fields.Char(string="Remarks", copy=False)
    #Catalyst
    key_remarks = fields.Text(string="Key Remarks", copy=False)
    parking_name = fields.Text(string="Name Of The Parking Places", copy=False)
    reason = fields.Text(string="Reason", copy=False)
    detail_desc = fields.Text(string="Detail Explanation", copy=False)
    commodity_desc = fields.Text(string="Commodity Description", copy=False)
    #HTML -> Text
    note = fields.Text(string="Notes", copy=False)
    customs_note = fields.Text(string="Customs Notes", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    sec_msure_note = fields.Text(string="Security Measure Notes", copy=False)
    port_auth_regul = fields.Text(string="Port Authority Regulations", copy=False)

    #Date
    from_date = fields.Date(string="From Date", default=fields.Date.today)
    to_date = fields.Date(string="To Date", default=fields.Date.today)
    dc_date = fields.Date(string="DC Date", copy=False, tracking=True)
    due_date = fields.Date(string="Due Date", copy=False)
    remind_date = fields.Date(string="Reminder Date", copy=False, tracking=True)
    vendor_inv_date = fields.Date(string="Supplier / Vendor Invoice Date", copy=False, tracking=True)
    cheque_date = fields.Date(string="Cheque Date", copy=False, tracking=True)
    clearing_date = fields.Date(string="Clearing Date", copy=False)
    quote_date = fields.Date(string="Quotation Date",copy=False, default=fields.Date.today, tracking=True)
    request_date = fields.Date(string="Request Date", default=fields.Date.today)
    eff_from_date = fields.Date(string="Effect From Date")
    draft_date = fields.Date(string="Draft Date", copy=False, default=fields.Date.today)
    ack_date = fields.Date(string="Acknowledgement Date", copy=False)
    comply_date = fields.Date(string="Compliant Date", copy=False)
    receive_date = fields.Date(string="Received Date")
    ship_date = fields.Date(string="Shipping Date", copy=False)
    stmt_date = fields.Date(string="Statement Date", default=fields.Date.today)
    cr_date = fields.Date(string="Credit Date")
    dr_date = fields.Date(string="Debit Date", copy=False)
    enq_date = fields.Date(string="Enquiry Date", copy=False, default=fields.Date.today)
    customer_po_date = fields.Date(string="Customer PO Date", copy=False, tracking=True)
    join_date = fields.Date(string="Joining Date", copy=False, default=fields.Date.today, tracking=True)
    relive_date = fields.Date(string="Reliving Date", copy=False, tracking=True)
    clearing_date = fields.Date(string="Clearing Date", copy=False)
    birth_date = fields.Date(string="Date Of Birth", copy=False)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    delivery_date = fields.Date(string="Delivery Date", copy=False, tracking=True)
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    as_on_date = fields.Date(string="As On Date", default=fields.Date.today)
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    #Catalyst
    last_audit_date = fields.Date(string="Last Audit Date", copy=False)
    next_audit_date = fields.Date(string="Next Audit Date", copy=False)
    lease_valid_from_date = fields.Date(string="Validity From Date", copy=False)
    lease_valid_to_date = fields.Date(string="Validity To Date", copy=False)
    con_start_date = fields.Date(string="Contract Start Date", copy=False)
    con_end_date = fields.Date(string="Contract End Date", copy=False)
    holiday_date = fields.Date(string="Date", copy=False)
    purchase_date = fields.Date(string="Purchase Date", copy=False)
    national_from_date = fields.Date(string="From Date", copy=False)
    national_to_date = fields.Date(string="To Date", copy=False)
    last_fc_date = fields.Date(string="Last FC Date", copy=False)
    next_fc_date = fields.Date(string="Next FC Date", copy=False)
    next_inspection_date = fields.Date(string="Next Inspection Date", copy=False)
    road_tax_paid_date = fields.Date(string="Road Tax Paid Date", copy=False)
    rt_validity_to_date = fields.Date(string="Validity To Date", copy=False)
    puc_from_date = fields.Date(string="From Date", copy=False)
    puc_to_date = fields.Date(string="To Date", copy=False)
    green_tax_from_date = fields.Date(string="From Date", copy=False)
    green_tax_to_date = fields.Date(string="To Date", copy=False)
    spd_gov_from_date = fields.Date(string="From Date", copy=False)
    spd_gov_to_date = fields.Date(string="To Date", copy=False)
    amc_from_date = fields.Date(string="From Date", copy=False)
    amc_to_date = fields.Date(string="To Date", copy=False)
    eff_from_date = fields.Date(string="Effective From Date", copy=False)
    mhc_date = fields.Date(string="Last Health Checkup Date", copy=False)
    next_mhc_date = fields.Date(string="Next Health Checkup Date", copy=False)
    lic_expire_date = fields.Date(string="License Expiry Date", copy=False)

    #Datetime
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    cancel_date = fields.Datetime(string="Cancelled Date", copy=False, readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    attach_date = fields.Datetime(string="Attached Date", copy=False, readonly=True)
    inactive_date = fields.Datetime(string="Inactivated Date", copy=False, readonly=True)
    generate_date = fields.Datetime(string="Generated Date", copy=False, default=fields.Datetime.now, readonly=True, store=True)
    revised_date = fields.Datetime(string="Revised Date", copy=True, readonly=True)
    #Catalyst
    applied_on = fields.Datetime(string="Applied On", copy=False)
    
    
    #Many2many
    tax_ids = fields.Many2many('account.tax', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    #Image
    sign_img = fields.Image(string="Signature Image", copy=False, max_height=128, max_width=128)


    #Example
    header_id = fields.Many2one(RES_USERS, string='Transaction Reference', index=True, ondelete='cascade')
    #One2many --> use header_id instead of id.
    line_ids = fields.One2many(RES_USERS, 'id', string="Lines", copy=True)


    @api.depends('qty','bal_qty')
    def _compute_all_line(self):
        self.bal_qty  = 100
        return True

    def write(self, vals):
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id, 
                       })
        return super(FieldsDatabank, self).write(vals)

    @validation
    def button_action(self) -> dict:
        return {
            'effect': {
            'fadeout': 'slow',
            'message': 'Everything Looks Good!',
	        'img_url': '/fields_databank/static/img/smiley.gif',
            'type': 'rainbow_man',
                      }
               }
