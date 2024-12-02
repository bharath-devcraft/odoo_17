
# -*- coding: utf-8 -*-
{
    'name': "Transport Vendor",

    'summary': "This is a custom transport vendor",

    'description': """Scope of this module to fulfill the necessary features related to common transport vendor form.""",

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_transport_vendor_view.xml',
        'wizard/cm_transport_vendor_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_transport_vendor/static/src/views/*.js',
            'cm_transport_vendor/static/src/**/*.xml',
            'cm_transport_vendor/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

