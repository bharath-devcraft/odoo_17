# -*- coding: utf-8 -*-
{
    'name': "Port Tariff",

    'summary': "This is a custom port tariff",

    'description': """Scope of this module to fulfill the necessary features related to port tariff form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_port_terminal','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_port_tariff_view.xml',
        'wizard/cm_port_tariff_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_port_tariff/static/src/views/*.js',
            'cm_port_tariff/static/src/**/*.xml',
            'cm_port_tariff/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

