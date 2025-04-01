
# -*- coding: utf-8 -*-
{
    'name': "Tank Tcode",

    'summary': "This is a custom tank tcode",

    'description': """Scope of this module to fulfill the necessary features related to common tank tcode form.""",

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
        'views/cm_tank_tcode_view.xml',
        'wizard/cm_tank_tcode_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tank_tcode/static/src/views/*.js',
            'cm_tank_tcode/static/src/**/*.xml',
            'cm_tank_tcode/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
