
# -*- coding: utf-8 -*-
{
    'name': "Customs Work Tariff",

    'summary': "This is a custom customs work tariff",

    'description': """Scope of this module to fulfill the necessary features related to common customs work tariff form.""",

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
        'views/cm_customs_work_tariff_view.xml',
        'wizard/cm_customs_work_tariff_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_customs_work_tariff/static/src/views/*.js',
            'cm_customs_work_tariff/static/src/**/*.xml',
            'cm_customs_work_tariff/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
