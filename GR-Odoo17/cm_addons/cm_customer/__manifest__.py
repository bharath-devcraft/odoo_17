# -*- coding: utf-8 -*-
{
    'name': "Customer Master",

    'summary': "This is a custom customer master",

    'description': """Scope of this module to fulfill the necessary features related to common customer master form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_customer_master_view.xml',
        'wizard/cm_customer_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_customer/static/src/views/*.js',
            'cm_customer/static/src/**/*.xml',
            'cm_customer/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

