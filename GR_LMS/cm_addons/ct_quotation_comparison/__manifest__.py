# -*- coding: utf-8 -*-
{
    'name': "Quotation Comparison",

    'summary': "This is a quotation comparison",

    'description': """
            Scope of this module to fulfill the necessary features related to common quotation comparison form.
    """,

    'author': "Bharath",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','account','custom_properties','cm_fiscal_year','ct_quotation_submit'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_quotation_comparison_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_quotation_comparison/static/src/css/*.css',
            'ct_quotation_comparison/static/src/css/*.scss',
            'ct_quotation_comparison/static/src/views/*.js',
            'ct_quotation_comparison/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

