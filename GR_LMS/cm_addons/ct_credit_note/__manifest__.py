# -*- coding: utf-8 -*-
{
    'name': "Credit Note",

    'summary': "This is a credit note",

    'description': """
            Scope of this module to fulfill the necessary features related to credit note form.
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
        'views/ct_credit_note_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_credit_note/static/src/css/*.css',
            'ct_credit_note/static/src/css/*.scss',
            'ct_credit_note/static/src/views/*.js',
            'ct_credit_note/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

