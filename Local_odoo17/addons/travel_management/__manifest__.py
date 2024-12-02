# -*- coding: utf-8 -*-
{
    'name': "travel_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','travel_package_master','mail','board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/travel_management.xml',
        'views/portal_templates.xml',
        # ~ 'views/templates.xml',
        'reports/travel_management_report.xml',
        'reports/travel_management_template.xml',
        'data/travel_management_peyment_request_mail_template.xml',
        'data/mail_message_subtype_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/css/*.css',
            'travel_management/static/src/css/*.scss',
            #'travel_management/static/src/js/*.js',
        ],
        # ~ 'web.assets_frontend': [
            # ~ 'purchase/static/src/js/purchase_datetimepicker.js',
            # ~ 'purchase/static/src/js/purchase_portal_sidebar.js',
        # ~ ],
    },
    'license': 'LGPL-3',
}
