# -*- coding: utf-8 -*-
{
    'name': "Store Issue",

    'summary': "This is a store issue template",

    'description': """
            Scope of this module to fulfill the necessary features related to common store issue form.
    """,

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_store_issue_view.xml',
        'wizard/ct_store_issue_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_store_issue/static/src/css/*.css',
            'ct_store_issue/static/src/css/*.scss',
            'ct_store_issue/static/src/views/*.js',
            'ct_store_issue/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

