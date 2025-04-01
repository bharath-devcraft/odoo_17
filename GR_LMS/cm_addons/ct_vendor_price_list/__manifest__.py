# -*- coding: utf-8 -*-
{
    'name': "Vendor Price List",

    'summary': "This is a vendor price list",

    'description': """
            Scope of this module to fulfill the necessary features related to vendor price list form.
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
        'views/ct_vendor_price_list_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_vendor_price_list/static/src/css/*.css',
            'ct_vendor_price_list/static/src/css/*.scss',
            'ct_vendor_price_list/static/src/views/*.js',
            'ct_vendor_price_list/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

