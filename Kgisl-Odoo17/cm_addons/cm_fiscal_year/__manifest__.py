# -*- coding: utf-8 -*-
{
    'name': "Fiscal Year Master",

    'summary': "Module to manage fiscal years",

    'description': """
        This module allows users to manage fiscal years in Odoo. 
        It provides features for creating, editing, and closing fiscal years, 
        ensuring proper financial period management within the system.
    """,

    'author': "Bharath",
    'website': "https://www.kgisl.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','sh_message','custom_properties'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_fiscal_year_view.xml',
        'views/templates.xml',
        'wizard/cm_fiscal_year_batch_inactive_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_fiscal_year/static/src/views/*.js',
            'cm_fiscal_year/static/src/**/*.xml',
            'cm_fiscal_year/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

