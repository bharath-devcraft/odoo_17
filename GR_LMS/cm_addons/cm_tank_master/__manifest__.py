
# -*- coding: utf-8 -*-
{
    'name': "Tank Master",

    'summary': "This is a custom tank master",

    'description': """Scope of this module to fulfill the necessary features related to common tank master form.""",

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_tank_master_view.xml',
        'views/cm_soc_tank_view.xml',
        'views/cm_gscs_tank_view.xml',
        'views/cm_ot_op_tank_view.xml',
        'wizard/cm_tank_master_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tank_master/static/src/views/*.js',
            'cm_tank_master/static/src/**/*.xml',
            'cm_tank_master/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
