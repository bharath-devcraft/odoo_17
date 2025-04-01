# -*- coding: utf-8 -*-
{
    'name': "PO Advance",

    'summary': "This is a PO advance",

    'description': """
            Scope of this module to fulfill the necessary features related to PO advance form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','ct_purchase_order'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_po_advance_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_po_advance/static/src/css/*.css',
            'ct_po_advance/static/src/css/*.scss',
            'ct_po_advance/static/src/views/*.js',
            'ct_po_advance/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

