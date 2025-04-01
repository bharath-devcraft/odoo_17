# -*- coding: utf-8 -*-

from odoo import models, fields

import time
from datetime import datetime, timedelta

class CtQuotationsScheduler(models.Model):
    _name = 'ct.quotations.scheduler'
    _description = 'Quotations Scheduler'

    def quotations_bc_pending_scheduler_mail(self):
        mail_name = "Quotation BC Pending Mail"

        current_date = fields.Datetime.today()
        two_working_days_ago = current_date - timedelta(days=2)
        while two_working_days_ago.weekday() in [5, 6]:
            two_working_days_ago -= timedelta(days=1)
        qs_rec = self.env['ct.quotations'].search([('status', '=', 'quotation_sent'),('ap_rej_date', '<', two_working_days_ago)])
        
        if qs_rec:
            for qs in qs_rec:
                tat_days = 0
                temp_date = qs.ap_rej_date
                while temp_date.date() < current_date.date():
                    if temp_date.weekday() not in [5, 6]:
                        tat_days += 1
                    temp_date += timedelta(days=1)

                subject = f'#quotation-BC-pending# {qs.name} - TAT : {tat_days} days"'
                
                default_to=[]
                if qs.executed_user_id and qs.executed_user_id.email:
                    default_to.append(qs.executed_user_id.email)
                if qs.generated_user_id and qs.generated_user_id.email:
                    default_to.append(qs.generated_user_id.email)
                default_cc=[]
                if qs.ap_rej_user_id and qs.ap_rej_user_id.email:
                    default_cc.append(qs.ap_rej_user_id.email)
                if qs.confirm_user_id and qs.confirm_user_id.email:
                    default_cc.append(qs.confirm_user_id.email)

                self.env.cr.execute("""select csm_quotation_bc_pending_mail(%s,'%s','%s','%s')"""%
                                    (qs.id,qs.status,qs.name or qs.draft_name, qs.ap_rej_user_id.partner_id.name,))
                data = self.env.cr.fetchall()

                if data[0][0]:
                    mail_type='scheduler'
                    mail_config_name='Quotation BC Pending Mail'
                    vals = self.env['cp.mail.configuration'].mail_config_mailids_data(mail_type=mail_type,mail_name=mail_config_name)

                    email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
                    email_cc = ", ".join(set(default_cc + vals.get('email_cc', []))) if default_cc or vals.get('email_cc') else ''
                    email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
                    email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''
                    self.env['cp.mail.queue'].create_mail_queue(
                        name = mail_name, trans_rec = self, mail_from = email_from,
                        email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                        subject = subject, body = data[0][0])
        return True
