# -*- coding: utf-8 -*-
{
    'name': "Tank Operator",

    'summary': "This is a custom tank operator",

    'description': """Scope of this module to fulfill the necessary features related to tank operator form.""",

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
        'views/cm_tank_operator_view.xml',
        'wizard/cm_tank_operator_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tank_operator/static/src/views/*.js',
            'cm_tank_operator/static/src/**/*.xml',
            'cm_tank_operator/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

