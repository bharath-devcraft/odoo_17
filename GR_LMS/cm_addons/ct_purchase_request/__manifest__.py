# -*- coding: utf-8 -*-
{
    'name': "Purchase Request",

    'summary': "This is a Purchase Request",

    'description': """
            Scope of this module to fulfill the necessary features related to common purchase request form.
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
        'views/ct_purchase_request_view.xml',
        'wizard/ct_purchase_request_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_purchase_request/static/src/css/*.css',
            'ct_purchase_request/static/src/css/*.scss',
            'ct_purchase_request/static/src/views/*.js',
            'ct_purchase_request/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

