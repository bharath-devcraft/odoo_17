# -*- coding: utf-8 -*-
{
    'name': "Terminal",

    'summary': "This is a custom terminal",

    'description': """Scope of this module to fulfill the necessary features related to common terminal form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
	'data/audit_rule_data.xml',
	'data/security_rule.xml',
	'views/cm_terminal_view.xml',
	'wizard/cm_terminal_batch_inactive_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
		'cm_terminal/static/src/views/*.js',
		'cm_terminal/static/src/**/*.xml',
		'cm_terminal/static/src/**/*.css',
        ],
    },    
    'demo': [
        'demo/demo.xml',
    ],

    
    'license': 'LGPL-3',
}

