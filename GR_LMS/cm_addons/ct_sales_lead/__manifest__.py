# -*- coding: utf-8 -*-
{
    'name': "Sales Lead",

    'summary': "This is a sales lead",

    'description': """
            Scope of this module to fulfill the necessary features related to sales lead form.
    """,

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_sales_lead_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_sales_lead/static/src/css/*.css',
            'ct_sales_lead/static/src/css/*.scss',
            'ct_sales_lead/static/src/views/*.js',
            'ct_sales_lead/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

