
# -*- coding: utf-8 -*-
{
    'name': "KYC Master",

    'summary': "This is a custom kyc master",

    'description': """Scope of this module to fulfill the necessary features related to common kyc master form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_kyc_master_view.xml',
        'wizard/cm_kyc_master_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_kyc_master/static/src/views/fields/*.js',
            'cm_kyc_master/static/src/views/*.js',
            'cm_kyc_master/static/src/**/*.xml',
            'cm_kyc_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
