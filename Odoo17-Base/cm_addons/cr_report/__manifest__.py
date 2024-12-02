# -*- coding: utf-8 -*-
{
    'name': "Report",

    'summary': "This is custom PDF and Excel report ",

    'description': """Scope of this module to fulfill the necessary features related to reports.""",

    'author': "Praveenkumar M",
    'website': "https://www.kgisl.com",
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',    
    'depends': ['base','web'],

    'data': [
        'security/ir.model.access.csv',
        'views/cr_report_view.xml',
        'views/cr_report_qweb.xml',
        'views/cr_report_template.xml',           
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

