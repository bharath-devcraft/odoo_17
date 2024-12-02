# -*- coding: utf-8 -*-
{
    'name': "Transaction Template",

    'summary': "This is a transaction template",

    'description': """
            Scope of this module to fulfill the necessary features related to common transaction form.
    """,

    'author': "Bharath",
    'website': "https://www.kgisl.com/",
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','account','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_transaction_view.xml',
        'reports/ct_transaction_report.xml',
        'reports/ct_transaction_template.xml',
        'wizard/ct_transaction_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_transaction/static/src/css/*.css',
            'ct_transaction/static/src/css/*.scss',
            'ct_transaction/static/src/views/*.js',
            'ct_transaction/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

