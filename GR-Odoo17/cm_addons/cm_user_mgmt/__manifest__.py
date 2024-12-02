# -*- coding: utf-8 -*-
{
    'name': "User Management",

    'summary': "Custom Master",

    'description': """
        
This module serves as a base for custom User Management modules within Odoo. It includes all essential views and functionalities, providing a solid foundation for new modules.
    """,

    'author': "Karthikeyan Subramani",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','cm_fiscal_year'],

    # always loaded
    'data': [
        'views/cm_user_mgmt_view.xml',
        'data/audit_rule_data.xml',
        'data/base_model_access_data.xml',
        'security/ir.model.access.csv',        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
     'assets': {
        'web.assets_backend': [
            'cm_user_mgmt/static/src/views/*.js',
            'cm_user_mgmt/static/src/**/*.xml',
            'cm_user_mgmt/static/src/**/*.css',
        ],
    },

   
}

