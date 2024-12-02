# -*- coding: utf-8 -*-
{
    'name': "Product Restriction",

    'summary': "This is a custom product restriction",

    'description': """Scope of this module to fulfill the necessary features related to product restriction form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_port_product_restriction_view.xml',
        'wizard/cm_port_product_restriction_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_port_product_restriction/static/src/views/*.js',
            'cm_port_product_restriction/static/src/**/*.xml',
            'cm_port_product_restriction/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

