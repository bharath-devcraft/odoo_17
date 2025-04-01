# -*- coding: utf-8 -*-
{
    'name': "RFQ",

    'summary': "This is a RFQ",

    'description': """
            Scope of this module to fulfill the necessary features related to common RFQ transaction form.
    """,

    'author': "Karthikeyan S",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_rfq_view.xml',
        'wizard/ct_rfq_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_rfq/static/src/css/*.css',
            'ct_rfq/static/src/css/*.scss',
            'ct_rfq/static/src/views/*.js',
            'ct_rfq/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

