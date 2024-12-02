# -*- coding: utf-8 -*-
{
    'name': "Depot Location",

    'summary': "This is a custom depot location",

    'description': """Scope of this module to fulfill the necessary features related to depot location form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_depot_location_view.xml',
        'wizard/cm_depot_location_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_depot_location/static/src/views/*.js',
            'cm_depot_location/static/src/**/*.xml',
            'cm_depot_location/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

