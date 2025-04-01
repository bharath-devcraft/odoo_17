
# -*- coding: utf-8 -*-
{
    'name': "Damage Code",

    'summary': "This is a custom damage code",

    'description': """Scope of this module to fulfill the necessary features related to common damage code form.""",

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_damage_code_view.xml',
        'wizard/cm_damage_code_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_damage_code/static/src/views/*.js',
            'cm_damage_code/static/src/**/*.xml',
            'cm_damage_code/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
