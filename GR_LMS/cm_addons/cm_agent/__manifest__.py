# -*- coding: utf-8 -*-
{
    'name': "Agent Master",

    'summary': "This is a custom agent master",

    'description': """Scope of this module to fulfill the necessary features related to common agent master form.""",

    'author': "Karthikeyan S",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_city'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_agent_view.xml',
        'wizard/cm_agent_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_agent/static/src/views/*.js',
            'cm_agent/static/src/**/*.xml',
            'cm_agent/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

