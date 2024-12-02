
# -*- coding: utf-8 -*-
{
    'name': "Calendar Year",

    'summary': "This is a custom calendar year",

    'description': """Scope of this module to fulfill the necessary features related to common calendar year form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_calendar_year_view.xml',
        'wizard/cm_calendar_year_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_calendar_year/static/src/views/*.js',
            'cm_calendar_year/static/src/**/*.xml',
            'cm_calendar_year/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
