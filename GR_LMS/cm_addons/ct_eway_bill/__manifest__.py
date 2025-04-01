# -*- coding: utf-8 -*-
{
    'name': "E-Way Bill",

    'summary': "This is a e-way bill",

    'description': """
            Scope of this module to fulfill the necessary features related to e-way bill form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_eway_bill_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_eway_bill/static/src/css/*.css',
            'ct_eway_bill/static/src/css/*.scss',
            'ct_eway_bill/static/src/views/*.js',
            'ct_eway_bill/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

