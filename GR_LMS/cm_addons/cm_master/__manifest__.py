# -*- coding: utf-8 -*-
{
    'name': "Master Template",

    'summary': "This is a custom master template",

    'description': """Scope of this module to fulfill the necessary features related to common master form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_master_view.xml',
        'wizard/cm_master_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_master/static/src/views/*.js',
            'cm_master/static/src/**/*.xml',
            'cm_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

