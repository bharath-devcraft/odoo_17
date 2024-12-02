# -*- coding: utf-8 -*-
{
    'name': "Base Custom Modules",

    'summary': "Custom Master",

    'description': """
        
This module serves as a base for custom User Management modules within Odoo. It includes all essential views and functionalities, providing a solid foundation for new modules.
    """,

    'author': "Karthikeyan Subramani",
    'website': "https://www.kgisl.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','base','mail'],

    # always loaded
    'data': [
        'views/cm_tax_view.xml',        
        'views/cm_company_view.xml',        
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
     'assets': {
        'web.assets_backend': [
            'cm_base_inherit/static/src/views/*.js',
            'cm_base_inherit/static/src/**/*.xml',
            'cm_base_inherit/static/src/**/*.css',
        ],
    },

   
}

