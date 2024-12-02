# -*- coding: utf-8 -*-
{
    'name': "Profile Master",

    'summary': "This is a custom profile master",

    'description': """Scope of this module to fulfill the necessary features related to common profile master form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'views/cm_profile_master_view.xml',
        'wizard/cm_profile_master_batch_inactive_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_profile_master/static/src/views/*.js',
            'cm_profile_master/static/src/**/*.xml',
            'cm_profile_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

