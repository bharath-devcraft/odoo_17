# -*- coding: utf-8 -*-
{
    'name': "cm_division_master",

    'summary': "Custom Master Template",

    'description': """
          Long description of module's purpose    
    """,

    'author': "Hari",
    'website': "https://www.kgisl.com",

    # Categories can be used to filter modules in modules listing
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','sh_message','custom_properties'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_division_master_view.xml',
        'views/templates.xml',
        'wizard/cm_division_master_batch_inactive_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_division_master/static/src/views/*.js',
            'cm_division_master/static/src/**/*.xml',
            'cm_division_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

