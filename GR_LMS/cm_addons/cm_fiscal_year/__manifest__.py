# -*- coding: utf-8 -*-
{
    'name': "Fiscal Year",

    'summary': "This is a custom fiscal year master",

    'description': """Scope of this module to fulfill the necessary features related to fiscal year form.""",

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
        'views/cm_fiscal_year_view.xml',
        'wizard/cm_fiscal_year_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cm_fiscal_year/static/src/views/*.js',
            'cm_fiscal_year/static/src/**/*.xml',
            'cm_fiscal_year/static/src/**/*.css',
        ],
    },
    'license': 'LGPL-3',
}

