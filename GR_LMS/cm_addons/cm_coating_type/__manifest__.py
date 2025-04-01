
# -*- coding: utf-8 -*-
{
    'name': "Coating Type",

    'summary': "This is a custom coating type",

    'description': """Scope of this module to fulfill the necessary features related to common coating type form.""",

    'author': "Sathiskumar N",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_coating_type_view.xml',
        'wizard/cm_coating_type_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_coating_type/static/src/views/*.js',
            'cm_coating_type/static/src/**/*.xml',
            'cm_coating_type/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
