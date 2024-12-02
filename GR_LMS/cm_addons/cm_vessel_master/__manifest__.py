# -*- coding: utf-8 -*-
{
    'name': "Vessel Master",

    'summary': "This is a custom vessel Master",

    'description': """Scope of this module to fulfill the necessary features related to vessel master form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_vessel_master_view.xml',
        'wizard/cm_vessel_master_batch_inactive_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
		'cm_vessel_master/static/src/views/*.js',
		'cm_vessel_master/static/src/**/*.xml',
		'cm_vessel_master/static/src/**/*.css',
        ],
    },    
    'demo': [
        'demo/demo.xml',
    ],   
    'license': 'LGPL-3',
}

