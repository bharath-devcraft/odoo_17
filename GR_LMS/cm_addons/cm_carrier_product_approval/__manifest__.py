
# -*- coding: utf-8 -*-
{
    'name': "Carrier Product Approval",

    'summary': "This is a custom carrier product approval",

    'description': """Scope of this module to fulfill the necessary features related to common carrier product approval form.""",

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
        'views/cm_carrier_product_approval_view.xml',
        'wizard/cm_carrier_product_approval_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_carrier_product_approval/static/src/views/*.js',
            'cm_carrier_product_approval/static/src/**/*.xml',
            'cm_carrier_product_approval/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
