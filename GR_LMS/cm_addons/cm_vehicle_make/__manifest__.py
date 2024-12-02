
# -*- coding: utf-8 -*-
{
    'name': "Vehicle Make",

    'summary': "This is a custom vehicle make",

    'description': """Scope of this module to fulfill the necessary features related to common vehicle make form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_vehicle_make_view.xml',
        'wizard/cm_vehicle_make_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_vehicle_make/static/src/views/*.js',
            'cm_vehicle_make/static/src/**/*.xml',
            'cm_vehicle_make/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
