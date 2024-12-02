# -*- coding: utf-8 -*-
{
    'name': "Port",

    'summary': "This is a custom port master",

    'description': """Scope of this module to fulfill the necessary features related to port master.""",

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
        'views/cm_port_view.xml',
        'wizard/cm_port_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_port/static/src/views/*.js',
            'cm_port/static/src/**/*.xml',
            'cm_port/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

