# -*- coding: utf-8 -*-
{
    'name': "Business Vertical Sub Type",

    'summary': "This is a custom business vertical sub type master",

    'description': """Scope of this module to fulfill the necessary features related to business vertical sub type form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_business_vertical_sub_type_view.xml',
        'wizard/cm_business_vertical_sub_type_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_business_vertical_sub_type/static/src/views/*.js',
            'cm_business_vertical_sub_type/static/src/**/*.xml',
            'cm_business_vertical_sub_type/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

