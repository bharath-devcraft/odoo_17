
# -*- coding: utf-8 -*-
{
    'name': "Tender Contract",

    'summary': "This is a custom tender contract",

    'description': """Scope of this module to fulfill the necessary features related to common tender contract form.""",

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
        'views/cm_tender_contract_view.xml',
        'wizard/cm_tender_contract_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tender_contract/static/src/views/*.js',
            'cm_tender_contract/static/src/**/*.xml',
            'cm_tender_contract/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
