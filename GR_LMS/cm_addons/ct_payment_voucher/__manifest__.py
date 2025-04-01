# -*- coding: utf-8 -*-
{
    'name': "Payment Voucher",

    'summary': "This is a payment voucher",

    'description': """
            Scope of this module to fulfill the necessary features related to payment voucher form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_payment_voucher_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_payment_voucher/static/src/css/*.css',
            'ct_payment_voucher/static/src/css/*.scss',
            'ct_payment_voucher/static/src/views/*.js',
            'ct_payment_voucher/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

