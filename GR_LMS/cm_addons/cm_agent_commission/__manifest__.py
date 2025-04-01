
# -*- coding: utf-8 -*-
{
    'name': "Agent Commission",

    'summary': "This is a custom agent commission",

    'description': """Scope of this module to fulfill the necessary features related to common agent commission form.""",

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
        'views/cm_agent_commission_view.xml',
        'wizard/cm_agent_commission_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_agent_commission/static/src/views/*.js',
            'cm_agent_commission/static/src/**/*.xml',
            'cm_agent_commission/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
