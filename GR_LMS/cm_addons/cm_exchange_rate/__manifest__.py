
# -*- coding: utf-8 -*-
{
    'name': "Exchange Rate",

    'summary': "This is a custom exchange rate",

    'description': """Scope of this module to fulfill the necessary features related to common exchange rate form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_exchange_rate_view.xml',
        'wizard/cm_exchange_rate_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_exchange_rate/static/src/views/*.js',
            'cm_exchange_rate/static/src/**/*.xml',
            'cm_exchange_rate/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
