# -*- coding: utf-8 -*-
{
    'name': "Profile Master",

    'summary': "Custom Profile Master",

    'description': """
        
This module serves as a base for custom Profile master modules within Odoo. It includes all essential views and functionalities, providing a solid foundation for new modules. Developer can utilize this module as a template when creating their custom profile master modules, streamlining the development process. Additionally, it's used as the default scaffold command profile master template, simplifying the setup of new projects..
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
        'views/cm_profile_master_view.xml',
        'views/templates.xml',
        'wizard/cm_profile_master_batch_inactive_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_profile_master/static/src/views/*.js',
            'cm_profile_master/static/src/**/*.xml',
            'cm_profile_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

