# -*- coding: utf-8 -*-
{
    'name': "KYC",

    'summary': "This is a custom KYC",

    'description': """Scope of this module to fulfill the necessary features related to common KYC form.""",

    'author': "Hari",
    'website': "https://www.catalysts.com.sg",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_kyc_view.xml',
        'wizard/cm_kyc_batch_inactive_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
		'cm_kyc/static/src/views/*.js',
                'cm_kyc/static/src/views/fields/*.js',
		'cm_kyc/static/src/**/*.xml',
		'cm_kyc/static/src/**/*.css',
        ],
    },    
    'demo': [
        'demo/demo.xml',
    ],   
    'license': 'LGPL-3',
}

