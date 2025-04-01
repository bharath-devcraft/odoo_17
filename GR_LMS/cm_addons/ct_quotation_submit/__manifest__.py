# -*- coding: utf-8 -*-
{
    'name': "Quotation Submit",

    'summary': "This is a Quotation Submit",

    'description': """
            Scope of this module to fulfill the necessary features related to common Quotation Submit form.
    """,

    'author': "Karthikeyan S",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['account','base','mail','custom_properties','cm_fiscal_year','ct_rfq'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_quotation_submit_view.xml',
        'wizard/ct_quotation_submit_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_quotation_submit/static/src/css/*.css',
            'ct_quotation_submit/static/src/css/*.scss',
            'ct_quotation_submit/static/src/views/*.js',
            'ct_quotation_submit/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

