# -*- coding: utf-8 -*-
{
    'name': "Quotations",

    'summary': "This is a quotations",

    'description': """
            Scope of this module to fulfill the necessary features related to quotations form.
    """,

    'author': "Hari",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','cm_base_inherit', 'cm_flexi_capacity', 'cm_surveyor_tariff','cm_flexi_layer_type', 'cm_exchange_rate'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'data/cron_quotation_bc_pending_mail.xml',
        'views/ct_quotations_view.xml',
        'views/ct_quotations_operator_offer_view.xml',        
        'wizard/ct_quotations_mail_preview_view.xml',
        'wizard/ct_quotations_revise_remarks_view.xml', 
        'reports/ct_quotations_report.xml',
        'reports/ct_quotations_template.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_quotations/static/src/css/*.css',
            'ct_quotations/static/src/css/*.scss',
            'ct_quotations/static/src/views/*.js',
            'ct_quotations/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

