# -*- coding: utf-8 -*-
{
    'name': "Branch",

    'summary': "This is a custom branch master",

    'description': """Scope of this module to fulfill the necessary features related to branch master form.""",

    'author': "Karthikeyan S",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_base_inherit'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_branch_view.xml',
        'wizard/cm_branch_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_branch/static/src/views/*.js',
            'cm_branch/static/src/**/*.xml',
            'cm_branch/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

