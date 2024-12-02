
# -*- coding: utf-8 -*-
{
    'name': "Tank Lease Tariff",

    'summary': "This is a custom tank lease tariff",

    'description': """Scope of this module to fulfill the necessary features related to common tank lease tariff form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_base_inherit'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_tank_lease_tariff_view.xml',
        'wizard/cm_tank_lease_tariff_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tank_lease_tariff/static/src/views/*.js',
            'cm_tank_lease_tariff/static/src/**/*.xml',
            'cm_tank_lease_tariff/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
