# -*- coding: utf-8 -*-
{
    'name': "Tank Operators",

    'summary': "This is a custom tank Operators",

    'description': """Scope of this module to fulfill the necessary features related to common tank operators form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_tank_operators_view.xml',
        'wizard/cm_tank_operators_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tank_operators/static/src/views/*.js',
            'cm_tank_operators/static/src/**/*.xml',
            'cm_tank_operators/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

