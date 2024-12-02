# -*- coding: utf-8 -*-
{
    'name': "Nocost Transaction Template",

    'summary': "This is a nocost transaction template",

    'description': """
            Scope of this module to fulfill the necessary features related to common nocost transaction form.
    """,

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_nocost_transaction_view.xml',
        'wizard/ct_nocost_transaction_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_nocost_transaction/static/src/css/*.css',
            'ct_nocost_transaction/static/src/css/*.scss',
            'ct_nocost_transaction/static/src/views/*.js',
            'ct_nocost_transaction/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

