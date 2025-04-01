# -*- coding: utf-8 -*-
{
    'name': "Domestic Business Conformation",

    'summary': "This is a domestic business conformation",

    'description': """
            Scope of this module to fulfill the necessary features related to domestic business conformation form.
    """,

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    'depends': ['base','mail','account','custom_properties','cm_fiscal_year'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_doms_business_confirmation_view.xml',
        'reports/ct_doms_business_confirmation_report.xml',
        'reports/ct_doms_business_confirmation_template.xml',
        'wizard/ct_doms_business_confirmation_batch_cancel_view.xml', 
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_doms_business_confirmation/static/src/css/*.css',
            'ct_doms_business_confirmation/static/src/css/*.scss',
            'ct_doms_business_confirmation/static/src/views/*.js',
            'ct_doms_business_confirmation/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

