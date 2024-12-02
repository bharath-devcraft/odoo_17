
# -*- coding: utf-8 -*-
{
    'name': "Vehicle Master",

    'summary': "This is a custom vehicle master",

    'description': """Scope of this module to fulfill the necessary features related to common vehicle master form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_master'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_vehicle_master_view.xml',
        'wizard/cm_vehicle_master_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_vehicle_master/static/src/views/*.js',
            'cm_vehicle_master/static/src/**/*.xml',
            'cm_vehicle_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

