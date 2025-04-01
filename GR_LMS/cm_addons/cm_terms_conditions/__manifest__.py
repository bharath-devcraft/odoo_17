
# -*- coding: utf-8 -*-
{
    'name': "Terms & Conditions",

    'summary': "This is a custom terms & conditions",

    'description': """Scope of this module to fulfill the necessary features related to common terms & conditions form.""",

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
        'views/cm_terms_conditions_view.xml',
        'wizard/cm_terms_conditions_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_terms_conditions/static/src/views/*.js',
            'cm_terms_conditions/static/src/**/*.xml',
            'cm_terms_conditions/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
