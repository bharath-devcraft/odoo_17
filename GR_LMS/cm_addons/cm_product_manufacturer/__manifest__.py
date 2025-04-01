
# -*- coding: utf-8 -*-
{
    'name': "Product Manufacturer",

    'summary': "This is a custom product manufacturer",

    'description': """Scope of this module to fulfill the necessary features related to common product manufacturer form.""",

    'author': "Sathiskumar N",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_product_manufacturer_view.xml',
        'wizard/cm_product_manufacturer_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_product_manufacturer/static/src/views/*.js',
            'cm_product_manufacturer/static/src/**/*.xml',
            'cm_product_manufacturer/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
