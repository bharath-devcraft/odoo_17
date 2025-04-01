# -*- coding: utf-8 -*-
{
    'name': "Sales Return",

    'summary': "This is a sales return",

    'description': """
            Scope of this module to fulfill the necessary features related to sales return form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','ct_stock_move','cm_product_inherit'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_sales_return_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_sales_return/static/src/css/*.css',
            'ct_sales_return/static/src/css/*.scss',
            'ct_sales_return/static/src/views/*.js',
            'ct_sales_return/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

