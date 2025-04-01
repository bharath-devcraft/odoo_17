
# -*- coding: utf-8 -*-
{
    'name': "Depot Product Cleaning",

    'summary': "This is a custom depot product cleaning",

    'description': """Scope of this module to fulfill the necessary features related to common depot product cleaning form.""",

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
        'views/cm_depot_product_cleaning_view.xml',
        'wizard/cm_depot_product_cleaning_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_depot_product_cleaning/static/src/views/*.js',
            'cm_depot_product_cleaning/static/src/**/*.xml',
            'cm_depot_product_cleaning/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
