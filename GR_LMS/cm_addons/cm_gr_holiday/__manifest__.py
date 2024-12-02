
# -*- coding: utf-8 -*-
{
    'name': "GR Holiday",

    'summary': "This is a custom gr holiday",

    'description': """Scope of this module to fulfill the necessary features related to common gr holiday form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_gr_holiday_view.xml',
        'wizard/cm_gr_holiday_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_gr_holiday/static/src/views/*.js',
            'cm_gr_holiday/static/src/**/*.xml',
            'cm_gr_holiday/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
