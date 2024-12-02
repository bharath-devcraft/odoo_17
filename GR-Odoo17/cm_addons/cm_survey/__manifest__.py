# -*- coding: utf-8 -*-
{
    'name': "Survey",

    'summary': "Custom Survey",

    'description': """
        This module allows you to create and manage surveys for collecting feedback from users or customers.
        Key Features:
        - Create customizable surveys
        - Collect and store feedback responses
        - Analyze survey results
    """,

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','custom_properties'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cm_survey_view.xml',
        'views/templates.xml',
        'data/audit_rule_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_survey/static/src/views/*.js',
            'cm_survey/static/src/**/*.xml',
            'cm_survey/static/src/**/*.css',
            "cm_survey/static/src/**/*"
        ],
    },
    
    'license': 'LGPL-3',
}

