# -*- coding: utf-8 -*-
{
    'name': "Depot Vendor Master",

    'summary': "This is a custom depot vendor master",

    'description': """Scope of this module to fulfill the necessary features related to common depot vendor master form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_depot_vendor_master_view.xml',
        'wizard/cm_depot_vendor_master_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_depot_vendor_master/static/src/views/*.js',
            'cm_depot_vendor_master/static/src/**/*.xml',
            'cm_depot_vendor_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

