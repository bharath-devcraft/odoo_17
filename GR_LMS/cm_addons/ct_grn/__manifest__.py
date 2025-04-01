# -*- coding: utf-8 -*-
{
    'name': "GRN",

    'summary': "This is a GRN",

    'description': """
            Scope of this module to fulfill the necessary features related to GRN form.
    """,

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','account','custom_properties','cm_fiscal_year','ct_purchase_order'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_grn_view.xml',
        'reports/ct_grn_report.xml',
        'reports/ct_grn_template.xml',
        'wizard/ct_grn_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_grn/static/src/css/*.css',
            'ct_grn/static/src/css/*.scss',
            'ct_grn/static/src/views/*.js',
            'ct_grn/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

