
# -*- coding: utf-8 -*-
{
    'name': "Payment Term",

    'summary': "This is a custom payment term",

    'description': """Scope of this module to fulfill the necessary features related to common payment term form.""",

    'author': "Karthikeyan S",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_payment_term_view.xml',
        'wizard/cm_payment_term_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_payment_term/static/src/views/*.js',
            'cm_payment_term/static/src/**/*.xml',
            'cm_payment_term/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
