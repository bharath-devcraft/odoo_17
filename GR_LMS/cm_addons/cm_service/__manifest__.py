
# -*- coding: utf-8 -*-
{
    'name': "Service",

    'summary': "This is a custom service",

    'description': """Scope of this module to fulfill the necessary features related to common service form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_service_view.xml',
        'wizard/cm_service_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_service/static/src/views/*.js',
            'cm_service/static/src/**/*.xml',
            'cm_service/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
