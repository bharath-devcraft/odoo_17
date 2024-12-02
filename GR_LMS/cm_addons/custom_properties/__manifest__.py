# -*- coding: utf-8 -*-
{
    'name': "Custom Properties",

    'summary': "Custom Properties",

    'description': """
          It covers fundamental configurations of business process. 
    """,

    'author': "Hari",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'auto_install': False,
    'version': '0.1',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'data/cm_groups_data.xml',
        'views/views.xml',
        'views/res_config_settings_views.xml',
        'views/ir_action_view.xml',
        'views/cp_mail_configuration_view.xml',
        'views/cp_sms_configuration_view.xml',
        'views/cp_mail_queue_view.xml',
        'views/cp_sms_queue_view.xml',
        'views/cp_ir_sequence_generate_view.xml',
        'views/cp_scheduler_view.xml',
        'views/cp_external_apis_view.xml',
        'views/report_templates.xml',
        'views/failure_history_views.xml',
        'data/ir_module_category_data.xml',
        'data/auto_execute_sql.xml',
        'data/audit_rule_data.xml',
        'data/report_layout.xml',
        'templates/webclient.xml',
        'templates/web_layout.xml',
        'views/cp_popup_notification_view.xml',
        'security/ir.model.access.csv',
        'views/gr_report_templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'assets': {
        'web._assets_primary_variables': [
            (
                'after', 
                'web/static/src/scss/primary_variables.scss', 
                'custom_properties/static/src/scss/colors.scss'
            ),
            (
                'after', 
                'web/static/src/scss/primary_variables.scss', 
                'custom_properties/static/src/scss/variables.scss'
            ),
        ],
        'web._assets_backend_helpers': [
            'custom_properties/static/src/scss/mixins.scss',
        ],
        'web.assets_web_dark': [
            (
                'after',
                'custom_properties/static/src/scss/variables.scss',
                'custom_properties/static/src/scss/variables.dark.scss',
            ),
            "custom_properties/static/src/**/*",
        ],      
        'web.assets_backend': [
            (
                'after',
                'web/static/src/webclient/webclient.js',
                'custom_properties/static/src/webclient/webclient.js',
            ),
            (
                'after',
                'web/static/src/webclient/webclient.xml',
                'custom_properties/static/src/webclient/webclient.xml',
            ),
            (
                'after',
                'web/static/src/webclient/webclient.js',
                'custom_properties/static/src/webclient/menus/app_menu_service.js',
            ),
            (
                'after',
                'web/static/src/webclient/webclient.js',
                'custom_properties/static/src/webclient/appsbar/appsbar.js',
            ),
        'custom_properties/static/src/webclient/**/*.xml',
        'custom_properties/static/src/webclient/**/*.scss',
        'custom_properties/static/src/webclient/**/*.js',
        'custom_properties/static/src/views/**/*.scss',
        "custom_properties/static/src/**/*"
        ],
        'web.report_assets_common': [
            "custom_properties/static/src/**/*",
        ],
     },
     'license': 'LGPL-3',
}

