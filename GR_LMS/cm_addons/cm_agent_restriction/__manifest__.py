
# -*- coding: utf-8 -*-
{
    'name': "Agent Restriction",

    'summary': "This is a custom agent restriction",

    'description': """Scope of this module to fulfill the necessary features related to common agent restriction form.""",

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
        'views/cm_agent_restriction_view.xml',
        'wizard/cm_agent_restriction_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_agent_restriction/static/src/views/*.js',
            'cm_agent_restriction/static/src/**/*.xml',
            'cm_agent_restriction/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
