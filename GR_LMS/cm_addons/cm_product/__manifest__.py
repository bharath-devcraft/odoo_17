
# -*- coding: utf-8 -*-
{
    'name': "Product",

    'summary': "This is a custom product",

    'description': """Scope of this module to fulfill the necessary features related to common product form.""",

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
        'views/cm_product_view.xml',
        'wizard/cm_product_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_product/static/src/views/*.js',
            'cm_product/static/src/**/*.xml',
            'cm_product/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
