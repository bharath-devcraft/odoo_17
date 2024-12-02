# -*- coding: utf-8 -*-
{
    'name': "Base Product Inherit",

    'summary': "This is a custom base product inherit master",

    'description': """Scope of this module to fulfill the necessary features related to base product inherit master form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','product', 'cm_hsn_code'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_product_template_view.xml',
        'views/cm_product_template_accessories_view.xml',
        'wizard/cm_product_template_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_product_inherit/static/src/views/*.js',
            'cm_product_inherit/static/src/**/*.xml',
            'cm_product_inherit/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

