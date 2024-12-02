# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api
from odoo.addons.custom_properties.decorators import validation

RES_USERS = 'res.users'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'
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

WARRANTY_STATUS = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

MAIL_SMS_STATUS = [('pending', 'Pending'),
                   ('sent', 'Sent'),
                   ('re_sent', 'Re-Send'),('not_applicable', 'Not Applicable'),
                   ('sms_not_applicable', 'SMS Not Applicable'),
                   ('mail_not_applicable', 'Mail Not Applicable')]

JC_STATUS = [('applicable', 'Applicable'),
             ('not_applicable', 'Not Applicable'),
             ('jc_open', 'JC Open'),
             ('jc_closed', 'JC Closed')]

YEARS = [('fiscal_year', 'Fiscal Year'),
         ('calendar_year','Calendar Year')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

COMPANY_TYPE_OPTIONS = [('person', 'Individual'), ('company', 'Company')]

GST_OPTIONS = [('registered', 'Registered'), ('un_registered', 'Un Registered')]

GRADE_OPTIONS = [('a', 'A'), ('b', 'B'), ('c', 'C')]

RATING_OPTIONS = [('0','0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]

FORMAT_TYPE_OPTIONS = [('excel', 'Excel'),('pdf', 'PDF')]

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
    phone_no = fields.Char(string="Phone No", size=12)
    pin_code = fields.Char(string="Pin Code", copy=False, size=10)
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
    street = fields.Char(string="Street", size=252)
    street1 = fields.Char(string="Street1", size=252)
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
    job_position = fields.Char(string="Job Position", copy=False, size=50)
    tax_name = fields.Char(string="Tax Name", copy=False, size=252)
    serial_no = fields.Char(string="Serial No", copy=False, size=252)
    mail_from = fields.Char(string="From", copy=False, size=252)
    mail_to = fields.Char(string="To", copy=False, size=252)
    mail_cc = fields.Char(string="Cc", copy=False, size=252)
    mail_bcc = fields.Char(string="Bcc", copy=False, size=252)
    interval = fields.Char(string="Interval", copy=False, size=252)
    from_mail_id = fields.Char(string="From Email-ID", copy=False, size=252)
    subject = fields.Char(string="Subject", copy=False, size=252)
    watcher_mail_id = fields.Char(string="Watcher Mail ID", copy=False, size=252)
    ext_no = fields.Char(string="Ext No", copy=False, size=15)
    seq_month = fields.Char(string="Sequence Month", copy=False, size=252)
    seq_year = fields.Char(string="Sequence Year", copy=False, size=252)
    fiscal_year_code = fields.Char(string="Fiscal Year Code", copy=False, size=5)

	
    #Selection
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    pay_mode = fields.Selection(selection=PAY_MODE_OPTIONS, string="Mode Of Payment", copy=False, tracking=True)
    grn_type = fields.Selection(selection=TRANS_STATUS, string="GRN Type", copy=False)
    entry_from = fields.Selection(selection=TRANS_STATUS, string="Entry From", copy=False, tracking=True)
    invoice_control = fields.Selection(selection=TRANS_STATUS, string="Invoice / Billing Status", copy=False)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    wages_type = fields.Selection(selection=TRANS_STATUS, string="Wages Type", copy=False)
    priority = fields.Selection(selection=TRANS_STATUS, string="Priority", tracking=True)
    warranty = fields.Selection(selection=WARRANTY_STATUS, string="Warranty", copy=False, tracking=True)
    email_status = fields.Selection(selection=MAIL_SMS_STATUS, string="Email Status", copy=False)
    sms_status = fields.Selection(selection=MAIL_SMS_STATUS, string="SMS Status", copy=False)
    jc_status = fields.Selection(selection=JC_STATUS, string="Job Card Status", copy=False)
    seq_num_reset = fields.Selection(selection=YEARS, string="Sequence Number Reset")
    tds = fields.Selection(selection=YES_OR_NO, string="TDS Applicable", copy=False)
    company_type = fields.Selection(selection=COMPANY_TYPE_OPTIONS, string="Company Type", copy=False)
    gst_category = fields.Selection(selection=GST_OPTIONS, string="GST Category", copy=False)
    grade = fields.Selection(selection=GRADE_OPTIONS, string="Grade", copy=False)
    rating = fields.Selection(selection=RATING_OPTIONS, string="Rating", copy=False)
    format_type = fields.Selection(selection=FORMAT_TYPE_OPTIONS, string="Format Type", nolabel=True, widget='selection')

    #Boolean 
    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    manual_round_off = fields.Boolean(string="Apply Manual Round Off", default=False)
    trigger_del = fields.Boolean(string="Trigger Delete", default=False)

    #Many2one
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", copy=False, ondelete='restrict', readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    attach_user_id = fields.Many2one(RES_USERS, string="Attached By", copy=False, ondelete='restrict', readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner Name", index=True, ondelete='restrict', tracking=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    product_id = fields.Many2one('product.product', string="Product Name", index=True, ondelete='restrict')
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    department_id = fields.Many2one(CM_MASTER, string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    brand_id = fields.Many2one(CM_MASTER, string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    model_id = fields.Many2one(CM_MASTER, string="Model Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    catg_id = fields.Many2one(CM_MASTER, string="Category Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    del_term_id = fields.Many2one(CM_MASTER, string="Delivery Term", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    inward_id = fields.Many2one(CM_MASTER, string="Inward Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    outward_id = fields.Many2one(CM_MASTER, string="Outward Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    city_id = fields.Many2one(CM_MASTER, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    division_id = fields.Many2one(CM_MASTER, string="Division", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    project_id = fields.Many2one(CM_MASTER, string="Project Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bank_id = fields.Many2one(CM_MASTER, string="Bank Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    period_id = fields.Many2one(CM_MASTER, string="Period", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    account_id = fields.Many2one(CM_MASTER, string="Account Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    transport_id = fields.Many2one(CM_MASTER, string="Transport Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    employee_id = fields.Many2one(CM_MASTER, string="Employee Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    job_id = fields.Many2one(CM_MASTER, string="Designation", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    executive_id = fields.Many2one(CM_MASTER, string="Executive", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    segment_id = fields.Many2one(CM_MASTER, string="Segment", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    source_id = fields.Many2one(CM_MASTER, string="Source Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    destination_id = fields.Many2one(CM_MASTER, string="Destination Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    labor_id = fields.Many2one(CM_MASTER, string="Labor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    branch_id = fields.Many2one(CM_MASTER, string="Branch Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    expense_id = fields.Many2one(CM_MASTER, string="Expense", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    tax_group_id = fields.Many2one(CM_MASTER, string="Tax Group", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    task_manager_id = fields.Many2one(RES_USERS, string="Task Manager", ondelete='restrict', tracking=True)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", copy=False, ondelete='restrict', readonly=True)
    title_id = fields.Many2one('res.partner.title', string="Title", copy=False, ondelete='restrict')
    model_id = fields.Many2one('ir.model', string="Model Name", copy=False)
    generate_user_id = fields.Many2one(RES_USERS, string="Generated By", copy=False, default=lambda self: self.env.user.id, readonly=True, store=True)
    revised_user_id = fields.Many2one(RES_USERS, string="Revised By", copy=False, readonly=True)
    parent_id = fields.Many2one(RES_USERS, string="Parent Ref", copy=False, readonly=True)
    copy_user_id = fields.Many2one(RES_USERS, string="Existing User", copy=False, domain=[('status', '=', 'active')])
    fiscal_year_id = fields.Many2one('cm.fiscal.year',string="Fiscal Year", copy=False)
    ir_sequence_id = fields.Many2one('ir.sequence', string="IR Sequence Ref", copy=False)
    po_id = fields.Many2one(CM_MASTER, string="Purchase Order", copy=False)

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

    #HTML
    note = fields.Html(string="Notes", copy=False, sanitize=False)

    #Integer
    entry_seq = fields.Integer(string="Sequence", copy=False)
    version_no = fields.Integer(string="Version No", copy=False, readonly=True)
    cr_days = fields.Integer(string="Credit Days", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    revise_version = fields.Integer(string="Revise Version", copy=False, readonly=True)
    seq_next_number = fields.Integer(string="Sequence Next Number", copy=False)

    #Text
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    round_off_remark = fields.Text(string="Round Off Remarks", copy=False)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    closer_note = fields.Text(string="Closer Notes", copy=False)
    batch_info = fields.Text(string="Info", copy=False)
    rating_feedback = fields.Text(string="Rating Feedback", copy=False)
    nature_of_work = fields.Text(string="Nature Of Work")
    revise_remark = fields.Text(string="Revise Remarks", copy=False)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    remark = fields.Char(string="Remarks", copy=False)

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
    eff_from_date = fields.Date(string="Effect From Date", default=fields.Date.today)
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

    #Many2many
    tax_ids = fields.Many2many('account.tax', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    partner_ids = fields.Many2many('res.partner', string="Partner Name", ondelete='restrict', check_company=True, domain=[('active', '=', True)])
    department_ids = fields.Many2many('res.users', string='Access Departments', ondelete='restrict')
    user_menu_ids = fields.Many2many('ir.ui.menu', string="Access Menus", ondelete='restrict')
    groups_ids = fields.Many2many('res.groups', string="Groups", ondelete='restrict')
    access_company_ids = fields.Many2many(RES_COMPANY, string="Access Companies", ondelete='restrict', store=True)
    division_ids = fields.Many2many(RES_COMPANY, 'division_id', 'user_id', string="Access Divisions", ondelete='restrict', store=True)

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
