# -*- coding: utf-8 -*-
{
    'name': "Report",

    'summary': "Custom Report",

    'description': """
        
This module serves as a base for custom report modules within Odoo. It includes all essential views and functionalities, providing a solid foundation for new modules. Developer can utilize this module as a template when creating their custom report modules, streamlining the development process. Additionally, it's used as the default scaffold command master template, simplifying the setup of new projects..
    """,

    'author': "Praveenkumar M",
    'website': "https://www.kgisl.com",

    # Categories can be used to filter modules in modules listing
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cr_report_view.xml',
        'views/cr_report_qweb.xml',
        'views/cr_report_template.xml',
        'views/templates.xml',
        'data/audit_rule_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cr_report/static/src/js/action_manager.js',
            'cr_report/static/src/**/*.xml',
            'cr_report/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

