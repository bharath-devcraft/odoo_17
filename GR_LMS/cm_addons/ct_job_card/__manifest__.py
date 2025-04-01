# -*- coding: utf-8 -*-
{
    'name': "Job Card",

    'summary': "This is a job card",

    'description': """
            Scope of this module to fulfill the necessary features related to job card form.
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
        'views/ct_job_card_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_job_card/static/src/css/*.css',
            'ct_job_card/static/src/css/*.scss',
            'ct_job_card/static/src/views/*.js',
            'ct_job_card/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

