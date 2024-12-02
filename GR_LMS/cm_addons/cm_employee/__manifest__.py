
# -*- coding: utf-8 -*-
{
    'name': "Employee",

    'summary': "This is a custom employee",

    'description': """Scope of this module to fulfill the necessary features related to common employee form.""",

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
        'views/cm_employee_view.xml',
        'wizard/cm_employee_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_employee/static/src/views/*.js',
            'cm_employee/static/src/**/*.xml',
            'cm_employee/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
