# -*- coding: utf-8 -*-
{
    'name': "Base Custom Modules",

    'summary': "Custom Master",

    'description': """
        
This module serves as a base for custom User Management modules within Odoo. It includes all essential views and functionalities, providing a solid foundation for new modules.
    """,

    'author': "Karthikeyan S",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','base','mail'],

    # always loaded
    'data': [
        'views/cm_tax_view.xml',        
        'views/cm_company_view.xml',        
        'views/cm_country_view.xml',        
        'views/cm_country_state_view.xml',        
        'views/cm_product_category_view.xml',        
        'views/cm_uom_view.xml',        
        'views/cm_currency_view.xml',        
        'views/cm_tax_group_view.xml',        
        'security/ir.model.access.csv',
        'wizard/cm_company_batch_inactive_view.xml',
        'wizard/cm_country_batch_inactive_view.xml',
        'wizard/cm_country_state_batch_inactive_view.xml',
        'wizard/cm_currency_batch_inactive_view.xml',
        'wizard/cm_product_category_batch_inactive_view.xml',
        'wizard/cm_tax_batch_inactive_view.xml',
        'wizard/cm_tax_group_batch_inactive_view.xml',
        'wizard/cm_uom_batch_inactive_view.xml',
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

