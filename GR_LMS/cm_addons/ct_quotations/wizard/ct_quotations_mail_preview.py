# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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

    

    @api.model
    def default_get(self, fields_list):
        res = super(CtQuotationsMailPreview, self).default_get(fields_list)
        res.update({
            'mail_to': self.env.context.get('email'),
            'subject': f"#GMPL-Quotation# {self.env.context.get('name')}",
            'body': '''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Quotation Email</title>
                        <style>
                            body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f4f4f4;
                            color: #333;
                            }
                            .email-container {
                            width: 600px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            padding: 20px;
                            }
                            .email-header {
                            text-align: center;
                            padding-bottom: 20px;
                            border-bottom: 1px solid #ddd;
                            }
                            .email-header h1 {
                            margin: 0;
                            font-size: 24px;
                            color: #2c3e50;
                            }
                            .email-body {
                            padding: 20px 0;
                            }
                            .email-body p {
                            font-size: 16px;
                            line-height: 1.6;
                            }
                            .quotation-details {
                            margin: 20px 0;
                            padding: 15px;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                            background-color: #f9f9f9;
                            }
                            .quotation-details p {
                            margin: 5px 0;
                            }
                            .email-footer {
                            text-align: center;
                            font-size: 14px;
                            color: #888;
                            padding-top: 20px;
                            border-top: 1px solid #ddd;
                            }
                            .email-footer a {
                            color: #3498db;
                            text-decoration: none;
                            }
                            .button {
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #3498db;
                            color: #ffffff;
                            text-decoration: none;
                            border-radius: 5px;
                            margin-top: 20px;
                            }
                        </style>
                        </head>
                        <body>

                        <div class="email-container">
                            <div class="email-header">
                            <h1>Quotation <span id="quotation-number"></span></h1>
                            </div>

                            <div class="email-body">
                            <p>Dear Sir / Mam, </p> 
                            <p>Thank you for your interest in our services / products. We are pleased to provide you with the quotation details below. Should you have any questions or need further clarification, feel free to reach out to us. Kindly find the attachment for more details.</p>

                            <div class="quotation-details">
                                <p><strong>Quotation No : SQ/24-25/00003</strong> <span id="quotation-number"></span></p>
                                <p><strong>Date         :</strong> 29/11/2024</p>
                                <p><strong>Booking Party:</strong> DHL Global Forwarding</p>
                                <p><strong>Service Name :</strong> Overseas Trip Move Export</p>
                                <p><strong>Total Amount :</strong> INR 67,000.00 </p>
                                <p><strong>Validity Days:</strong> 10 </p>
                            </div>

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
            quotation.mail_send()