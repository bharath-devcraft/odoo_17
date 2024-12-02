
# -*- coding: utf-8 -*-
{
    'name': "Transport Route",

    'summary': "This is a custom transport route",

    'description': """Scope of this module to fulfill the necessary features related to common transport route form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_transport_location'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_transport_route_view.xml',
        'wizard/cm_transport_route_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_transport_route/static/src/views/*.js',
            'cm_transport_route/static/src/**/*.xml',
            'cm_transport_route/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
