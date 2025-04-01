# -*- coding: utf-8 -*-
{
    'name': "Delivery Challan",

    'summary': "This is a delivery challan",

    'description': """
            Scope of this module to fulfill the necessary features related to delivery challan form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','ct_business_confirmation'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_delivery_challan_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_delivery_challan/static/src/css/*.css',
            'ct_delivery_challan/static/src/css/*.scss',
            'ct_delivery_challan/static/src/views/*.js',
            'ct_delivery_challan/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

