
# -*- coding: utf-8 -*-
{
    'name': "Department",

    'summary': "This is a custom department",

    'description': """Scope of this module to fulfill the necessary features related to common department form.""",

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
        'views/cm_department_view.xml',
        'wizard/cm_department_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_department/static/src/views/*.js',
            'cm_department/static/src/**/*.xml',
            'cm_department/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
