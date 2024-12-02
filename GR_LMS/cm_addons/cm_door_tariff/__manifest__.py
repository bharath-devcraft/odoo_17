
# -*- coding: utf-8 -*-
{
    'name': "Door Tariff",

    'summary': "This is a custom door tariff",

    'description': """Scope of this module to fulfill the necessary features related to common door tariff form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_port','cm_base_inherit'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_door_tariff_view.xml',
        'wizard/cm_door_tariff_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_door_tariff/static/src/views/*.js',
            'cm_door_tariff/static/src/**/*.xml',
            'cm_door_tariff/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
