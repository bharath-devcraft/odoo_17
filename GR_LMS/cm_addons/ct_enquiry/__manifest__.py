# -*- coding: utf-8 -*-
{
    'name': "Enquiry",

    'summary': "This is a enquiry",

    'description': """
            Scope of this module to fulfill the necessary features related to enquiry form.
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
        'views/ct_enquiry_view.xml',
    ],
    'demo': [],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'ct_enquiry/static/src/css/*.css',
            'ct_enquiry/static/src/css/*.scss',
            'ct_enquiry/static/src/views/*.js',
            'ct_enquiry/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

