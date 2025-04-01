# -*- coding: utf-8 -*-
{
    'name': "Store Issue Request",

    'summary': "This is a store issue request",

    'description': """
            Scope of this module to fulfill the necessary features related to store issue request form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','ct_business_confirmation'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_store_issue_request_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_store_issue_request/static/src/css/*.css',
            'ct_store_issue_request/static/src/css/*.scss',
            'ct_store_issue_request/static/src/views/*.js',
            'ct_store_issue_request/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

