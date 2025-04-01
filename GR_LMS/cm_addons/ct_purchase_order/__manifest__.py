# -*- coding: utf-8 -*-
{
    'name': "Purchase Order",

    'summary': "This is a purchase order",

    'description': """
            Scope of this module to fulfill the necessary features related to purchase order form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','account','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_purchase_order_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_purchase_order/static/src/css/*.css',
            'ct_purchase_order/static/src/css/*.scss',
            'ct_purchase_order/static/src/views/*.js',
            'ct_purchase_order/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

