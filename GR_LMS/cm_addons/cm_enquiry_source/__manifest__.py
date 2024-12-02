# -*- coding: utf-8 -*-
{
    'name': "Enquiry Source",

    'summary': "This is a custom enquiry source",

    'description': """Scope of this module to fulfill the necessary features related to enquiry source form.""",

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
        'views/cm_enquiry_source_view.xml',
        'wizard/cm_enquiry_source_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_enquiry_source/static/src/views/*.js',
            'cm_enquiry_source/static/src/**/*.xml',
            'cm_enquiry_source/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

