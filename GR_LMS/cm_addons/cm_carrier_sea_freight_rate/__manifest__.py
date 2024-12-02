
# -*- coding: utf-8 -*-
{
    'name': "Carrier Sea Freight Rate",

    'summary': "This is a custom carrier sea freight rate",

    'description': """Scope of this module to fulfill the necessary features related to common carrier sea freight rate form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_port'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_carrier_sea_freight_rate_view.xml',
        'wizard/cm_carrier_sea_freight_rate_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_carrier_sea_freight_rate/static/src/views/*.js',
            'cm_carrier_sea_freight_rate/static/src/**/*.xml',
            'cm_carrier_sea_freight_rate/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
