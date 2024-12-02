# -*- coding: utf-8 -*-
{
    'name': "City",

    'summary': "This is a custom city master",

    'description': """Scope of this module to fulfill the necessary features related to common city form.""",

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
        'views/cm_city_view.xml',
        'wizard/cm_city_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_city/static/src/views/*.js',
            'cm_city/static/src/**/*.xml',
            'cm_city/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

