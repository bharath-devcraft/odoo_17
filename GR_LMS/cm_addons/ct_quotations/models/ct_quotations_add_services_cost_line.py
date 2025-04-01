# -*- coding: utf-8 -*-

from odoo import models, fields

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('quotation_sent', 'Approved'),
    ('order_released ', 'Order Released'),    
    ('revised', 'Revised'),
    ('cancelled', 'Cancelled')]

RES_USERS = 'res.users'


class CtQuotationsAdditionalServicesCostLine(models.Model):
    _name = 'ct.quotations.add.services.cost.line'
    _description = 'Additional Services Cost'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    name = fields.Char(string="Quotation No", index=True, size=30, related="quotations_id.name")
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], related="quotations_id.service_id")
    payment_term_id = fields.Many2one('cm.payment.term', string="Payment Term", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], related="quotations_id.payment_term_id")  
    un_tax_value = fields.Float(string="Un Taxed Value", related="quotations_id.taxable_amt")
    tax_value = fields.Float(string="Tax Value", related="quotations_id.tax_amt")      
    tot_value = fields.Float(string="Total Value", related="quotations_id.net_amt")
    validity_date = fields.Date(string="Validity Date", related="quotations_id.validity_date")  
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True, related="quotations_id.confirm_user_id") 
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved By", copy=False, ondelete='restrict', readonly=True, related="quotations_id.ap_rej_user_id")         
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict',  related="quotations_id.quotation_currency_id")    
    quotations_id =  fields.Many2one('ct.quotations', string="Quotations", ondelete='restrict')  
    child_status = fields.Selection(selection=CUSTOM_STATUS, string="Status", default="draft", store=True, tracking=True, related="quotations_id.status")
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


    def call_revise_popup(self):
        local_context = dict(
            self.env.context,
            id=self.id,
        )
        return {
                'type': 'ir.actions.act_window',
                'name': "Revise Remarks",
                'res_model': 'ct.quotations.revise.remarks',
                'view_mode': 'form',
                'target': 'new',
                'context': local_context,
            }  
        
    def revise_action(self, vals):
        if self.child_status == 'quotation_sent':
            self.quotations_id.revise_remark = vals['revise_remark']
            self.quotations_id.entry_revise()