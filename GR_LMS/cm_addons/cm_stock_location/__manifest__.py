
# -*- coding: utf-8 -*-
{
    'name': "Stock Location",

    'summary': "This is a custom stock location",

    'description': """Scope of this module to fulfill the necessary features related to common stock location form.""",

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'data/default_data.xml',
        'views/cm_stock_location_view.xml',
        'wizard/cm_stock_location_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_stock_location/static/src/views/*.js',
            'cm_stock_location/static/src/**/*.xml',
            'cm_stock_location/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
