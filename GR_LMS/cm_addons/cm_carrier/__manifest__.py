
# -*- coding: utf-8 -*-
{
    'name': "Carrier",

    'summary': "This is a custom carrier",

    'description': """Scope of this module to fulfill the necessary features related to common carrier form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_carrier_view.xml',
        'wizard/cm_carrier_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_carrier/static/src/views/*.js',
            'cm_carrier/static/src/**/*.xml',
            'cm_carrier/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

