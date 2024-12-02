# -*- coding: utf-8 -*-
{
    'name': "Task Group Master",

    'summary': "Module to manage task group mapping",

    'description': """
        This module allows users to manage task group mapping in Odoo.
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
    'depends': ['base','mail','custom_properties'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_task_group_view.xml',
        'views/templates.xml',
        'wizard/cm_task_group_batch_inactive_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_task_group/static/src/views/*.js',
            'cm_task_group/static/src/**/*.xml',
            'cm_task_group/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
