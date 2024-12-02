
# -*- coding: utf-8 -*-
{
    'name': "Vendor Type",

    'summary': "This is a custom vendor type",

    'description': """Scope of this module to fulfill the necessary features related to common vendor type form.""",

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
        'views/cm_vendor_type_view.xml',
        'wizard/cm_vendor_type_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_vendor_type/static/src/views/*.js',
            'cm_vendor_type/static/src/**/*.xml',
            'cm_vendor_type/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
