# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('quotation_sent', 'Approved'),
    ('order_released', 'Order Released '),
    ('original', 'Original'),
    ('revised', 'Revised'),
    ('rejected', 'Rejected'),    
    ('cancelled', 'Cancelled')]

class CtQuotationsMailPreview(models.TransientModel):
    _name = 'ct.quotations.mail.preview'
    _description = "Mail Preview"

    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    mail_from = fields.Char('From')
    mail_to = fields.Char('To')
    mail_cc = fields.Char('Cc')
    mail_bcc = fields.Char('Bcc')
    subject = fields.Char('Subject')
    body = fields.Html('Body', sanitize=False)
    attachment_ids = fields.Many2many('ir.attachment', string="Attachment", ondelete='restrict')
    quotations_id = fields.Many2one('ct.quotations', string="Quotations", store=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", related="quotations_id.status")

    

    @api.model
    def default_get(self, fields_list):
        res = super(CtQuotationsMailPreview, self).default_get(fields_list)
        # attachment_ids = self.context.get('attachment')  
        res.update({
            'mail_to': self.env.context.get('email'),
            'quotations_id': self.env.context.get('quotations_id'),
            'attachment_ids': [(4, id) for id in self.env.context.get('attachment')],
            'subject': f"#GMPL-Quotation# {self.env.context.get('name')}",
            'body': f'''<html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Quotation Email</title>
                        </head>
                        <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; color: #333;">

                            <div style="width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); padding: 20px;">
                                <div style="text-align: center; padding-bottom: 20px; border-bottom: 1px solid #ddd;">
                                    <h1 style="margin: 0; font-size: 24px; color: #2c3e50;">Goodrich Maritime Private Limited</h1>
                                    <br/>
                                    <h1 style="margin: 0; font-size: 24px; color: #2c3e50;">Quotation <span id="quotation-number"></span></h1>
                                </div>

                                <div style="padding: 20px 0;">
                                    <p>Dear Sir / Mam, </p> 
                                    <p>Thank you for your interest in our services / products. We are pleased to provide you with the quotation details below. Should you have any questions or need further clarification, feel free to reach out to us.<br/><br/> Kindly find the attachment for more details.</p>

                                    <div style="margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
                                        <p><strong>Quotation No :</strong> {self.env.context.get('name')}</p>
                                        <p><strong>Date         :</strong> {self.env.context.get('entry_date')}</p>
                                        <p><strong>Booking Party:</strong> {self.env.context.get('bkg_party_name')}</p>
                                        <p><strong>Service Name :</strong> {self.env.context.get('service_name')}</p>
                                        <p><strong>Total Amount : {format(self.env.context.get('net_amt'), ',')} {self.env.context.get('quotation_currency')} </strong></p>
                                        <p><strong>Validity Date:</strong> {self.env.context.get('validity_date')}</p>
                                    </div>
                                    <p> {self.env.context.get('mail_content')}</p>
                                    <p>We look forward to your confirmation and are happy to assist you with any additional information you may require.</p>
                                </div>
                            </div>

                        </body>
                        </html>
                        '''
        })
        return res

    def action_mail_send(self):
        for rec in  self.env.context.get('active_ids'):
            quotation = self.env['ct.quotations'].search([('id', '=', rec)])
            quotation.mail_send(data=self.body, to=self.mail_to, cc=self.mail_cc, bcc=self.mail_bcc, subject=self.subject, attachment_id=self.attachment_ids)