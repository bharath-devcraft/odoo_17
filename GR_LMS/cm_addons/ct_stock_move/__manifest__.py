# -*- coding: utf-8 -*-
{
    'name': "Stock Move",

    'summary': "This is a stock move and stock lot related module",

    'description': """
            Scope of this module to fulfill the necessary features related to stock move and stock lot form.
    """,

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_stock_move_view.xml',
        'views/ct_stock_lot_view.xml',
        # 'wizard/ct_stock_move_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_stock_move/static/src/css/*.css',
            'ct_stock_move/static/src/css/*.scss',
            'ct_stock_move/static/src/views/*.js',
            'ct_stock_move/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

