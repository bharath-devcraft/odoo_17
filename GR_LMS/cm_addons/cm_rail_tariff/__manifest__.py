# -*- coding: utf-8 -*-
{
    'name': "Rail Tariff",

    'summary': "This is a rail tariff",

    'description': """Scope of this module to fulfill the necessary features related to rail tariff form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_rail_tariff_view.xml',
        'wizard/cm_rail_tariff_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_rail_tariff/static/src/views/*.js',
            'cm_rail_tariff/static/src/**/*.xml',
            'cm_rail_tariff/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

