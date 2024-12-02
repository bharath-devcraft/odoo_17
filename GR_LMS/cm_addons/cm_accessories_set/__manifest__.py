
# -*- coding: utf-8 -*-
{
    'name': "Accessories Set",

    'summary': "This is a custom accessories set",

    'description': """Scope of this module to fulfill the necessary features related to common accessories set form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','product','cm_product_inherit'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_accessories_set_view.xml',
        'wizard/cm_accessories_set_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_accessories_set/static/src/views/*.js',
            'cm_accessories_set/static/src/**/*.xml',
            'cm_accessories_set/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
