# -*- coding: utf-8 -*-
{
    'name': "Master",

    'summary': "Custom Master",

    'description': """
        
This module serves as a base for custom master modules within Odoo. It includes all essential views and functionalities, providing a solid foundation for new modules. Developer can utilize this module as a template when creating their custom master modules, streamlining the development process. Additionally, it's used as the default scaffold command master template, simplifying the setup of new projects..
    """,

    'author': "Praveenkumar M",
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
        'views/cm_master_view.xml',
        'views/templates.xml',
        'wizard/cm_master_batch_inactive_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_master/static/src/views/*.js',
            'cm_master/static/src/**/*.xml',
            'cm_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

