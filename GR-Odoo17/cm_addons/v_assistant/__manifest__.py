# -*- coding: utf-8 -*-
{
    'name': "v_assistant",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Hari",
    'website': "https://www.catalysts.com.sg",
    'category': 'Catalyst/custom_modules',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','base_setup', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/chatgpt_model_data.xml',
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        #'views/templates.xml',
        'views/v_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
