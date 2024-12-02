# -*- coding: utf-8 -*-
{
    'name': "Shipment Term",

    'summary': "This is a custom shipment term master",

    'description': """Scope of this module to fulfill the necessary features related to shipment term master form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_shipment_term_view.xml',
        'wizard/cm_shipment_term_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_shipment_term/static/src/views/*.js',
            'cm_shipment_term/static/src/**/*.xml',
            'cm_shipment_term/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

