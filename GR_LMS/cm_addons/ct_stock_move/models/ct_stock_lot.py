# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_STOCK_MOVE = 'ct.stock.lot'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CM_MASTER = 'cm.master'

UOM='uom.uom'

ISSUE_TYPE=[('material', 'Material'),('service', 'Service')]

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('approved', 'In Stock'),
    ('not_in_stock', 'Not In Stock'),
    ('expired', 'Expired')
    ]

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                     ('not_applicable', 'Not Applicable')]
                     

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]
LOT_TYPE =  [('new','New'),
             ('replacement', 'Replacement')]

class CtStockLot(models.Model):
    _name = 'ct.stock.lot'
    _description = 'Lot/Serial No Details'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'
    _rec_name = 'serial_no'

    name = fields.Char(string="Ref No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", compute="_compute_status", readonly=True, store=True, tracking=True)
    
    remarks = fields.Text(string="Remarks", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one(CM_MASTER, string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    
    ref_no = fields.Char(string="Ref No")
    entry_date = fields.Date(string="Ref Date", copy=False, default=fields.Date.today)
    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    store_uom_id = fields.Many2one(UOM, string="Store UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    store_uom_qty = fields.Float(string="Store UOM Qty", digits=(2, 3))
    store_pend_qty = fields.Float(string="Store UOM Pending Qty", digits=(2, 3))
    po_uom_id = fields.Many2one(UOM, string="PO UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    po_uom_qty = fields.Float(string="PO UOM Qty", digits=(2, 3))
    po_pend_qty = fields.Float(string="PO UOM Pending Qty", digits=(2, 3))

    warranty = fields.Selection(selection=APPLICABLE_OPTION, string="Warranty", copy=False, tracking=True)
    lot_type = fields.Selection(selection=LOT_TYPE, string="Lot Type", copy=False, tracking=True)
    from_date = fields.Date(string="Warranty From Date", copy=False)
    expiry_date = fields.Date(string="Expiry/To Date", copy=False)
    serial_no = fields.Char(string="Serial No", copy=False, size=252)
    unit_price = fields.Float(string="Unit Price")	
    price_tax = fields.Float(string="Price Tax")	
    parent_id = fields.Many2one('ct.stock.lot', string="Parent Serial No", ondelete='restrict')
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
         
    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
 
    line_ids = fields.One2many('ct.stock.lot.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    def display_warnings(self, warning_msg, kw):
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(_(formatted_messages))
            else:
                return [formatted_messages]
        else:
            return False
        
    @api.depends("store_pend_qty")
    def _compute_status(self):
        for record in self:
            record.status = 'not_in_stock' if record.store_pend_qty == 0 else 'approved'


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
        return super(CtStockLot, self).write(vals)


