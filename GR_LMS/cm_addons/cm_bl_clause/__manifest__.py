
# -*- coding: utf-8 -*-
{
    'name': "BL Clause",

    'summary': "This is a custom BL clause",

    'description': """Scope of this module to fulfill the necessary features related to common BL clause form.""",

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
        'views/cm_bl_clause_view.xml',
        'wizard/cm_bl_clause_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_bl_clause/static/src/views/*.js',
            'cm_bl_clause/static/src/**/*.xml',
            'cm_bl_clause/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
