# -*- coding: utf-8 -*-
{
    'name': " HS/SAC Code Code",

    'summary': "This is a custom  HS/SAC Code Code",

    'description': """Scope of this module to fulfill the necessary features related to  HS/SAC Code Code form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_hsn_code_view.xml',
        'wizard/cm_hsn_code_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_hsn_code/static/src/views/*.js',
            'cm_hsn_code/static/src/**/*.xml',
            'cm_hsn_code/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

