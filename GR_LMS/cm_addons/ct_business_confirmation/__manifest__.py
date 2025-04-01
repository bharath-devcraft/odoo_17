# -*- coding: utf-8 -*-
{
    'name': "Business Confirmation",

    'summary': "This is a business confirmation",

    'description': """
            Scope of this module to fulfill the necessary features related to business confirmation form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','cm_base_inherit'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_business_confirmation_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_business_confirmation/static/src/css/*.css',
            'ct_business_confirmation/static/src/css/*.scss',
            'ct_business_confirmation/static/src/views/*.js',
            'ct_business_confirmation/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

