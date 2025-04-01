# -*- coding: utf-8 -*-
{
    'name': "Rejection Reason",

    'summary': "This is a custom Rejection reason",

    'description': """Scope of this module to fulfill the necessary features related to Rejection reason form.""",

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_rejection_remark_view.xml',
        'wizard/cm_rejection_remark_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_rejection_remark/static/src/views/*.js',
            'cm_rejection_remark/static/src/**/*.xml',
            'cm_rejection_remark/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

