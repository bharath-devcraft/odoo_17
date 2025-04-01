# -*- coding: utf-8 -*-
{
    'name': "Disposal Certificate",

    'summary': "This is a disposal certificate",

    'description': """
            Scope of this module to fulfill the necessary features related to disposal certificate form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','ct_stock_move'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_disposal_certificate_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_disposal_certificate/static/src/css/*.css',
            'ct_disposal_certificate/static/src/css/*.scss',
            'ct_disposal_certificate/static/src/views/*.js',
            'ct_disposal_certificate/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

