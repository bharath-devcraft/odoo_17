
# -*- coding: utf-8 -*-
{
    'name': "Item",

    'summary': "This is a custom item",

    'description': """Scope of this module to fulfill the necessary features related to common item form.""",

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
        'views/cm_item_view.xml',
        'wizard/cm_item_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_item/static/src/views/*.js',
            'cm_item/static/src/**/*.xml',
            'cm_item/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
