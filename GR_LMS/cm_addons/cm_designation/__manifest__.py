
# -*- coding: utf-8 -*-
{
    'name': "Designation",

    'summary': "This is a custom designation",

    'description': """Scope of this module to fulfill the necessary features related to common designation form.""",

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
        'views/cm_designation_view.xml',
        'wizard/cm_designation_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_designation/static/src/views/*.js',
            'cm_designation/static/src/**/*.xml',
            'cm_designation/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
