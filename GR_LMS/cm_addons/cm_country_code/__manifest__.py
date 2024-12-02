
# -*- coding: utf-8 -*-
{
    'name': "Country Code",

    'summary': "This is a custom country code",

    'description': """Scope of this module to fulfill the necessary features related to common country code form.""",

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
        'views/cm_country_code_view.xml',
        'wizard/cm_country_code_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_country_code/static/src/views/*.js',
            'cm_country_code/static/src/**/*.xml',
            'cm_country_code/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
