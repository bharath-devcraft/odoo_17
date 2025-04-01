# -*- coding: utf-8 -*-
{
    'name': "Gate Pass",

    'summary': "This is a gate pass module",

    'description': """
            Scope of this module to fulfill the necessary features related to gate pass form.
    """,

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year','product','ct_stock_move'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_gate_pass_view.xml',
        'wizard/ct_gate_pass_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_gate_pass/static/src/css/*.css',
            'ct_gate_pass/static/src/css/*.scss',
            'ct_gate_pass/static/src/views/*.js',
            'ct_gate_pass/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

