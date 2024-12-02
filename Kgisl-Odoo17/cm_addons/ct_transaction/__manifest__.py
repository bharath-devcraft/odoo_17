# -*- coding: utf-8 -*-
{
    'name': "Transaction",

    'summary': "Custom transaction module",

    'description': """
                This module serves as a foundation for custom transactional operations within Odoo.
                It encompasses all necessary views and functionalities, akin to a base module. 
                Subsequently, any individual intending to create a custom transactional module can utilize this module as a template.
                Furthermore, it is employed as the default scaffold command transaction template.
    """,

    'author': "Bharath",
    'website': "https://www.kgisl.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'KGiSL/custom_modules',
    'application' : True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','account','custom_properties','cm_fiscal_year'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/audit_rule_data.xml',
        'views/ct_transaction_view.xml',
        'views/templates.xml',
        'reports/ct_transaction_report.xml',
        'reports/ct_transaction_template.xml',
        'wizard/ct_transaction_batch_cancel_view.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'installable': True,
    #'post_init_hook': '_synchronize_cron',
    
    'assets': {
        'web.assets_backend': [
            'ct_transaction/static/src/css/*.css',
            'ct_transaction/static/src/css/*.scss',
            'ct_transaction/static/src/views/*.js',
            'ct_transaction/static/src/**/*.xml',
        ],
    },
    
    'license': 'LGPL-3',
}

