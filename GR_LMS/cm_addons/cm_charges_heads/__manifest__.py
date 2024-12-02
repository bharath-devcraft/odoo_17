# -*- coding: utf-8 -*-
{
    'name': "Charges Heads",

    'summary': "This is a custom charges heads.",

    'description': """Scope of this module to fulfill the necessary features related to charges heads form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','account','cm_hsn_code'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_charges_heads_view.xml',
        'wizard/cm_charges_heads_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_charges_heads/static/src/views/*.js',
            'cm_charges_heads/static/src/**/*.xml',
            'cm_charges_heads/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

