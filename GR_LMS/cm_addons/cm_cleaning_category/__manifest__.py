
# -*- coding: utf-8 -*-
{
    'name': "Cleaning Category",

    'summary': "This is a custom cleaning category",

    'description': """Scope of this module to fulfill the necessary features related to common cleaning category form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_cleaning_category_view.xml',
        'wizard/cm_cleaning_category_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_cleaning_category/static/src/views/*.js',
            'cm_cleaning_category/static/src/**/*.xml',
            'cm_cleaning_category/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
