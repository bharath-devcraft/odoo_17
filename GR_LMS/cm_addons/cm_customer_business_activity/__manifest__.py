# -*- coding: utf-8 -*-
{
    'name': "Customer Business Activity",

    'summary': "This is a customer business activity",

    'description': """Scope of this module to fulfill the necessary features related to customer business activity form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_customer_business_activity_view.xml',
        'wizard/cm_customer_business_activity_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_customer_business_activity/static/src/views/*.js',
            'cm_customer_business_activity/static/src/**/*.xml',
            'cm_customer_business_activity/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

