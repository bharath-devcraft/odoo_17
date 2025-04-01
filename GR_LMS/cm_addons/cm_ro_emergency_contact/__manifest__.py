
# -*- coding: utf-8 -*-
{
    'name': "RO Emergency Contact",

    'summary': "This is a custom RO emergency contact",

    'description': """Scope of this module to fulfill the necessary features related to common RO emergency contact form.""",

    'author': "Karthikeyan S",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_ro_emergency_contact_view.xml',
        'wizard/cm_ro_emergency_contact_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_ro_emergency_contact/static/src/views/*.js',
            'cm_ro_emergency_contact/static/src/**/*.xml',
            'cm_ro_emergency_contact/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
