# -*- coding: utf-8 -*-
{
    'name': "Vessel Service Route",

    'summary': "This is a custom vessel service route",

    'description': """Scope of this module to fulfill the necessary features related to vessel service route form.""",

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
	    'views/cm_vessel_service_route_view.xml',
	    'wizard/cm_vessel_service_route_batch_inactive_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
		'cm_vessel_service_route/static/src/views/*.js',
		'cm_vessel_service_route/static/src/**/*.xml',
		'cm_vessel_service_route/static/src/**/*.css',
        ],
    },    
    'demo': [
        'demo/demo.xml',
    ],

    
    'license': 'LGPL-3',
}

