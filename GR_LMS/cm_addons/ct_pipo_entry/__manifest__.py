# -*- coding: utf-8 -*-
{
    'name': "PI-PO Creation",

    'summary': "This is a PI-PO creation",

    'description': """
            Scope of this module to fulfill the necessary features related to PI-PO creation form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','ct_vendor_price_list'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_pipo_entry_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_pipo_entry/static/src/css/*.css',
            'ct_pipo_entry/static/src/css/*.scss',
            'ct_pipo_entry/static/src/views/*.js',
            'ct_pipo_entry/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

