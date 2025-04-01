# -*- coding: utf-8 -*-
{
    'name': "Customer Invoice",

    'summary': "This is a customer invoice",

    'description': """
            Scope of this module to fulfill the necessary features related to common customer invoice form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','cm_base_inherit'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_customer_invoice_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_customer_invoice/static/src/css/*.css',
            'ct_customer_invoice/static/src/css/*.scss',
            'ct_customer_invoice/static/src/views/*.js',
            'ct_customer_invoice/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

